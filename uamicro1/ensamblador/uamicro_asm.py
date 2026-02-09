#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 14:23:15 2026

@author: Gabriel Adriano Sayeg De Luca
@author: OScar Yáñez Suárez
"""

import sys
"""
# Revisa argumentos de llamada
if len(sys.argv) != 2:
    print('ERROR: No se indica archivo para procesar')
    exit(0)
    
# Intenta leer el archivo en ensamblador
try:
    # Lee el archivo de programa
    with open(sys.argv[1], 'rt') as f:
        programa = f.readlines()
    # Remueve whitespace
    programa = [linea.strip() for linea in programa if linea != '']
except FileNotFoundError:
    print(f'ERROR: No se encuentra el archivo {sys.argv[1]}')
    exit(0)
"""
def ensamblar(programa):
    # Códigos de operación de la Uamicro I
    UAMicroI_Opcodes = {'LDA': 0x00, 'LDB': 0x01, 'STA': 0x02, 'STB': 0x03, 'ADD': 0x04, 'SBB': 0x05, 
                        'JMP': 0x06, 'JAZ': 0x07,
                        'ADA': 0xF0, 'ADB': 0xF1, 'SUA': 0xF2, 'SUB': 0xF3, 'HLT': 0xF6} 

    #### Paso 1

    # Inicializa la cadena del código ensamblado
    bytecode = bytearray()
    # Inicializa tabla de símbolos
    tabla_simbolos = dict()
    # Inicializa el contador de programa
    contador_de_programa = 0x00

    # Procesa cada linea
    for linea in programa:
        # Separa los tokens de la linea
        tokens = linea.split()
        # Procesa los tokens
        if len(tokens) == 3 and ':' in tokens[0] and tokens[1] in UAMicroI_Opcodes:
            # Caso - etiqueta: opcode dir
            etiqueta = tokens[0][:-1]
            if etiqueta in tabla_simbolos:
                # Si la etiqueta ya existe en la tabla de símbolos, actualiza su dirección de definición
                tabla_simbolos[etiqueta][0] = contador_de_programa
            else:
                tabla_simbolos[etiqueta] = [contador_de_programa, []]
            # Agrega opcode al bytecode
            bytecode.append(UAMicroI_Opcodes[tokens[1]])
            # Checa si la dirección es símbolo o número
            if '0x' in tokens[2]:
                # Agrega la dirección explícita
                bytecode.append(int(tokens[2], 16))
            else:
                # Agrega o actualiza el símbolo a la tabla de símbolos, con la dirección de sustitución
                # y si es la primera mención, marca la dirección con -1
                if tokens[2] in tabla_simbolos:
                    tabla_simbolos[tokens[2]][1].append(contador_de_programa + 1)
                else:
                    tabla_simbolos[tokens[2]] = [-1, [contador_de_programa + 1]]
                # Agrega un byte de relleno para sustituir la dirección en el paso dos
                bytecode.append(0x00)
            # Actualiza contador de programa
            contador_de_programa += 2
        elif len(tokens) == 2 and ':' in tokens[0] and tokens[1] in UAMicroI_Opcodes:
            # Caso - etiqueta: opcode
            etiqueta = tokens[0][:-1]
            if etiqueta in tabla_simbolos:
                # Si la etiqueta ya existe en la tabla de símbolos, actualiza su dirección de definición
                tabla_simbolos[etiqueta][0] = contador_de_programa
            else:
                # Agrega etiqueta a tabla de símbolos
                tabla_simbolos[etiqueta] = [contador_de_programa, []]
            # Agrega opcode al bytecode
            bytecode.append(UAMicroI_Opcodes[tokens[1]])
            # Actualiza contador de programa
            contador_de_programa += 1
        elif len(tokens) == 2 and ':' in tokens[0] and not tokens[1] in UAMicroI_Opcodes:
            # Caso . etiqueta: valor
            # Agrega o actualiza etiqueta en la tabla de símbolos, con la dirección de sustitución
            if tokens[0][:-1] in tabla_simbolos:
                tabla_simbolos[tokens[0][:-1]][0] = contador_de_programa
            else:
                tabla_simbolos[tokens[0][:-1]] = [contador_de_programa, []]
            # Agrega el valor al bytecode
            bytecode.append(int(tokens[1], 16))
            # Actualiza contador de programa
            contador_de_programa += 1
        elif len(tokens) == 2 and tokens[0] in UAMicroI_Opcodes:
            # Caso - opcode dir
            # Agrega opcode al bytecode
            bytecode.append(UAMicroI_Opcodes[tokens[0]])
            # Verifica si la dirección es explícita o simbólica
            if '0x' in tokens[1]:
                # Agrega dirección explícita al bytecode
                bytecode.append(int(tokens[1], 16))
            else:
                # Agrega o actualiza símbolo en la tabla de símbolos, con la dirección de sustitución
                # y si es la primera mención, marca la dirección con -1
                if tokens[1] in tabla_simbolos:
                    tabla_simbolos[tokens[1]][1].append(contador_de_programa + 1)
                else:
                    tabla_simbolos[tokens[1]] = [-1, [contador_de_programa + 1]]
                # Agrega un byte de relleno para sustituir la dirección en el paso dos
                bytecode.append(0x00)
            # Actualiza contador de programa
            contador_de_programa += 2
        elif len(tokens) == 1 and tokens[0] in UAMicroI_Opcodes:
            # Caso - opcode
            # Agrega opcode al bytecode
            bytecode.append(UAMicroI_Opcodes[tokens[0]])
            # Actualiza contador de programa
            contador_de_programa += 1
        else:
            print(f'ERROR de sintaxis: {linea}')
            exit(0)
        
    # Muestra resultados del primer paso
    #print(f'Código: {bytecode}')
    #print(f'Tabla de símbolos: {tabla_simbolos}')

    #### Paso 2

    # Procesa la tabla de símbolos
    for simbolo, info in tabla_simbolos.items():
        if len(info[1]):
            # Si el símbolo tiene referencias ...
            if info[0] == -1:
                # ... pero no está definido
                print(f'ERROR: Símbolo indefinido: {simbolo}')
                exit(0)
            else:
                # ... y tiene referencias
                for ref in info[1]:
                    bytecode[ref] = info[0]
        else:
            # El símbolo no tiene referencias
            print(f'ADVERTENCIA: {simbolo} está definido pero no se usa')
    return bytecode, tabla_simbolos
"""
# Ensambla el programa
bytecode, tabla_simbolos = ensamblar(programa)
# Muestra resultados del segundo paso
bytecodestr = '/'.join([f'{byte:02X}' for byte in bytecode])
print(f'Código: {bytecodestr}')
print(f'Tabla de símbolos: {tabla_simbolos}')

# Guarda archivo 
with open(sys.argv[1].replace('asm', 'bin'), 'wb') as f:
    f.write(bytecode)
    

"""