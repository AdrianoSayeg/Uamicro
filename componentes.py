class registro:
    def __init__(self, nombre):
        self.valor = 0x00 
    
    def enable(self):
        return self.valor
    
    def load(self, valor):
        self.valor = valor

class ALU:
    def __init__(self,valor=0x00):
        self.valor=valor
        
    def operar(self, A, B, Su):
        if Su==1:
            self.valor=A-B
        else:
            self.valor=A+B
            
    def enable(self):
        return self.valor

class pc:
    def __init__(self, nombre, size=0xff, valor=0x00):
        self.nombre = nombre
        self.valor = valor
        self.size = size+1 
    
    def enable(self,):
        return self.valor
        
    def clear(self):
        self.valor=0x00
        
    def incrementa(self):
        self.valor=(self.valor+1)%self.size

class MEM():
    def __init__(self, nombre, tamaño=0xff):
        self.lista=[0]*(tamaño+1) 
        self.nombre = nombre
    
    def enable(self,indice):
        return self.lista[indice]  
    
    def load(self,x):
        self.lista[x[0]]  = x[1] 
