from componentes import registro, ALU, pc, MEM, control, nemonico

class Microprocesador:
    def __init__(self):
        self.ACC_A = registro("ACC_A")
        self.ACC_B = registro("ACC_B")
        self.PC = pc("PC")
        self.ALU = ALU()
        self.MAR = registro("MAR")
        self.AR = registro("AR")
        self.MEM = MEM("MEM")
        self.IR = registro("IR")
        self.control = control
        self.busc = 0x0
        self.busd = 0x0
        self.ex = 0
        self.cont = 0
        self.nemonico = nemonico

    def reiniciar(self):
        self.PC.clear()
        self.cont = 0
        self.ex = 0

    def cargar_memoria(self, programa):
        for i, instruccion in enumerate(programa):
            self.MEM.load([i, instruccion])

    def paso(self):
        if self.ex:
            return

        self.busc = self.control[self.cont][f"{self.IR.enable():02x}"]
        self.ex, _, EA, LA, SU, EU, LB, EB, IPC, EPC, LAR, EAR, LIR, LM, VMA, WR = map(int, f'{self.busc:016b}')
        self.ALU.operar(self.ACC_A.enable(), self.ACC_B.enable(), SU)

        if EA: self.busd = self.ACC_A.enable()
        if EB: self.busd = self.ACC_B.enable()
        if EU: self.busd = self.ALU.enable()
        if EPC: self.busd = self.PC.enable()
        if EAR: self.busd = self.AR.enable()

        if VMA:
            if WR:
                self.busd = self.MEM.enable(self.MAR.enable())
            else:
                self.MEM.load([self.MAR.enable(), self.busd])

        if LA: self.ACC_A.load(self.busd)
        if LB: self.ACC_B.load(self.busd)
        if LAR: self.AR.load(self.busd)
        if LIR: self.IR.load(self.busd)
        if LM: self.MAR.load(self.busd)
        if IPC: self.PC.incrementa()

        self.cont = (self.cont + 1) % 7

