from componentes import registro, ALU, pc, MEM, control, nemonico
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from P1 import Ui_Form  # Interfaz generada desde Qt Designer


class uamicro1(QtWidgets.QWidget):
    #Clase que representa una interfaz gráfica y simulador funcional de un microprocesador simple.

    def __init__(self):
        #Inicializa la interfaz gráfica y los componentes internos del microprocesador.
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Inicialización de los registros y unidades funcionales del microprocesador
        self.ACC_A = registro("ACC_A")
        self.ACC_B = registro("ACC_B")
        self.PC = pc("PC")
        self.ALU = ALU()
        self.MAR = registro("MAR")
        self.AR = registro("AR")
        self.MEM = MEM("MEM")
        self.IR = registro("IR")

        # Control y estado del procesador
        self.control = control
        self.busc = 0x0     # bus de control
        self.busd = 0x0     # bus de datos
        self.ex = 0         # bit de fin de ejecución
        self.cont = 0       # contador de microciclos
        self.nemonico = nemonico

        # Conectar los botones de la interfaz a sus respectivas funciones
        self.ui.pushButton.clicked.connect(self.ejecutar)
        self.ui.pushButton_2.clicked.connect(self.celda_modificada)
        self.ui.pushButton_1.clicked.connect(self.abrir_archivo)

        # Cargar la memoria en la tabla
        self.actualizar_lista()

    def abrir_archivo(self):
        """
        Abre un archivo de texto con instrucciones de la UAMICRO1 (en hexadecimal, una por línea) y lo carga en memoria.
        """
        ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Selecciona un archivo", "", "Todos los archivos (*)")
        if ruta_archivo:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                lista = [int(linea.strip(), 16) for linea in f if linea.strip() != ""]
            self.cargar_memoria(lista)

    def celda_modificada(self):
        # Permite modificar directamente la memoria a través de la tabla en la interfaz.
        filas = self.ui.tableWidget.rowCount()
        items = [int(self.ui.tableWidget.item(fila, 0).text(), 16) for fila in range(filas)]
        self.cargar_memoria(items)

    def actualizar_labels(self):
        # Actualiza las etiquetas de la interfaz con los valores actuales de los registros y buses.
        self.ui.label_A.setText(f"{self.ACC_A.enable():02x}")
        self.ui.label_B.setText(f"{self.ACC_B.enable():02x}")
        self.ui.label_ALU.setText(f"{self.ALU.enable():02x}")
        self.ui.label_PC.setText(f"{self.PC.enable():02x}")
        self.ui.label_AR.setText(f"{self.AR.enable():02x}")
        self.ui.label_IR.setText(f"{self.IR.enable():02x}")
        self.ui.label_OUT.setText(f"{self.MEM.enable(0xff):02x}")
        self.ui.label_busc.setText(f"{self.busc:016b}")
        self.ui.label_busd.setText(f"{self.busd:02x}")

    def cargar_memoria(self, programa):
        # Carga una lista en memoria.
        for i in range(len(programa)):
            self.MEM.load([i, programa[i]])
        self.actualizar_lista()

    def actualizar_lista(self):
        # Actualiza la tabla de memoria en la interfaz gráfica y traduce las instrucciones a nemónicos.
        self.ui.tableWidget.setRowCount(len(self.MEM.lista))
        for row, x in enumerate(self.MEM.lista):
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{x:02x}'))
        row = 0
        while row + 1 < len(self.MEM.lista):
            x = self.MEM.lista[row]
            hex_instr = f'{x:02x}'
            if hex_instr in self.nemonico:
                nemonico = self.nemonico[hex_instr]
                if hex_instr[0] == '0':  # instrucción con operando
                    row += 1
                    self.ui.tableWidget.setItem(row - 1, 1, QtWidgets.QTableWidgetItem(f'{nemonico} ({self.MEM.lista[row]:02X})'))
                    self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                else:
                    self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{nemonico}'))
            else:
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
            row += 1

    def ejecutar(self):
        # Ejecuta las instrucciones del microprocesador paso a paso y haciendo pausas.
        
        if self.ex:  # Si la ejecución terminó, limpia el contador de programa y deja listo el microprocesador para ejecutar un programa.
            self.PC.clear()
            self.cont = 0
            self.ex = 0
        else:
            self.actualizar_labels() # mostramos los valores en la interfaz.

            # Obtener la linea de control.
            self.busc = self.control[self.cont][f"{self.IR.enable():02x}"]

            # Asigna cada bit a una señal de control.
            self.ex, _, EA, LA, SU, EU, LB, EB, IPC, EPC, LAR, EAR, LIR, LM, VMA, WR = map(int, f'{self.busc:016b}')

            # ALU calcula resultado dependiendo de la señal SU
            self.ALU.operar(self.ACC_A.enable(), self.ACC_B.enable(), SU)

            # Decidir qué poner en el bus de datos (busd)
            if EA: self.busd = self.ACC_A.enable()
            if EB: self.busd = self.ACC_B.enable()
            if EU: self.busd = self.ALU.enable()
            if EPC: self.busd = self.PC.enable()
            if EAR: self.busd = self.AR.enable()

            # Acceso a memoria (lectura o escritura)
            if VMA:
                if WR:  # lectura
                    self.busd = self.MEM.enable(self.MAR.enable())
                else:   # escritura
                    self.MEM.load([self.MAR.enable(), self.busd])

            # Cargar registros con el valor del bus de datos
            if LA: self.ACC_A.load(self.busd)
            if LB: self.ACC_B.load(self.busd)
            if LAR: self.AR.load(self.busd)
            if LIR: self.IR.load(self.busd)
            if LM: self.MAR.load(self.busd)

            # Incrementar PC si corresponde
            if IPC: self.PC.incrementa()

            # Actualizar el contador para avanzar al siguiente ciclo
            self.cont = (self.cont + 1) % 7
            QTimer.singleShot(50, self.ejecutar)  # Ejecutar el siguiente ciclo con 50 ms de retardo


# Código para correr la aplicación
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = uamicro1()
    window.show()
    sys.exit(app.exec_())
