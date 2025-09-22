class Counter:
    def __init__(self, nombre, size=0xff):
        self.nombre = nombre
        self.valor = 0
        self.size = size + 1

    def enable(self):
        return self.valor

    def incrementa(self):
        self.valor = (self.valor + 1) % self.size

    def load(self, valor):
        self.valor = valor
    
    def clear(self):
        self.valor = 0


class UpDownCounter:
    def __init__(self, bits=4):
        self.valor = 0
        self.max = 2**bits

    def clr(self):
        self.valor = 0

    def pu(self):
        self.valor = (self.valor + 1) % self.max

    def pd(self):
        self.valor = (self.valor - 1) % self.max

class SC:
    def __init__(self, NumeroSC=15):
        self.contadores = [Counter("PC")] + [Counter(f"SC{i}") for i in range(NumeroSC)]
        self.updown = UpDownCounter(bits=4)

    def clear(self):
        self.updown.clr()
        for contador in self.contadores:
            contador.clear()

    def StackDemux(self, I=0, E=0, L=0, bus=None):
        """Aplica las señales al contador seleccionado por el UpDownCounter"""
        activo = self.contadores[self.updown.valor]
        bus_out = None

        if I:
            activo.incrementa()
        if L:
            activo.load(bus)
        if E:
            bus_out = activo.enable()

        return bus_out

class registro:
    def __init__(self, nombre):
        self.valor = 0x00 
    
    def enable(self):
        return self.valor
    
    def load(self, valor):
        self.valor = valor

class ACCA:
    def __init__(self):
        self.valor = 0

    def load(self, v):
        self.valor = v & 0xFFF

    def enable(self):
        return self.valor

    def aminus(self):
        # bit 11 = signo
        return self.valor>>11 

    def azero(self):
        return int(not(self.valor or 0x0))

class MEM:
    def __init__(self, size=256):
        self.mem = [0] * size

    def access(self, addr, data=None, wr=0): 
        if wr == 1:  # read
            return self.mem[addr]
        elif wr == 0:  # write
            self.mem[addr] = data
            return None

class IR:
    def __init__(self):
        self.valor = 0

    def load(self, v):
        self.valor = v

    def enable(self):
        return self.valor & 0xFF

    def decode(self):
        op = (self.valor >> 8)     # opcode 4 bits
        rest = self.valor & 0xFF         # 8 bits bajos

        # Ejemplo básico de clasificación
        if op == 0xF:
            op1=rest>>4
            mnem={
                0x0:"NOP",
                0X1:"CLA",
                0x2:"XCH",
                0X3:"DEX",
                0x4:"INX",
                0X5:"CMA",
                0x6:"CMB",
                0X7:"IOR",
                0x8:"AND",
                0X9:"NOR",
                0xA:"NAN",
                0XB:"XOR",
                0xC:"RTS",
                0XD:"INP",
                0xE:"OUT",
                0XF:"HLT"
            }
            return (mnem[op1])
        else:
            mnem={
                0x0:"LDA",
                0X1:"ADD",
                0x2:"SUB",
                0X3:"STA",
                0x4:"LDB",
                0X5:"LDX",
                0x6:"JMP",
                0X7:"JAM",
                0x8:"JAZ",
                0X9:"JIM",
                0xA:"JIZ",
                0XB:"JMS",
                0xC:"LXA",
                0XD:"SXA",
                0xE:"AAB",
            }
            return (mnem[op])

class IndexRegister:
    def __init__(self):
        self.value = 0  

    def inx(self):
        self.value = (self.value + 1) 

    def dex(self):
        self.value = (self.value - 1)

    def sx(self, xx):
        self.value = (self.value + xx) 

    def lx(self, data):
        self.value = data

    def ex(self):
        return self.value

class IntRegister:
    def __init__(self):
        self.value = 0

    def load(self, addr):
        self.value = addr

    def eint(self):
        return self.value

class InputRegister:
    def __init__(self):
        self.value = 0

    def strobe(self, external_data):
        self.value = external_data

    def ein(self):
        return self.value

class OutputRegister:
    def __init__(self):
        self.value = 0

    def l_o(self, bus):
        self.value = bus & 0xFF

class ALU:
    def __init__(self,valor=0x00):
        self.valor=valor
        
    def operar(self, A, B, S0, S1, S2, S3):
        # convertir selectores a un número de 4 bits
        sel = (S3 << 3) | (S2 << 2) | (S1 << 1) | S0

        if sel == 0b0000:   # NOP
            self.valor = A
        elif sel == 0b0001: # ADD
            self.valor = A + B
        elif sel == 0b0010: # SUB
            self.valor = A - B
        elif sel == 0b0011: # CMA (complemento de A)
            self.valor = ~A
        elif sel == 0b0100: # CMB (complemento de B)
            self.valor = ~B
        elif sel == 0b0101: # IOR (A OR B)
            self.valor = A | B
        elif sel == 0b0110: # AND (A AND B)
            self.valor = A & B
        elif sel == 0b0111: # NOR (A NOR B)
            self.valor = ~(A | B)
        elif sel == 0b1000: # NAND (A NAND B)
            self.valor = ~(A & B)
        elif sel == 0b1001: # XOR (A XOR B)
            self.valor = A ^ B
        elif sel == 0b1010: # CLA (clear A → 0)
            self.valor = 0
        else:
            self.valor = 0  # por seguridad
            
    def enable(self):
        return self.valor

