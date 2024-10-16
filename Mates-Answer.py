import tkinter as tk
import random
import threading
import time
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Juego Matemático - Operaciones")
root.geometry("600x600")

# Variables globales
nivel = 1
puntuacion = 0
resultado_correcto = 0
tiempo_restante = 15
temporizador_activo = False
MAX_NIVELES = 60  # Máximo de niveles
respuestas_correctas = 0
respuestas_incorrectas = 0
hilo_temporizador = None

# Función para generar una operación y su resultado
def generar_operacion(nivel):
    operaciones = [
        lambda: (f"{random.randint(1, 5 * nivel)} + {random.randint(1, 5 * nivel)}", lambda a, b: a + b),
        lambda: (f"{random.randint(1, 5 * nivel)} - {random.randint(1, 5 * nivel)}", lambda a, b: a - b),
        lambda: (f"{random.randint(1, 5 * nivel)} * {random.randint(1, 5 * nivel)}", lambda a, b: a * b),
        lambda: (f"{random.randint(1, 5 * nivel)} / {random.randint(1, 5 * nivel) + 1}", lambda a, b: round(a / b, 2)),
    ]
    operacion = random.choice(operaciones)()
    valores = [int(num) for num in operacion[0].replace(" ", "").replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()]
    resultado = operacion[1](*valores)

    return operacion[0], resultado

# Función para generar opciones
def generar_opciones(resultado):
    opciones = {resultado}
    while len(opciones) < 5:
        opcion = round(resultado + random.uniform(-2, 2), 2)
        opciones.add(opcion)
    opciones = list(opciones)
    random.shuffle(opciones)
    return opciones

# Función para manejar el temporizador
def iniciar_temporizador():
    global tiempo_restante, temporizador_activo, hilo_temporizador

    # Reiniciar el tiempo restante y activar el temporizador
    tiempo_restante = 15
    temporizador_activo = True
    tiempo_label.config(text=f"Tiempo Restante: {tiempo_restante}s")  # Mostrar el tiempo inicial

    while tiempo_restante > 0 and temporizador_activo:
        time.sleep(1)
        tiempo_restante -= 1
        tiempo_label.config(text=f"Tiempo Restante: {tiempo_restante}s")
    
    # Si el tiempo se acaba y sigue activo el temporizador, pasa al siguiente nivel
    if tiempo_restante == 0 and temporizador_activo:
        verificar_respuesta(None)

# Función para detener el temporizador
def detener_temporizador():
    global temporizador_activo
    temporizador_activo = False  # Desactiva el temporizador actual

# Función que se ejecuta cuando el usuario selecciona una opción
def verificar_respuesta(valor):
    global puntuacion, nivel, resultado_correcto, respuestas_correctas, respuestas_incorrectas

    # Detener el temporizador actual
    detener_temporizador()

    # Evaluar la respuesta del usuario
    if valor is not None:  # Si se seleccionó una respuesta
        if valor == resultado_correcto:
            puntuacion += 1
            respuestas_correctas += 1
            respuesta_label.config(fg="green", text="Respuesta Correcta")
        else:
            respuestas_incorrectas += 1
            respuesta_label.config(fg="red", text="Respuesta Incorrecta")
    else:
        respuestas_incorrectas += 1
        respuesta_label.config(fg="red", text="No se seleccionó respuesta")

    # Incrementar nivel
    nivel += 1

    # Verificar si se ha alcanzado el máximo de niveles
    if nivel > MAX_NIVELES:
        finalizar_juego()
    else:
        actualizar_juego()

# Función para actualizar la interfaz gráfica con una nueva operación
def actualizar_juego():
    global resultado_correcto, hilo_temporizador

    # Limpiar la pantalla
    for widget in root.winfo_children():
        widget.destroy()

    # Generar operación y opciones
    operacion, resultado_correcto = generar_operacion(nivel)
    opciones = generar_opciones(resultado_correcto)

    # Mostrar nivel
    nivel_label = tk.Label(root, text=f"Nivel {nivel}", font=("Arial", 20))
    nivel_label.pack(pady=10)

    # Mostrar operación
    operacion_label = tk.Label(root, text=f"Operación: {operacion}", font=("Arial", 20))
    operacion_label.pack(pady=10)

    # Mostrar opciones
    for opcion in opciones:
        boton = tk.Button(root, text=str(opcion), font=("Arial", 16), command=lambda valor=opcion: verificar_respuesta(valor))
        boton.pack(pady=5)

    # Mostrar puntuación
    puntuacion_label = tk.Label(root, text=f"Puntuación: {puntuacion}", font=("Arial", 16))
    puntuacion_label.pack(pady=20)

    # Mostrar tiempo restante
    global tiempo_label
    tiempo_label = tk.Label(root, text=f"Tiempo Restante: {tiempo_restante}s", font=("Arial", 16))
    tiempo_label.pack(pady=10)

    # Mostrar mensaje de respuesta
    global respuesta_label
    respuesta_label = tk.Label(root, text="", font=("Arial", 16))
    respuesta_label.pack(pady=10)

    # Detener el hilo anterior del temporizador si está en ejecución
    if hilo_temporizador is not None and hilo_temporizador.is_alive():
        detener_temporizador()
    
    # Iniciar el temporizador en un hilo separado
    hilo_temporizador = threading.Thread(target=iniciar_temporizador)
    hilo_temporizador.start()

# Función para finalizar el juego
def finalizar_juego():
    global temporizador_activo
    detener_temporizador()

    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    # Mostrar resultados finales
    resultado_final_label = tk.Label(root, text="Juego Finalizado", font=("Arial", 24))
    resultado_final_label.pack(pady=20)

    # Mostrar respuestas correctas e incorrectas
    tk.Label(root, text=f"Respuestas Correctas: {respuestas_correctas}", font=("Arial", 16)).pack(pady=5)
    tk.Label(root, text=f"Respuestas Incorrectas: {respuestas_incorrectas}", font=("Arial", 16)).pack(pady=5)

    # Calcular y mostrar el porcentaje de IQ
    porcentaje_correctas = (respuestas_correctas / MAX_NIVELES) * 100 if MAX_NIVELES > 0 else 0
    tk.Label(root, text=f"Porcentaje de IQ: {porcentaje_correctas:.2f}%", font=("Arial", 18)).pack(pady=20)

    # Crear barra de progreso para mostrar IQ
    barra_progreso = ttk.Progressbar(root, length=400, maximum=100)
    barra_progreso['value'] = porcentaje_correctas
    barra_progreso.pack(pady=10)

    # Cambiar color de la barra de progreso
    if porcentaje_correctas <= 20:
        barra_progreso.config(style="red.Horizontal.TProgressbar")
    elif porcentaje_correctas <= 50:
        barra_progreso.config(style="orange.Horizontal.TProgressbar")
    elif porcentaje_correctas <= 80:
        barra_progreso.config(style="yellow.Horizontal.TProgressbar")
    else:
        barra_progreso.config(style="green.Horizontal.TProgressbar")

# Configurar estilos para la barra de progreso
style = ttk.Style()
style.configure("red.Horizontal.TProgressbar", troughcolor='white', background='red')
style.configure("orange.Horizontal.TProgressbar", troughcolor='white', background='orange')
style.configure("yellow.Horizontal.TProgressbar", troughcolor='white', background='yellow')
style.configure("green.Horizontal.TProgressbar", troughcolor='white', background='green')

# Iniciar el juego
actualizar_juego()

# Ejecutar la ventana principal
root.mainloop()
