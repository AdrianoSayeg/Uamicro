INICIO: LDA X
        ADD Y
        STA X
        LDA I
        SBB UNO
        STA I
        JAZ FIN
        JMP INICIO

FIN:    HLT
X:      0x01
Y:      0x02
I:      0X03
UNO:    0X01