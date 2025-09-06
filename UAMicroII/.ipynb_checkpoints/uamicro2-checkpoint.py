from componentes2 import SC,registro,ACCA,MEM,IR,IndexRegister,IntRegister,InputRegister,OutputRegister,ALU,ControlUnit


class Microprocesador:
    def __init__(self):
        # Registros
        self.ACC_A = ACCA()
        self.ACC_B = registro("ACC_B")
        self.SC = SC()       # Program Counter
        self.AR = registro("AR")      # Address Register
        self.MAR = registro("MAR")    # Memory Address Register
        self.IR = IR()                # Instruction Register
        self.X=IndexRegister()

        # Componentes
        self.ALU = ALU()
        self.MEM = MEM(size=256)
        self.control = ControlUnit()

        # Estado
        self.bus = 0
        self.ciclo = 0
        self.instr_actual = ""
        self.halted = False   # <- flag de paro

        # Banderas (para saltos condicionales)
        self.flags = {"Am":0,"Az":0,"Xm":0,"Xz":0}

    def reiniciar(self):
        """Reinicia completamente el procesador"""
        print('Reiniciando microprocesador...')
        self.SC.clear()
        self.ACC_A.load(0)
        self.ACC_B.load(0)
        self.AR.load(0)
        self.MAR.load(0)
        self.IR.load(0)
        self.X.lx(0)
        self.bus = 0
        self.ciclo = 0
        self.instr_actual = ""
        self.halted = False
        self.flags = {"Am": 0, "Az": 0, "Xm": 0, "Xz": 0}


    def cargar_memoria(self, programa):
        for i, instruccion in enumerate(programa):
            self.MEM.access(i, instruccion, wr=0)  # write en MEM
    
    def correr(self, programa):
        self.reiniciar()
        self.cargar_memoria(programa)
        self.halted = False
        while not(self.halted):
        #for i in range(50):
            self.paso()

    def paso(self):
        self.instr_actual=self.IR.decode()
        #print(self.instr_actual,self.SC.StackDemux( I=0, E=1, L=0, bus=None))
        #print(f'{self.IR.valor:04X}:{self.IR.enable():04X}')
        
        # Actualizar flags
        self.flags["Am"] = self.ACC_A.aminus()
        self.flags["Az"] = self.ACC_A.azero()
        self.flags["Xm"] = int(self.X.ex() >> 11)
        self.flags["Xz"] = int(self.X.ex() == 0)
        #if self.flags["Xz"]:print(f'{self.IR.valor:04X}:{self.IR.enable():04X}')
        # señales para este ciclo
        señales = self.control.get_signals(self.instr_actual, self.ciclo, self.flags)
        #print(señales)

        # --- Etapa de ejecución de señales ---

        # Operaciones de la ALU (usando selectores S0..S3 si están en señales)
        s0 = 1 if "S0" in señales else 0
        s1 = 1 if "S1" in señales else 0
        s2 = 1 if "S2" in señales else 0
        s3 = 1 if "S3" in señales else 0
        if "EU" in señales:  # sólo calculo si se usa la ALU
            self.ALU.operar(self.ACC_A.enable(), self.ACC_B.enable(), s0,s1,s2,s3)

        # Enables
        if "EA" in señales: self.bus = self.ACC_A.enable()
        if "EB" in señales: self.bus = self.ACC_B.enable()
        if "EU" in señales: self.bus = self.ALU.enable()
        if "Ek" in señales: self.bus = self.SC.StackDemux( I=0, E=1, L=0, bus=self.bus)     # PC→bus
        if "EAR" in señales: self.bus = self.AR.enable()
        if "Eir" in señales: self.bus = self.IR.enable()
        if "Ex" in señales: self.bus = self.X.ex()
        if "Ein" in señales: self.bus = self.Input.ein()
        
        # Memoria
        if "CS" in señales:
            if "WR" in señales:   # lectura
                self.bus = self.MEM.access(self.MAR.enable(), wr=1)
            else:                 # escritura
                self.MEM.access(self.MAR.enable(), data=self.bus, wr=0)
        
        # Loads
        if "LA" in señales: self.ACC_A.load(self.bus)
        if "LB" in señales: self.ACC_B.load(self.bus)
        if "LAR" in señales: self.AR.load(self.bus)
        if "Lir" in señales: self.IR.load(self.bus)
        if "LM" in señales: self.MAR.load(self.bus)
        if "Lx" in señales: self.X.lx(self.bus)
        if "Lo" in señales: print("Lo: ",self.bus)
        if "Lk" in señales: self.SC.StackDemux(I=0, E=0, L=1, bus=self.bus) 
        
        # PC
        if "Pu" in señales: self.SC.updown.pu()
        if "Pd" in señales: self.SC.updown.pd()
        if "Ik" in señales: self.SC.StackDemux(I=1, E=0, L=0, bus=self.bus)

        #index
        if "DEX" in señales: self.X.dex()
        if "INX" in señales: self.X.inx()
        #print(self.X.ex())

        # --- Avanzar ciclo ---
        self.ciclo += 1
        
        # Si terminamos microsecuencia, reiniciar a fetch
        if self.ciclo > max(self.control.control.get(self.instr_actual, {0:[]}).keys(), default=1):
            # fetch siempre empieza en ciclo 0
            self.ciclo = 0

        if self.instr_actual=="HLT":
            self.halted =True
            return

