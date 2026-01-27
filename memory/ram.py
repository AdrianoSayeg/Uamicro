class RAM():
    def __init__(self):
        # Memoria con espacio de 256 bytes
        self.memory = [0] * 256
    
    def read(self, address):
        # Leer un byte de la memoria en la dirección especificada
        return self.memory[address]
    
    def write(self, address, value):
        # Escribir un byte en la memoria en la dirección especificada
        self.memory[address] = value