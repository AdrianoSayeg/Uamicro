from componentes import registro,ALU,pc,MEM,control,nemonico
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from P1 import Ui_Form


class uamicro1(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.ejecutar)
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
        self.ex = 0
        self.cont = 0
        self.control= control
        self.nemonico=nemonico
        
    
    def actualizar_labels(self):
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
        for i in range(len(programa)):
            self.MEM.load([i, programa[i]])
        self.cont=0
        self.PC.clear()
        self.ex=0
        self.ui.tableWidget.setRowCount(len(self.MEM.lista))
        for row,x in enumerate(self.MEM.lista):
            self.ui.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(f'{x:02x}'))
        row=0
        while row+1< len(self.MEM.lista):
            x = self.MEM.lista[row]
            if f'{x:02x}' in self.nemonico:
                nemonico=self.nemonico[f'{x:02x}']
                if f'{x:02x}'[0]=='0':
                    row+=1
                    self.ui.tableWidget.setItem(row-1,1,QtWidgets.QTableWidgetItem(f'{nemonico} ({self.MEM.lista[row]:02X})'))
                else:
                    self.ui.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(f'{nemonico}'))
            row+=1
                                            

    def ejecutar(self):
        if self.ex:
            print('\nFIN DE EJECUCIÓN')
        else:
            self.actualizar_labels()
            print(f"\n=== Ciclo {self.cont} ===")
            self.busc=self.control[self.cont][f"{self.IR.enable():02x}"]
            self.ex,_,EA,LA,SU,EU,LB,EB,IPC,EPC,LAR,EAR,LIR,LM,VMA,WR= map(int, f'{self.busc:016b}')
            self.ALU.operar( self.ACC_A.enable(), self.ACC_B.enable(), SU)
            if EA:
                self.busd=self.ACC_A.enable()
            if EB:
                self.busd=self.ACC_B.enable()
            if EU:
                self.busd=self.ALU.enable()
            if EPC:
                self.busd=self.PC.enable()
            if EAR:
                self.busd=self.AR.enable()
            if VMA:
                if WR:
                    self.busd=self.MEM.enable(self.MAR.enable())
                else:
                    self.MEM.load([self.MAR.enable(),self.busd])
            if LA:
                self.ACC_A.load(self.busd)
            if LB:
                self.ACC_B.load(self.busd)
            if LAR:
                self.AR.load(self.busd)
            if LIR:
                self.IR.load(self.busd)
            if LM:
                self.MAR.load(self.busd)
            if IPC:
                self.PC.incrementa()
            
            print(self.busd)
            print(self.ex,_,EA,LA,SU,EU,LB,EB,IPC,EPC,LAR,EAR,LIR,LM,VMA,WR)
            print(f"Instruccion: {self.IR.enable():02x}")
            print(f"Resultado ALU: {self.ALU.enable()}")
            print(f"ACC_A: {self.ACC_A.enable()}, ACC_B: {self.ACC_B.enable()}")
            print(f"MAR: {self.MAR.enable()}, AR: {self.AR.enable()}")
            print(f"PC: {self.PC.enable()}, IR: {self.IR.enable()}")
            self.cont=(self.cont + 1) % 7
            QTimer.singleShot(50, self.ejecutar)