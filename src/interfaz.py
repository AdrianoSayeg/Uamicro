from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from P1 import Ui_Form
from uam1up import Microprocesador

class uamicro1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cpu = Microprocesador()
        self.m = 0

        self.ui.pushButton_ejecutar.clicked.connect(self.ejecutar)
        self.ui.pushButton_modificar.clicked.connect(self.celda_modificada)
        self.ui.pushButton_archivos.clicked.connect(self.abrir_archivo)
        self.ui.pushButton_modo.clicked.connect(self.modo)

        self.actualizar_lista()

    def modo(self):
        self.m = 1 - self.m
        self.ui.label_busc_2.setText(["CONTINUO", "PASOS"][self.m])
        self.reiniciar()

    def reiniciar(self):
        self.cpu.reiniciar()
        self.actualizar_labels()

    def abrir_archivo(self):
        self.reiniciar()
        ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Selecciona un archivo", "", "Todos los archivos (*)")
        if ruta_archivo:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                lista = [int(linea.strip(), 16) for linea in f if linea.strip()]
            self.cpu.cargar_memoria(lista)
            self.actualizar_lista()

    def celda_modificada(self):
        filas = self.ui.tableWidget.rowCount()
        items = [int(self.ui.tableWidget.item(fila, 1).text(), 16) for fila in range(filas)]
        self.cpu.cargar_memoria(items)
        self.reiniciar()

    def actualizar_labels(self):
        cpu = self.cpu
        self.ui.label_A.setText(f"{cpu.ACC_A.enable():02x}")
        self.ui.label_B.setText(f"{cpu.ACC_B.enable():02x}")
        self.ui.label_ALU.setText(f"{cpu.ALU.enable():02x}")
        self.ui.label_PC.setText(f"{cpu.PC.enable():02x}")
        self.ui.label_AR.setText(f"{cpu.AR.enable():02x}")
        self.ui.label_IR.setText(f"{cpu.IR.enable():02x}")
        self.ui.label_OUT.setText(f"{cpu.MEM.enable(0xff):02x}")
        self.ui.label_busc.setText(f"{cpu.busc:016b}")
        self.ui.label_busd.setText(f"{cpu.busd:02x}")

    def actualizar_lista(self):
        self.ui.tableWidget.setRowCount(len(self.cpu.MEM.lista))
        for row, x in enumerate(self.cpu.MEM.lista):
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{row:02x}'))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{x:02x}'))
        row = 0
        while row + 1 < len(self.cpu.MEM.lista):
            x = self.cpu.MEM.lista[row]
            hex_instr = f'{x:02x}'
            if hex_instr in self.cpu.nemonico:
                nem = self.cpu.nemonico[hex_instr]
                if hex_instr[0] == '0':
                    row += 1
                    self.ui.tableWidget.setItem(row - 1, 2, QtWidgets.QTableWidgetItem(f'{nem} ({self.cpu.MEM.lista[row]:02X})'))
                    self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(''))
                else:
                    self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{nem}'))
            else:
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(''))
            row += 1

    def ejecutar(self):
        if self.cpu.ex:
            self.reiniciar()
        else:
            self.actualizar_labels()
            self.cpu.paso()
            if self.m == 0:
                QTimer.singleShot(50, self.ejecutar)
