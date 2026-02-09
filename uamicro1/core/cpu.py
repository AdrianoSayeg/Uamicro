from core.registers import Registers
from core.alu import ALU

class CPU:
    def __init__(self, memory):
        # Hardware Interno del Microprocesador
        self.registers = Registers()
        self.alu = ALU()
        self.memory = memory 
        
        # Estado del Sistema
        self.halted = False
        self.phase = 0
        self.bus_data = 0x0 # Bus de datos de 8 bits
        self.bus_control = 0x0 # Bus de control de 16 bits
        # Señales (16 bits): [HLT, -, EA, LA, SU, EU, LB, EB, IPC, EPC, LAR, EAR, LIR, LM, VMA, WR]
        HLT=0x8000
        LPC=0x4000
        EA =0x2000
        LA =0x1000
        SU =0x0800
        EU =0x0400
        LB =0x0200
        EB =0x0100
        IPC=0x0080
        EPC=0x0040
        LAR=0x0020
        EAR=0x0010
        LIR=0x0008
        LM =0x0004
        VMA=0x0002
        WR =0x0001
        
        self.control_matrix = {
            # FETCH
            # T0: EPC=1, LM=1
            0: {f'{i:02x}': EPC|LM for i in range(256)},
            
            # T1: LIR=1, VMA=1, IPC=1, WR=0
            1: {f'{i:02x}': LIR|VMA|IPC for i in range(256)},

            # EXECUTE
            # T2:
            2: {
                'f6': HLT, # HLT
                'f0': EU|LA, # ADA: EU + LA
                'f1': EU|LB, # ADB: EU + LB
                'f2': EU|SU|LA, # SUA: EU + SU + LA
                'f3': EU|SU|LB, # SUB: EU + SU + LB
                **{f'0{j:x}': EPC|LM for j in range(8)} # MRI: EPC + LM
            },
            # T3: Leer operando (VMA + LAR + IPC + WR=0)
            3: {
                **{f'0{j:x}': VMA|LAR|IPC for j in range(8)} # VMA + LAR + IPC (Leer XX)
            },
            # T4: Mover operando de AR al MAR (EAR + LM)
            4: {
                **{f'0{j:x}': EAR|LM for j in range(6)},
                '06':LPC|EAR, # JMP: LPC + EAR
                '07':LPC|EAR  # JAZ: LPC + EAR si ACC_A == 0
            },
            # T5:
            5: {
                '00': LA|VMA, # LDA: LA + VMA 
                '01': LB|VMA, # LDB: LB + VMA 
                '02': EA|VMA|WR, # STA: EA + VMA + WR=1 
                '03': EB|VMA|WR, # STB: EB + VMA + WR=1
                '04': LB|VMA, # ADD: Trae dato a B 
                '05': LB|VMA  # SBB: Trae dato a B 
            },
            # T6: Operación aritmética final
            6: {
                '04': EU|LA, # ADD Final: A + B -> A (EU + LA)
                '05': EU|SU|LA  # SBB Final: A - B -> A (EU + SU + LA)
            }
        }

    def step(self):
        """Avanza una fase de tiempo (T0-T6) del procesador."""
        if self.halted:
            return
        # print('RAM:', self.memory.memory[self.registers.PC])
        # Decodificación: Obtener opcode y palabra de control
        
        opcode_hex = f"{self.registers.IR:02x}"
        #print(f"Decodificando Instrucción: OpCode {opcode_hex.upper()} en Fase T{self.phase} ---")
        word = self.control_matrix.get(self.phase, {}).get(opcode_hex, 0)
        if opcode_hex == '07' and self.phase==4:
            #print(f"JAZ: Evaluando condición ACC_A={self.registers.ACC_A}") 
            if self.registers.ACC_A != 0: 
                word = 0x0000
        self.bus_control = word
        #print(f"Palabra de Control Obtenida: {word:016b} (Hex: {word:04X})")

        # Desempaquetado de señales (Bus de Control de 16 bits)
        signals = [int(bit) for bit in f'{word:016b}']
        (hlt, lpc, ea, la, su, eu, lb, eb, ipc, epc, lar, ear, lir, lm, vma, wr) = signals
        #print(f"Señales de Control: HLT={hlt}, EA={ea}, LA={la}, SU={su}, EU={eu}, LB={lb}, EB={eb}, IPC={ipc}, EPC={epc}, LAR={lar}, EAR={ear}, LIR={lir}, LM={lm}, VMA={vma}, WR={wr}")
        if hlt:
            self.halted = True
            #print("UAMICRO I: HLT Detectado. Ejecución finalizada.")
            return

        # Escribir bus de datos (Solo un componente pone datos)
        if ea:    self.bus_data = self.registers.ACC_A
        elif eb:  self.bus_data = self.registers.ACC_B
        elif epc: self.bus_data = self.registers.PC
        elif ear: self.bus_data = self.registers.AR
        elif eu:  self.bus_data = self.alu.execute(self.registers.ACC_A, self.registers.ACC_B, su)
        elif vma and not wr: # WR=0: Leer de Memoria
            self.bus_data = self.memory.read(self.registers.MAR)

        # Leer bus (Varios componentes pueden recibir)
        if lpc: self.registers.PC = self.bus_data
        if la:  self.registers.ACC_A = self.bus_data
        if lb:  self.registers.ACC_B = self.bus_data
        if lar: self.registers.AR = self.bus_data
        if lir: self.registers.IR = self.bus_data
        if lm:  self.registers.MAR = self.bus_data
        if ipc: self.registers.PC = (self.registers.PC + 1) % 256
        
        # Escritura en memoria (VMA + WR=1)
        if vma and wr:
            self.memory.write(self.registers.MAR, self.bus_data)

        # Avanzar Ring Counter
        self.phase = (self.phase + 1) % 7