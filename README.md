# UAMICRO I

**UAMICRO I** es un microprocesador didáctico diseñado para simular la arquitectura y el funcionamiento interno de una CPU elemental.  
Se trata de un microprocesador simple y de capacidad limitada, cuyo objetivo principal es ilustrar las dos funciones básicas de las computadoras: la decodificación de la instrucción (**FETCH**) y la ejecución (**EXECUTE**).

El propósito de este microprocesador es facilitar la comprensión de los mecanismos fundamentales de ejecución de instrucciones, el funcionamiento de registros, la ALU, la memoria y el control por microinstrucciones.  

La arquitectura de UAMICRO sigue un modelo simplificado del esquema de **Von Neumann**, en el que los bloques funcionales tradicionales (entrada, memoria y salida) se integran en una única unidad de memoria. Esta configuración permite observar de forma clara el ciclo de instrucción y sus efectos internos sobre los componentes del sistema.

> Fragmento adaptado del *"Corso Pratico di Informatica"*, disponible en [papuasia.org](https://papuasia.org/corsopratico/), utilizado con fines educativos.

---

## 🚀 Características principales

- Simulación de una arquitectura de microprocesador educativo.
- Implementación en Python de:
  - Unidad Aritmética Lógica (ALU)
  - Contador de programa (PC)
  - Registros
  - Memoria unificada
- Ejecución de instrucciones paso a paso para observar los efectos internos.
- Interfaces gráficas experimentales desarrolladas en PyQt5.

---

## 📂 Estructura del proyecto

- `src/` → versión estable y funcional del simulador.  
- `experimental/` → desarrollos en progreso:  
  - `UAMicroII/` → segunda versión del microprocesador (en desarrollo).  
  - `UAMicro_GUI/` → nueva interfaz gráfica experimental.  
- `docs/` → documentación, reportes o capturas (a completar).  

---

## 🛠️ Requisitos

- Python 3.9+  
- Dependencias:
  - `PyQt5`  
  - `numpy`  

Instalación con:

```bash
pip install -r requirements.txt


