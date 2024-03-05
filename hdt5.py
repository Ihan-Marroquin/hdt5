import simpy
import random
import csv
import statistics
import matplotlib.pyplot as plt

class Proceso:
    def inicializar_objeto(self, env, ram, cpu, numero_proceso):
        self.memoria_necesaria = random.randint(1, 10)
        self.instrucciones_restantes = random.randint(1, 10)
        self.env = env
        self.ram = ram
        self.cpu = cpu
        self.numero_proceso = numero_proceso

    def inicializar(self):
        print(f"En el tiempo {self.env.now}: Proceso {self.numero_proceso} - Solicitando {self.memoria_necesaria} unidades de memoria RAM")
        yield self.ram.get(self.memoria_necesaria)

    def ejecutar_proceso(self):
        while self.instrucciones_restantes > 0:
            with self.cpu.request() as req:
                yield req
                print(f"En el tiempo {self.env.now}: Proceso {self.numero_proceso} - Ejecutando instrucciones, Instrucciones restantes: {self.instrucciones_restantes}")
                tiempo_procesamiento = min(3, self.instrucciones_restantes)  # Procesa un máximo de 3 instrucciones
                yield self.env.timeout(tiempo_procesamiento)
                self.instrucciones_restantes -= tiempo_procesamiento

                # Si el proceso ya no tiene instrucciones por realizar, termina
                if self.instrucciones_restantes <= 0:
                    break

                # Generar un número aleatorio para decidir si se espera o no
                random_num = random.randint(1, 21)
                if random_num == 1:
                    yield self.env.process(self.operaciones_io())
                elif random_num == 2:
                    yield self.env.timeout(1)

    def operaciones_io(self):
        print(f"En el tiempo {self.env.now}: Proceso {self.numero_proceso} - Realizando operaciones de entrada/salida")
        yield self.env.timeout(1)

    def liberar_recursos(self):
        print(f"En el tiempo {self.env.now}: Proceso {self.numero_proceso} - Liberando recursos")
        yield self.ram.put(self.memoria_necesaria)

def simular_procesos(env, ram, cpu, num_procesos, intervalo):
    tiempos_ejecucion = []
    print("Comenzando simulación....")
    for i in range(num_procesos):
        proceso = Proceso()
        proceso.inicializar_objeto(env, ram, cpu, i + 1)
        tiempo_inicio = env.now
        yield env.process(proceso.inicializar())
        tiempo_inicio_ejecucion = env.now
        yield env.process(proceso.ejecutar_proceso())
        tiempo_final = env.now
        tiempos_ejecucion.append((tiempo_inicio, tiempo_final))
        yield env.process(proceso.liberar_recursos())

    tiempo_promedio = statistics.mean(tiempo_final - tiempo_inicio for tiempo_inicio, tiempo_final in tiempos_ejecucion)
    desviacion_estandar = statistics.stdev(tiempo_final - tiempo_inicio for tiempo_inicio, tiempo_final in tiempos_ejecucion)
    print(f"-------------------------------------------------") 
    print(f"Tiempo promedio de ejecución: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")
    print(f"-------------------------------------------------")

    numero_random = random.randint(1, 1000)
    nombre_archivo = f"{num_procesos}_procesos_{numero_random}_intervalo_{intervalo}.csv"
    
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['proceso', 'tiempo_I', 'tiempo_F'])
        for i, (tiempo_inicio, tiempo_final) in enumerate(tiempos_ejecucion):
            writer.writerow([i + 1, tiempo_inicio, tiempo_final])

    print(f"Resultados almacenados en el archivo: {nombre_archivo}")

    plotear_tiempos(tiempos_ejecucion)

def plotear_tiempos(tiempos_ejecucion):
    num_procesos = range(1, len(tiempos_ejecucion) + 1)
    tiempo_total = [tiempo_final - tiempo_inicio for tiempo_inicio, tiempo_final in tiempos_ejecucion]
    tiempo_acumulado = [sum(tiempo_total[:i+1]) for i in range(len(tiempo_total))]

    plt.plot(num_procesos, tiempo_acumulado, marker='o')
    plt.title('Tiempo Total')
    plt.xlabel('Procesos')
    plt.ylabel('Tiempo de Ejecución')
    plt.grid(True)
    plt.show()

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)

num_procesos = int(input("Ingrese la cantidad de procesos a simular: "))
intervalo = 10

env.process(simular_procesos(env, ram, cpu, num_procesos, intervalo))
env.run()
