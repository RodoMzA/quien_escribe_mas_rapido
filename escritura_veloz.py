'''Juego de Escritura veloz'''

import tkinter as tk
from tkinter import messagebox
import random
import time
import json

# Creamos las variables para obtener nombre de jugador, tiempo de inicio, lista de los mejores jugadores, frases a escribir.
usuario = ""
start_time = 0
frases = [
    "soy el mas rapido",
    "me gusta competir",
    "solo se que no se nada",
    "hola mundo"
]

filename = "score.json"

# Función para iniciar el juego
def iniciar_juego():
    global usuario, start_time

    usuario = entry_name.get().strip() # ------  Obtener el nombre que introduce el usuario en la ventana.
    # Verificamos que el usuario haya ingresado su nombre.
    if not usuario:
        # De no ser asi, mostrar ventanta de emergencia.
        messagebox.showwarning("Advertencia", "Por favor, ingresa tu nombre de usuario para empezar a jugar.")
        return

    label_frase["text"] = random.choice(frases) # Escoger aleatoriamente una frase de nuestra lista.
    entry_frase.delete(0, tk.END) # Eliminamos el texto para evitar trampa.
    entry_frase.focus_set()  # Saltamos directamente para escribir la frase al iniciar el juego.
    start_time = time.time() # Iniciamos el conteo.

# Función para verificar la palabra ingresada.
def verificar_frases():

    # Verificamos ha iniciado el juego para poder escribir la palabra
    if not label_frase["text"]:
        messagebox.showwarning("Advertencia", "Inicia el juego primero.")
        return

    # Verificamos que la frase que escriba el usuario sea la misma que aparece.
    palabra_escrita = entry_frase.get().strip() # Obtiene la frase escrita por el usuario.
    frase_mostrada = label_frase["text"]

    if palabra_escrita == frase_mostrada:
        end_time = time.time() # Terminamos el conteo
        tiempo_final = round(end_time - start_time, 2) # Calcula el resultado y lo redondea a 2 decimales.

        # Verificamos si la frase existe dentro del top.
        if frase_mostrada not in top_por_frases:
            # De no existir la añadimos la frase al top.
            top_por_frases[frase_mostrada] = []

        palabras = top_por_frases[frase_mostrada]

        # Verificamos si el usuario ya existe para reemplazar su tiempo si es menor que el anterior.
        if jugador_existe(palabras, usuario, frase_mostrada, tiempo_final): # (True) si el usuario no existe, (False) si el usuario existe.
            # Agregar usuario y tiempo final al top de la frase correspondiente.
            top_por_frases[frase_mostrada].append((usuario, tiempo_final))
            messagebox.showinfo("Correcto", f"Bien hecho {usuario}! Tiempo: {tiempo_final} segundos.")

        # Ordenar el top por tiempo (de menor a mayor) 
        top_por_frases[frase_mostrada].sort(key=lambda x: x[1]) 

        # Guardar top en archivo.json
        guardar_top_jugadores("score.json", top_por_frases)      

        # Reiniciamos el juego [Eliminar usuario y frase]
        entry_frase.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_name.focus_set()  # Saltamos al apartado de escribir nombre de usuario.
        label_frase["text"] = "" # Eliminamos la frase mostrada.
        actualizar_top_jugadores(frase_mostrada) # Actualizar la lista de tops

    # Si la palabra no coincide mostrar ventana de advertencia.
    else:
        messagebox.showerror("Error", "La palabra no coincide. Inténtalo de nuevo.")

# Función para actualizar el top de jugadores
def actualizar_top_jugadores(frase_mostrada):

    # Verificar si la frase existe dentro del diccionario.
    if frase_mostrada not in top_por_frases:
        top_por_frases[frase_mostrada] = []
    top_jugadores = top_por_frases[frase_mostrada]
    
    # Mostrar por debajo de la intefaz el top
    top_jugadores_text = f"Top Jugadores | Frase: '{frase_mostrada}':\n"
    for i, (name, time, ) in enumerate(top_jugadores[:5], start=1):
        top_jugadores_text += f"{i}. {name} - {time} segundos - Frase: {frase_mostrada}\n"
    label_top_jugadores["text"] = top_jugadores_text

