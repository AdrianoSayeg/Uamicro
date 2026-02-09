; --- INICIALIZACIÓN ---
        LDA MULTIPLICANDO ; Carga 5 en A
        STA TEMP          ; Lo guarda para usarlo en cada suma
        LDA MULTIPLICADOR ; Carga 3 (contador de vueltas)
        STA I             ; I = 3

; --- BUCLE DE SUMA ---
BUCLE:  LDA RESULTADO     ; Trae lo que llevamos sumado
        ADD TEMP          ; Le suma el multiplicando
        STA RESULTADO     ; Guarda el nuevo total
        
        LDA I             ; Carga el contador
        SBB UNO           ; I = I - 1
        STA I             ; Actualiza contador
        
        JAZ FIN           ; Si I llegó a 0, terminamos
        JMP BUCLE         ; Si no, otra vuelta

; --- FINAL ---
FIN:    HLT               ; Resultado final estará en 'RESULTADO'

; --- DATOS (RAM) ---
MULTIPLICANDO: 0x05
MULTIPLICADOR: 0x03
RESULTADO:     0x00
I:             0x00
UNO:           0x01