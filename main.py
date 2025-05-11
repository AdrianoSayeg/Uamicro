from componentes import registro,ALU,pc,MEM
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from P1 import Ui_Form


class uamicro1(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ACC_A = registro("ACC_A")
        self.ACC_B = registro("ACC_B")
        self.PC = pc("PC")
        self.ALU = ALU()
        self.MAR = registro("MAR")
        self.AR = registro("AR")
        self.MEM = MEM("MEM")
        self.IR = registro("IR")
        self.busc = 0x0
        self.busd = 0x0
        self.su = 0
        self.ex = 1
        self.cont = 0
        self.instruccion=0x00
    
    def actualizar_labels(self):
        self.ui.label_A.setText(f"{self.ACC_A.enable():02x}")
        self.ui.label_B.setText(f"{self.ACC_B.enable():02x}")
        self.ui.label_ALU.setText(f"{self.ALU.enable():02x}")
        self.ui.label_PC.setText(f"{self.PC.enable():02x}")
        self.ui.label_AR.setText(f"{self.AR.enable():02x}")
        self.ui.label_IR.setText(f"{self.IR.enable():02x}")
        self.ui.label_OUT.setText(f"{self.MEM.enable(0xff):02x}") 
        
    def cargar_memoria(self, programa):
        for i in range(len(programa)):
            self.MEM.load([i, programa[i]])
        self.PC.clear()
    
    def HLT(self, x):
        self.ex = 0
    
    def pasar(self, x):
        pass
    
    def control(self, estado, instruccion):
        acc = {0: self.ACC_A, 1: self.ACC_B}
        control = {
            2: {
                f'{i}{j}': [self.HLT, None, 0, 0x1000] if f'{i}{j}' == 'f4'
                else [self.MAR.load, self.PC.enable(), 0, 0x44] if i == '0'
                else [acc[j%2].load, self.ALU.enable(), 1 if j >= 2 else 1, 0x400] 
                for i in ['0','f'] for j in range(6)
            },
            3: {
                f'{i}{j}': [self.AR.load, self.MEM.enable(self.MAR.enable()), 0, 0xa3] if i == '0'
                else [self.pasar, None, 0, 0x0] 
                for i in ['0','f'] for j in range(6)
            },
            4: {
                f'{i}{j}': [self.MAR.load, self.AR.enable(), 0, 0x14] if i == '0'
                else [self.pasar, None, 0, 0x0] 
                for i in ['0','f'] for j in range(6)
            },
            5: {
                f'{i}{j}': [acc[j%2].load, self.MEM.enable(self.MAR.enable()), 0, 0x3] if i == '0' and (j == 0 or j == 1)
                else [self.MEM.load, [self.MAR.enable(), acc[j%2].enable()], 0, 0x2] if i == '0' and (j == 2 or j == 3)
                else [self.ACC_B.load, self.MEM.enable(self.MAR.enable()), 0, 0x203] if i == '0' and (j == 4 or j == 5)
                else [self.pasar, None, 0, 0x0] 
                for i in ['0','f'] for j in range(6)
            },                 
            6: {
                f'{i}{j}': [self.ACC_A.load, self.ALU.enable(), 1 if j == 5 else 0, 0x0] if (j == 4 or j == 5)
                else [self.pasar, None, 0, 0x0] 
                for i in ['0','f'] for j in range(6)
            }
        }
        
        decode = control[estado][instruccion]
        
        # 1. Configurar todas las señales PRIMERO
        self.busd = decode[1]
        self.busc = decode[3]
        
        
        # 4. Ejecutar acción final
        decode[0](decode[1])
        
        # Debugging detallado
        print(decode[0],decode[1])
        print(f"Instrucción: {instruccion}")
        print(f"Resultado ALU: {self.ALU.enable()}")
        print(f"ACC_A: {self.ACC_A.enable()}, ACC_B: {self.ACC_B.enable()}")
        print(f"MAR: {self.MAR.enable()}, AR: {self.AR.enable()}")
        print(f"PC: {self.PC.enable()}, IR: {self.IR.enable()}")
    

        
    def ejecutar(self):

        if self.ex:
            self.actualizar_labels()
            print(f"\n=== Ciclo {self.cont} ===")
            
            # FETCH
            if self.cont == 0:
                self.MAR.load(self.PC.enable())
                self.busc = 0x44
                self.busd = self.PC.enable()
                print("FETCH: Cargando dirección de PC en MAR")
                print(self.PC.enable(),self.MAR.enable())
            elif self.cont == 1:                 
                self.PC.incrementa()
                mem_out = self.MEM.enable(self.MAR.enable())
                self.IR.load(mem_out)
                self.instruccion = f'{self.IR.enable():02x}'
                print(f"FETCH: Instrucción leída: {self.instruccion}")
                self.busc = 0x8a
                self.busd = mem_out
            
            # EXECUTE
            else:
                print(f"{self.cont},i:{self.instruccion}")
                if (self.cont==2 and self.instruccion[1] in ("2","3")) or (self.cont==6 and self.instruccion[1]=="5") :
                    self.ALU.operar( self.ACC_A.enable(), self.ACC_B.enable(), 1)
                else:
                    self.ALU.operar( self.ACC_A.enable(), self.ACC_B.enable(), 0)
                if self.cont == 3 and self.instruccion[0] == '0':
                    self.PC.incrementa()
                    print("EXECUTE: Incrementando PC adicional")
                self.control(self.cont, self.instruccion) 
            
            self.cont = (self.cont + 1) % 7
            QTimer.singleShot(500, self.ejecutar)
        else:   
            print('\nFIN DE EJECUCIÓN')