# Función para mostrar una ventana con el top de cada frase.
def mostrar_todos_los_tops():
    if not top_por_frases:
        messagebox.showinfo("Tops", "No hay tops registrados todavía.")
        return

    # Crear un texto con todos los tops organizados por frases
    todos_los_tops_text = "Tops de Jugadores por Frase:\n\n"
    for frase, top_jugadores in top_por_frases.items():
        todos_los_tops_text += f"Frase: '{frase}'\n"
        for i, (name, time) in enumerate(top_jugadores[:5], start=1):
            todos_los_tops_text += f"{i}. {name} - {time} segundos\n"
        todos_los_tops_text += "\n"  # Separador entre frases

    # Mostrar el texto en una ventana emergente o en un Label
    messagebox.showinfo("Todos los Tops", todos_los_tops_text)

# Funcion para regresar (True) si el usuario no existe o (False) si el usuario existe.
def jugador_existe(palabras, usuario, frase_mostrada, tiempo_final):
    for i, (jugador, tiempo) in enumerate(palabras):
        if jugador == usuario:
            if tiempo_final > tiempo:
                messagebox.showinfo("Correcto", f"¡{usuario}! Tiempo: {tiempo_final} segundos.\n Tu mejor tiempo es: {tiempo}")
                return False
    # Reemplazar el tiempo si el nuevo es mejor.
            else:
                messagebox.showinfo("Correcto", f"¡Excelente {usuario}! Haz impuesto un nuevo record.\n Tiempo: {tiempo_final} segundos.")
                top_por_frases[frase_mostrada][i]= (usuario, tiempo_final)
                return False
    return True      

# Funcion para guardar la lista de tops.
def guardar_top_jugadores(filename, top_por_frases = {}):
    f = open(filename, "w")
    json.dump(top_por_frases, f, indent=4)

# Funcion para cargar la lista de tops.
def cargar_archivo_top_jugadores(filename):
    try:
        f = open(filename, "r")
        return json.load(f)
    except FileNotFoundError:
        print("Aun no existen jugadores para mostrar los marcadores.")
        return {}
    
top_por_frases = cargar_archivo_top_jugadores(filename)
    

# Crear ventana principal
root = tk.Tk()
root.title("Juego de Escritura Rápida | zRodoMzA")
root.geometry("500x800")

# Crear etiquetas y obtener el texto escrito por el usuario
label_name = tk.Label(root, text="Nombre de Usuario:", font=("Arial", 12))
label_name.pack(pady=5)
entry_name = tk.Entry(root, font=("Arial", 12))
entry_name.pack(pady=5)

# Botón para iniciar el juego
btn_start = tk.Button(root, text="Iniciar Juego", font=("Arial", 12), command=iniciar_juego)
btn_start.pack(pady=10)

# Etiqueta para mostrar la palabra
label_frase = tk.Label(root, text="", font=("Arial", 16), fg="blue")
label_frase.pack(pady=20)

# Campo para ingresar la palabra
entry_frase = tk.Entry(root, font=("Arial", 14))
entry_frase.pack(pady=10)

# Botón para verificar la palabra
btn_check = tk.Button(root, text="Verificar", font=("Arial", 12), command=verificar_frases)
btn_check.pack(pady=10)

# Etiqueta para mostrar el top de jugadores
label_top_jugadores = tk.Label(root, text="Top Jugadores:\n", font=("Arial", 12), justify=tk.LEFT)
label_top_jugadores.pack(pady=20)

# Botón para mostrar todos los tops
btn_mostrar_todos_los_tops = tk.Button(root, text="Mostrar Todos los Tops", command=mostrar_todos_los_tops)
btn_mostrar_todos_los_tops.pack(pady=10)

# Etiqueta para mostrar el top de jugadores
label_top_jugadores = tk.Label(root, text="Top Jugadores:", font=("Arial", 12))
label_top_jugadores.pack(pady=10)

root.mainloop()
