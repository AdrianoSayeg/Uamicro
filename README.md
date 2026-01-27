# UAMICRO Project: Simulador de Microprocesadores Didácticos

Este repositorio contiene la implementación en Python de los microprocesadores**UAMICRO**, diseñados con fines educativos para ilustrar la arquitectura y el funcionamiento interno de una CPU elemental.

El proyecto permite visualizar las dos funciones básicas de una computadora: la decodificación de la instrucción (**FETCH**) y su ejecución (**EXECUTE**).

> Basado en el *"Corso Pratico di Informatica"*, disponible en [papuasia.org](https://papuasia.org/corsopratico/).


---

## UAMICRO I: Características Técnicas

La primera versión simula una arquitectura simplificada del modelo **Von Neumann**:

- **Arquitectura de 8 bits**: Buses de datos y direcciones independientes.
- **Memoria Unificada**: 256 locaciones de 8 bits.
- **Componentes Implementados**:
  - **ALU**: Operaciones aritméticas básicas (ADD, SUB).
  - **Registros**: Acumuladores A y B, PC (Program Counter), IR (Instruction Register).
  - **Matriz de Control**: Lógica basada en microinstrucciones y fases de tiempo (T0-T6).
- **Interfaz Gráfica (PyQt5)**: 
  - Visualización en tiempo real de registros y buses.
  - Resaltado dinámico del Program Counter en la tabla de memoria.
  - Carga de programas mediante archivos `.txt` en formato hexadecimal.

---

## Instalación y Uso

### Requisitos
- Python 3.9+
- PyQt5

### Ejecución
Para correr el simulador de la versión 1:
```bash
cd uamicro1
python3 main_gui.py
