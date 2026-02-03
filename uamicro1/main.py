import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from core.cpu import CPU
from memory.ram import RAM
from ensamblador.uamicro_asm import ensamblar

class SimuladorUAMICRO(QtWidgets.QMainWindow):
    def __init__(self):
        super(SimuladorUAMICRO, self).__init__()
        # Cargar la interfaz
        uic.loadUi('ui/ventana.ui', self) 
        
        # Inicializar el hardware
        self.ram = RAM()
        self.cpu = CPU(self.ram)
        
        # CONFIGURACIÓN UI
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.ejecutar_paso)
        
        self.tabla_memoria.blockSignals(True)
        self.configurar_tabla_memoria()
        self.tabla_memoria.blockSignals(False)
        
        # Conectar los botones
        self.btn_paso.clicked.connect(self.ejecutar_paso)
        self.btn_clear.clicked.connect(self.resetear_todo)
        self.btn_start.clicked.connect(self.toggle_corrido_automatico)
        self.btn_load.clicked.connect(self.cargar_archivo_txt)
        
        # Conectar la tabla
        self.tabla_memoria.cellChanged.connect(self.actualizar_ram_desde_tabla)

        self.actualizar_pantalla()
        

    def actualizar_pantalla(self):
        """Actualiza todos los labels con los valores actuales de la CPU"""
        regs = self.cpu.registers
        
        # Plantilla HTML para los labels
        def fmt_label(nombre, valor):
            return f"""
            <table width="100%" style="border: 2px solid #084B8A; background-color: #A9D0F5;">
                <tr><td align="center" style="font-size: 16px; color: #084B8A;">{nombre}</td></tr>
                <tr><td align="center" style="font-size: 8px; font-weight: bold; font-family: 'OCR A Extended';">{valor:02X}</td></tr>
            </table>
            """

        self.label_A.setText(fmt_label("ACC A", regs.ACC_A))
        self.label_B.setText(fmt_label("ACC B", regs.ACC_B))
        self.label_PC.setText(fmt_label("PC", regs.PC))
        self.label_AR.setText(fmt_label("AR", regs.AR))
        self.label_IR.setText(fmt_label("IR", regs.IR))
        
        self.label_bus_datos.setText(f"BUS DE DATOS Y DIRECCIONES (8 BITS): {self.cpu.phase:08b}")
        self.label_bus_control.setText(f"BUS DE CONTROL: {self.cpu.bus_control:016b}")
        
        # Registro de salida
        self.label_OUT.setText(f"{self.ram.read(0xFF):02X}")
        
        # Refrescar tabla 
        self.tabla_memoria.blockSignals(True)
        for i in range(256):
            valor=int(self.ram.read(i))
            self.tabla_memoria.item(i, 1).setText(f"{valor:02X}")
        self.tabla_memoria.blockSignals(False)
        # Obtener la dirección actual del PC
        pc_actual = self.cpu.registers.PC

        self.tabla_memoria.blockSignals(True)
        for i in range(256):
            item_dir = self.tabla_memoria.item(i, 0)
            item_val = self.tabla_memoria.item(i, 1)
            item_instr = self.tabla_memoria.item(i, 2)
            
            # Actualizar texto del valor
            item_val.setText(f"{self.ram.read(i):02X}")

            # Resaltar instruccion que se está ejecutando
            if i == pc_actual:
                # Color para la fila donde está el PC (Fondo amarillo, texto negro)
                item_dir.setBackground(QtGui.QColor("#F4D03F"))
                item_val.setBackground(QtGui.QColor("#F4D03F"))
                item_instr.setBackground(QtGui.QColor("#F4D03F"))
                item_dir.setForeground(QtGui.QColor("black"))
                item_val.setForeground(QtGui.QColor("black"))
                item_instr.setForeground(QtGui.QColor("black"))
            else:
                # Color normal (Fondo azul claro, texto azul oscuro)
                item_dir.setBackground(QtGui.QColor("#A9D0F5"))
                item_val.setBackground(QtGui.QColor("#A9D0F5"))
                item_instr.setBackground(QtGui.QColor("#A9D0F5"))
                item_dir.setForeground(QtGui.QColor("#084B8A"))
                item_val.setForeground(QtGui.QColor("#084B8A"))
                item_instr.setForeground(QtGui.QColor("#084B8A"))
                
        self.tabla_memoria.blockSignals(False)
    
    def actualizar_luces_control(self,clr=0):
        control = self.cpu.bus_control # Palabra de 16 bits
        
        # Diccionario que asocia el nombre del label con su posición en el bit
        mapeo_senales = {
            "WR": 0,  
            "VMA": 1, 
            "LM": 2, 
            "LIR": 3,
            "EAR": 4,
            "LAR": 5,
            "EPC": 6,
            "IPC": 7,
            "EB": 8,
            "LB": 9,
            "EU": 10,
            "SU": 11,
            "LA": 12,
            "EA": 13,

            "HLT": 15
        }

        estilo_encendido = "background-color: #00FF00; color: black; border: 1px solid white; font-weight: bold;" # Verde brillante
        estilo_apagado = "background-color: #2C3E50; color: #7F8C8D; border: 1px solid #34495E;" # Gris oscuro

        for nombre_label, bit in mapeo_senales.items():
            label_widget = getattr(self, nombre_label, None)
            if label_widget:
                if (control >> bit) & 1:
                    label_widget.setStyleSheet(estilo_encendido)
                else:
                    label_widget.setStyleSheet(estilo_apagado)
        if clr:
            self.CLR_PC.setStyleSheet(estilo_encendido)
            self.CLR_AR.setStyleSheet(estilo_encendido)
            self.CLR_IR.setStyleSheet(estilo_encendido)
        else:
            self.CLR_PC.setStyleSheet(estilo_apagado)
            self.CLR_AR.setStyleSheet(estilo_apagado)
            self.CLR_IR.setStyleSheet(estilo_apagado)

            
    def ejecutar_paso(self):
        if not self.cpu.halted:
            self.cpu.step()
            self.actualizar_pantalla()
            self.actualizar_luces_control()
        else:
            self.timer.stop()
            print("HLT detectado")

    def toggle_corrido_automatico(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_start.setText("START")
        else:
            self.timer.start(500) # 500ms por fase
            self.btn_start.setText("STOP")

    # Métodos de apoyo
    def configurar_tabla_memoria(self):
        self.tabla_memoria.setRowCount(256)
        self.tabla_memoria.setColumnCount(3)
        self.tabla_memoria.setHorizontalHeaderLabels(["Dir", "Valor", "Instrucción"])
        self.tabla_memoria.verticalHeader().setVisible(False)
        
        for i in range(256):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem("---" if j == 2 else "00" if j == 1 else f"{i:02X}")
                item.setFlags(QtCore.Qt.ItemIsEnabled) # Bloquea TODA la tabla
                self.tabla_memoria.setItem(i, j, item)
            
            
    def actualizar_ram_desde_tabla(self, fila, columna):
        if columna == 1:
            texto = self.tabla_memoria.item(fila, columna).text()
            try:
                self.ram.write(fila, int(texto, 16))
            except: pass

    def resetear_todo(self):
        self.cpu.registers.clr()
        self.cpu.phase = 0
        self.cpu.halted = False
        self.cpu.bus_control = 0x0
        self.ram.memory = [0] * 256
        self.btn_start.setText("START")
        self.actualizar_pantalla()
        self.actualizar_luces_control(1)
        self.timer.stop()
        

    def cargar_archivo_txt(self):
        opciones = QtWidgets.QFileDialog.Options()
        archivo, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Cargar Código Ensamblador", "", "Ensamblador (*.asm)")
        if archivo:
            try:
                # Leer el archivo
                with open(archivo, 'rt') as f:
                    programa = f.readlines()
                    lineas = [linea.strip() for linea in programa if linea.strip()]
                print(lineas)

                # Ensamblar el código
                bytecode, tabla_simbolos = ensamblar(lineas)
                
                # Cargar el bytecode en la RAM
                self.resetear_todo()
                for i, byte in enumerate(bytecode):
                    self.ram.write(i, byte)
                
                # Limpiar la columna de instrucciones
                for i in range(256):
                    self.tabla_memoria.item(i, 2).setText("")
                # Rellenar la columna de instrucciones
                cp=0
                for linea in programa:
                    l=linea.strip()
                    if not l:
                        continue
                    self.tabla_memoria.item(cp,2).setText(l)
                    tokens = l.split()
                    if any(t in ['LDA', 'LDB', 'STA', 'STB', 'ADD', 'SBB'] for t in tokens):
                        cp += 2
                    else:
                        cp += 1


                self.actualizar_pantalla()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error de Carga", f"Error al cargar el archivo: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = SimuladorUAMICRO()
    ventana.show()
    sys.exit(app.exec_())