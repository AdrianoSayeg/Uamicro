from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
# Importamos la nueva interfaz que hemos modificado
from P1_cleaned import Ui_Form
# Importamos el Microprocesador (se asume que existe el archivo uam1up.py)
from uamicro2 import Microprocesador

class UAMicroProcessorGUI(QtWidgets.QWidget):
    """
    Clase principal de la interfaz de usuario para el simulador del microprocesador.
    Gestiona la interacción del usuario, la visualización de los registros y la memoria,
    y la ejecución del programa.
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cpu = Microprocesador()
        self.is_continuous_mode = True  # True para 'CONTINUO', False para 'PASOS'

        # Conectar los botones a sus respectivas funciones
        self.ui.pushButton_ejecutar.clicked.connect(self.run_program)
        self.ui.pushButton_modificar.clicked.connect(self.modify_memory)
        self.ui.pushButton_archivos.clicked.connect(self.open_file)
        self.ui.pushButton_modo.clicked.connect(self.toggle_mode)

        # Inicializar la interfaz con los valores del microprocesador
        self.update_memory_table()
        self.update_labels()

    def toggle_mode(self):
        """
        Cambia entre los modos de ejecución 'CONTINUO' y 'PASOS'.
        """
        self.is_continuous_mode = not self.is_continuous_mode
        mode_text = "CONTINUO" if self.is_continuous_mode else "PASOS"
        self.ui.label_busc_2.setText(mode_text)
        self.reset_processor()

    def reset_processor(self):
        """
        Reinicia el estado del microprocesador y actualiza la GUI.
        """
        self.cpu.reiniciar()
        self.update_labels()

    def open_file(self):
        """
        Abre un archivo de programa, lo carga en la memoria del microprocesador
        y actualiza la GUI.
        """
        self.reset_processor()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Selecciona un archivo", "", "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Lee cada línea y la convierte a un valor hexadecimal
                program_data = [int(line.strip(), 16) for line in f if line.strip()]
            
            self.cpu.cargar_memoria(program_data)
            self.update_memory_table()

    def modify_memory(self):
        """
        Lee el contenido de la tabla de memoria en la GUI, lo carga
        en la memoria del microprocesador y reinicia el estado.
        """
        num_rows = self.ui.tableWidget.rowCount()
        program_data = []
        for row in range(num_rows):
            item = self.ui.tableWidget.item(row, 1)
            if item:
                try:
                    # Lee el dato y lo convierte de hexadecimal a entero
                    value = int(item.text(), 16)
                    program_data.append(value)
                except (ValueError, IndexError):
                    # Maneja errores si el dato no es válido
                    QtWidgets.QMessageBox.warning(
                        self, "Error de formato",
                        f"El dato en la fila {row} no es un número hexadecimal válido."
                    )
                    return
        
        self.cpu.cargar_memoria(program_data)
        self.reset_processor()
        self.update_memory_table()

    def update_labels(self):
        """
        Actualiza las etiquetas de la GUI con los valores actuales de los
        registros del microprocesador.
        """
        self.ui.label_A.setText(f"{self.cpu.ACC_A.enable():02X}")
        self.ui.label_B.setText(f"{self.cpu.ACC_B.enable():02X}")
        self.ui.label_ALU.setText(f"{self.cpu.ALU.enable():02X}")
        self.ui.label_PC.setText(f"{self.cpu.PC.enable():02X}")
        self.ui.label_AR.setText(f"{self.cpu.AR.enable():02X}")
        self.ui.label_IR.setText(f"{self.cpu.IR.enable():02X}")
        
        # Asume que hay un registro de salida que se puede leer de la memoria
        self.ui.label_OUT.setText(f"{self.cpu.MEM.enable(0xff):02X}")
        
        self.ui.label_busc.setText(f"{self.cpu.busc:016b}")
        self.ui.label_busd.setText(f"{self.cpu.busd:02X}")

    def update_memory_table(self):
        """
        Actualiza la tabla de memoria en la GUI con los datos y nemónicos.
        """
        # Limpiar la tabla y establecer el número de filas
        self.ui.tableWidget.setRowCount(len(self.cpu.MEM.lista))
        
        # Llenar la tabla con los datos de la memoria
        for row, value in enumerate(self.cpu.MEM.lista):
            # Formato de la dirección y el dato en hexadecimal
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{row:02X}'))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{value:02X}'))
            
            # Decodificar el nemónico de la instrucción (asumiendo que uam1up.py lo tiene)
            instruction_hex = f'{value:02X}'
            mnemonic = self.cpu.nemonico.get(instruction_hex, "")
            
            # Llenar la columna de instrucción
            if mnemonic:
                # Si la instrucción es de 2 bytes, la siguiente celda se queda vacía
                if mnemonic.startswith("J") or mnemonic.startswith("LDA"): 
                    self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{mnemonic}'))
                    self.ui.tableWidget.item(row + 1, 2).setText("")
                else:
                    self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{mnemonic}'))
            else:
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
    
    def run_program(self):
        """
        Inicia la ejecución del programa, ya sea en modo continuo o por pasos.
        """
        # Si el procesador está detenido, lo reiniciamos
        if self.cpu.ex:
            self.reset_processor()
            return
            
        self.cpu.paso() # Ejecuta un solo paso de la microsecuencia
        self.update_labels()
        
        # Lógica para la ejecución continua
        if self.is_continuous_mode:
            # Si el procesador no está detenido, programamos el siguiente paso
            if not self.cpu.ex:
                QTimer.singleShot(50, self.run_program)