# Simulación de Corrida de Procesos en un Sistema Operativo

Este repositorio contiene un programa de simulación en Python que modela el comportamiento de un sistema operativo de tiempo compartido. En este sistema, los procesos comparten el procesador y la memoria RAM de manera intercalada.

## Descripción del Código

El código simula la llegada, ejecución y finalización de procesos en un sistema operativo. Cada proceso solicita una cantidad de memoria RAM, realiza un conjunto de instrucciones y puede realizar operaciones de entrada/salida. El tiempo de ejecución de cada proceso se mide y se registran los resultados en un archivo CSV. Además, se genera un gráfico que muestra el tiempo total de ejecución en función del número de procesos.

## Requisitos

- Python 3
- SimPy
- Matplotlib

## Instrucciones de Uso

1. Instala los requisitos utilizando pip:

