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

control= {
#FETCH
    0:{
        f'{i}{j}':0x44 for i in ['0','f'] for j in range(6)                  
    },
    1:{
        f'{i}{j}':0x8b for i in ['0','f'] for j in range(6)                   
    },
    #EXECUTE
    2: {
        f'{i}{j}': 0x8000 if f'{i}{j}' == 'f4'
        else 0x44 if i == '0'
        else 0x1400 if f'{i}{j}'=="f0"
        else 0x600 if f'{i}{j}'=="f1"
        else 0x1c00 if f'{i}{j}'=="f2"
        else 0x1e00 if f'{i}{j}'=="f3"
        else 0x0
        for i in ['0','f'] for j in range(6)
    },
    3: {
        f'{i}{j}': 0xa3 if i == '0'
        else 0x0 
        for i in ['0','f'] for j in range(6)
    },
    4: {
        f'{i}{j}': 0x14 if i == '0'
        else 0x0 
        for i in ['0','f'] for j in range(6)
    },
    5: {
        f'{i}{j}': 0x3+0x1000*(1-j)+0x200*j if f'{i}{j}' in ('00','01')
        else 0x2+0x2000*(3-j)+0x100*(j-2) if f'{i}{j}' in ('02','03')
        else 0x203 if f'{i}{j}' in ('04','05')
        else 0x0 
        for i in ['0','f'] for j in range(6)
    },                
    6: {
        f'{i}{j}': 0x1400+0x800*(j//2) if f'{i}{j}' in ('04','05')
        else 0x0 
        for i in ['0','f'] for j in range(6)
    }
}