class ControlUnit:
    def __init__(self):
        self.signals_out = [
            "LM",
            "CS","WR","CLR",
            "LAR","EAR",
            "Pu","Pd","Lk","Ik","Ek",
            "Lir","Eir",
            "Eint",
            "LA","EA",
            "EU","S0","S1","S2","S3","S4",
            "LB",
            "Sx","Lx","INx","DEx","Ex",
            "Lin","Ein",
            "Lrio",
            "Lo",
        ]
        
        # Microsecuencias de ejecución (sin fetch, porque es fijo)
        self.control = {
            # LDA XX   A <- (XX)
            "LDA": {
                2: ["Eir","LM"],
                3: ["CS","WR","LA"]
            },
            # ADD XX   A <- A + (XX)
            "ADD": {
                2: ["Eir","LM","S0"],
                3: ["CS","LB"],
                4: ["EU","LA","S0"]
            },
            # SUB XX   A <- A - (XX)
            "SUB": {
                2: ["Eir","LM","S1"],
                3: ["CS","LB"],
                4: ["EU","LA","S1"]
            },
            # STA XX   (XX) <- A
            "STA": {
                2: ["Eir","LM"],
                3: ["EA","CS"],
            },
            # LDB XX   B <- (XX)
            "LDB": {
                2: ["Eir","LM"],
                3: ["CS","WR","LB"]
            },
            # LDX XX   X <- (XX)
            "LDX": {
                2: ["Eir","LM"],
                3: ["CS","WR","Lx"]
            },
            # JMP XX   PC <- XX
            "JMP": {
                2: ["Eir","Lk"],
            },
            # JAM XX   PC <- XX if A < 0
            "JAM": {
                2: ["Eir","Lk"],
            },
            # JAZ XX   PC <- XX if A == 0
            "JAZ": {
                2: ["Eir","Lk"],
            },
            # JIM XX   PC <- XX if X < 0
            "JIM": {
                2: ["Eir","Lk"],
            },
            # JIZ XX   PC <- XX if X == 0
            "JIZ": {
                2: ["Eir","Lk"],
            },
            # JMS XX   subroutine jump
            "JMS": {
                2: ["Pu"],
                3: ["Eir","Lk"]
            },
            # CLA      A <- 0
            "CLA": {
                2: ["EU","LA","S3","S2"]
            },
            # CMA      A <- ~A
            "CMA": {
                2: ["EU","LA","S1","S0"]
            },
            # CMB      B <- ~B
            "CMB": {
                2: ["EU","LB","S2"]
            },
            # IOR      A <- A OR B
            "IOR": {
                2: ["EU","LA","S2","S0"]
            },
            # AND      A <- A AND B
            "AND": {
                2: ["EU","LA","S2","S1"]
            },
            # NOR      A <- ~(A OR B)
            "NOR": {
                2: ["EU","LA","S2","S1","S0"]
            },
            # NAND     A <- ~(A AND B)
            "NAN": {
                2: ["EU","LA","S3"]
            },
            # XOR      A <- A XOR B
            "XOR": {
                2: ["EU","LA","S3","S0"]
            },
            # RTS      return
            "RTS": {
                2: ["Pd"]
            },
            # XCH      intercambia A <-> X
            "XCH": {
                2: ["EA","LAR"],
                3: ["Ex","LA"],
                4: ["EAR","Lx"]
            },
            # DEX
            "DEX": {
                2: ["DEX"]
            },
            # INX
            "INX": {
                2: ["INX"]
            },
            # LXA XX   A <- (X + XX)
            "LXA": {
                2: ["Eir","LA"],
                3: ["Ex","LB","Sx"],
                4: ["EA","LM"],
                5: ["CS","LA"]
            },
            # SXA XX   (X+XX) <- A
            "SXA": {
                2: ["EA","LAR"],
                3: ["Eir","LA"],
                4: ["Ex","LB","Sx"],
                5: ["EA","LM"]
            },
            # INP
            "INP": {
                2: ["Lin"],
                3: ["Ein","LA"]
            },
            # OUT
            "OUT": {
                2: ["EA","Lo"]
            },
            
            # AAB A <- A + B
            "AAB": {
                2: ["EU","S0","LA"]
            },
        }

    def check_condition(self, instr, flags):
        """Evalúa condiciones para saltos"""
        if instr == "JMP":
            return True
        elif instr == "JAM":
            return flags.get("Am",0) == 1
        elif instr == "JAZ":
            return flags.get("Az",0) == 1
        elif instr == "JIM":
            return flags.get("Xm",0) == 1
        elif instr == "JIZ":
            return flags.get("Xz",0) == 1
        elif instr == "JMS":
            return True
        return True

    def get_signals(self, instr, ciclo, flags):
        """
        Obtiene señales de control para ciclo.
        ciclos 0 y 1 -> FETCH fijo
        resto -> depende de la instrucción
        """
        if ciclo == 0:
            return ["Ek","LM"]
        elif ciclo == 1:
            return ["CS","WR","Lir","Ik"]

        señales = self.control.get(instr, {}).get(ciclo, [])

        if instr.startswith("J"):
            if self.check_condition(instr, flags):
                return señales 
            else: 
                return []

        return señales

