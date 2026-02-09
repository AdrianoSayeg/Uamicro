        LDA MULTIPLICANDO 
        STA TEMP          
        LDA MULTIPLICADOR 
        STA I             
BUCLE:  LDA RESULTADO     
        ADD TEMP          
        STA RESULTADO     
        
        LDA I             
        SBB UNO           
        STA I             
        
        JAZ FIN           
        JMP BUCLE         
FIN:    HLT               
MULTIPLICANDO: 0x05
MULTIPLICADOR: 0x03
RESULTADO:     0x00
TEMP:          0x00
I:             0x00
UNO:           0x01
