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
        # Matriz de Control (Microprogramación de la UAMICRO I)
        # Señales (16 bits): [HLT, -, EA, LA, SU, EU, LB, EB, IPC, EPC, LAR, EAR, LIR, LM, VMA, WR]
        # NOTA: WR=0 es Lectura, WR=1 es Escritura
        self.control_matrix = {
            # FETCH
            # T0: EPC=1, LM=1
            0: {f'{i:02x}': 0x0044 for i in range(256)},
            
            # T1: LIR=1, VMA=1, IPC=1, WR=0
            1: {f'{i:02x}': 0x008A for i in range(256)},

            # EXECUTE
            # T2:
            2: {
                'f6': 0x8000, # HLT
                'f0': 0x1400, # ADA: EU + LA
                'f1': 0x0600, # ADB: EU + LB
                'f2': 0x1C00, # SUA: EU + SU + LA
                'f3': 0x1E00, # SUB: EU + SU + LB
                **{f'0{j:x}': 0x0044 for j in range(6)} # MRI: EPC + LM
            },
            # T3: Leer operando (VMA + LAR + IPC + WR=0)
            3: {
                '00': 0x00A2, '01': 0x00A2, '02': 0x00A2, 
                '03': 0x00A2, '04': 0x00A2, '05': 0x00A2 
            },
            # T4: Mover operando de AR al MAR (EAR + LM)
            4: {
                '00': 0x0014, '01': 0x0014, '02': 0x0014, 
                '03': 0x0014, '04': 0x0014, '05': 0x0014
            },
            # T5:
            5: {
                '00': 0x1002, # LDA: LA + VMA 
                '01': 0x0202, # LDB: LB + VMA 
                '02': 0x2003, # STA: EA + VMA + WR=1 
                '03': 0x0103, # STB: EB + VMA + WR=1
                '04': 0x0202, # ADD: Trae dato a B 
                '05': 0x0202  # SBB: Trae dato a B 
            },
            # T6: Operación aritmética final
            6: {
                '04': 0x1400, # ADD Final: A + B -> A (EU + LA)
                '05': 0x1C00  # SBB Final: A - B -> A (EU + SU + LA)
            }
        }

    def step(self):
        """Avanza una fase de tiempo (T0-T6) del procesador."""
        if self.halted:
            return
        # print('RAM:', self.memory.memory[self.registers.PC])
        # Decodificación: Obtener opcode y palabra de control
        
        opcode_hex = f"{self.registers.IR:02x}"
        #print(f"--- Decodificando Instrucción: OpCode {opcode_hex.upper()} en Fase T{self.phase} ---")
        word = self.control_matrix.get(self.phase, {}).get(opcode_hex, 0)
        self.bus_control = word
        #print(f"Palabra de Control Obtenida: {word:016b} (Hex: {word:04X})")

        # Desempaquetado de señales (Bus de Control de 16 bits)
        signals = [int(bit) for bit in f'{word:016b}']
        (hlt, _, ea, la, su, eu, lb, eb, ipc, epc, lar, ear, lir, lm, vma, wr) = signals
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
        elif vma and not wr: # WR=0: Leer de Memoria [cite: 453]
            self.bus_data = self.memory.read(self.registers.MAR)

        # Leer bus (Varios componentes pueden recibir)
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