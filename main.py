import tkinter as tk
import os
import threading
from tkinter import filedialog
from tkinter import messagebox
from bot import subirVideo, editar
from PIL import Image, ImageTk
from win10toast import ToastNotifier
from time import sleep

videos = []

def seleccionar_archivo():
    archivos = filedialog.askopenfilenames(
        title="Selecciona videos",
        filetypes=[("Todos los videos", "*.mp4;*.avi;*.mkv;*.mov;*.flv;*.wmv;*.webm;*.mpeg;*.mpg")]
    )
    if archivos:  # Si se seleccionó un archivo
        print(f"Existen {archivos}")
        if (len(archivos) != 2):
            labelVideos.config(text="Selecciona DOS videos",fg="red")
            return
        videos.clear()
        videos.extend(archivos[:2])
        
        titulo1 = os.path.basename(videos[0])
        titulo2 = os.path.basename(videos[1])
        
        labelVideos.config(text=f"Selección: {titulo1}, {titulo2}",fg="green")


def proceso():
    try:
        titulo = entradaTitulo.get()
        desc = entradaDescripcion.get("1.0", "end-1c")

        if not titulo or not desc or len(videos) != 2:
            messagebox.showerror("Error", "Campos incompletos")
            return

        labelVideos.config(text="Procesando video...", fg="blue")
        
        video = editar(titulo, videos[0], videos[1])
        subirVideo(video, titulo, desc)
        
        labelVideos.config(text="Subiendo video...", fg="blue")

        """
        Notificamos con el popup de Windows
        """
        toaster = ToastNotifier()
        toaster.show_toast("Completado", "¡Video subido a la plataforma!", duration=15)

        labelVideos.config(text="¡Proceso completado!", fg="green")
        
        sleep(2)
        # Eliminar los videos No queremos dejar rastro oh yeah!
        os.remove(videos[0])
        os.remove(videos[1])
        os.remove(video)
        
    except Exception as e:
        labelVideos.config(text="Error en el proceso", fg="red")
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def inicio():
    """ Esta parte ayuda a la ejecución en hilos para no detener la interfaz """
    hilo = threading.Thread(target=proceso)
    hilo.daemon = True  # Permite que el hilo termine cuando se cierre la app
    hilo.start()

root = tk.Tk()
root.title("Bot - YT")
root.geometry("400x430")

labelTitulo = tk.Label(root, text="Titulo del video").pack()
entradaTitulo = tk.Entry(root, width=50)
entradaTitulo.pack()

labelDesc = tk.Label(root, text="Descripción del video").pack()
entradaDescripcion = tk.Text(root, width=40, height=10)
entradaDescripcion.pack(pady=8)

# Botón para abrir el explorador de archivos
btn_seleccionar = tk.Button(root, text="Selecciona ambos videos", command=seleccionar_archivo)
btn_seleccionar.pack()

labelVideos = tk.Label(root, text="")
labelVideos.pack()

btn_inicio = tk.Button(root, text="Iniciar", command=inicio, bg="lightgreen")
btn_inicio.pack(pady=5)

imagen = Image.open("imagen.png") 
imagen = imagen.resize((150, 70))
imagen_tk = ImageTk.PhotoImage(imagen)
label = tk.Label(root, image=imagen_tk)
label.pack(pady=5)

root.mainloop()