class Registers:
    def __init__(self):
        self.clr()

    def clr(self):
        # Acumuladores A y B 
        self.ACC_A = 0
        self.ACC_B = 0 
        
        # Program Counter (P.C.)
        self.PC = 0
        # Instruction Register (I.R.) 
        self.IR = 0

        # Memory Address Register (M.A.R.) 
        self.MAR = 0
        # Registro Auxiliar (A.R.)
        self.AR = 0