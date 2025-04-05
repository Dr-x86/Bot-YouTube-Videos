import tkinter as tk
import os
from tkinter import filedialog
import threading
from tkinter import messagebox
from bot import subirVideo, editar
from PIL import Image, ImageTk
from win10toast import ToastNotifier
from time import sleep
from youtube import download_video

def proceso():
    deshabilitarEntradas()
    try:
        titulo = entradaTitulo.get()
        desc = entradaDescripcion.get("1.0", "end-1c")
        url = entradaUrl.get() 

        if not titulo or not desc or not url:
            messagebox.showerror("Error", "Campos incompletos")
            habilitarEntradas()
            return
        
        """
        Limpiamos los campos de entrada para evitar confusiones
        """
        labelVideos.config(text="Descargando video...", fg="blue")
        video_descarga = download_video(url, titulo)  # Descargamos el video de YouTube
        
        if not video_descarga.endswith(".mp4"):
            messagebox.showerror("Error", f"{video_descarga}")
            habilitarEntradas()
            borrarEntradas()
            labelVideos.config(text="")
            return
            
        labelVideos.config(text="Editando Video...", fg="blue")
        video = editar(titulo, video_descarga)
        
        labelVideos.config(text="Subiendo video...", fg="blue")
        subirVideo(video, titulo, desc)
        """
        Notificamos con el popup de Windows
        """
        
        toaster.show_toast("Completado", "¡Video subido a la plataforma!", duration=15)
        labelVideos.config(text="¡Proceso completado!", fg="green")
        
        sleep(2)
        # Eliminar los videos No queremos dejar rastro oh yeah!
        os.remove(video_descarga)
        os.remove(video)
        
    except Exception as e:
        labelVideos.config(text="Error en el proceso", fg="red")
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        habilitarEntradas()
    
    habilitarEntradas()
    borrarEntradas()

def deshabilitarEntradas():
    entradaTitulo.config(state=tk.DISABLED)  
    entradaUrl.config(state=tk.DISABLED)  
    entradaDescripcion.config(state="disabled")
    btn_inicio.config(state="disabled")

def habilitarEntradas():
    entradaDescripcion.config(state="normal")
    entradaTitulo.config(state="normal")
    entradaUrl.config(state="normal")
    btn_inicio.config(state="normal")

def borrarEntradas():
    entradaUrl.delete(0, tk.END)
    entradaTitulo.delete(0, tk.END)
    entradaDescripcion.delete("1.0", tk.END)

def inicio():
    """ Esta parte ayuda a la ejecución en hilos para no detener la interfaz """
    hilo = threading.Thread(target=proceso)
    hilo.daemon = True  # Permite que el hilo termine cuando se cierre la app
    hilo.start()

def salir():
    exit()


toaster = ToastNotifier()
root = tk.Tk()
root.title("Bot - YouTube")
root.geometry("400x500")

labelTituloURL = tk.Label(root, text="URL Del video").pack()
entradaUrl = tk.Entry(root, width=50)
entradaUrl.pack()

labelTitulo = tk.Label(root, text="Titulo del video").pack()
entradaTitulo = tk.Entry(root, width=50)
entradaTitulo.pack()

labelDesc = tk.Label(root, text="Descripción del video").pack()
entradaDescripcion = tk.Text(root, width=40, height=10)
entradaDescripcion.pack(pady=8)

labelVideos = tk.Label(root, text="")
labelVideos.pack()

btn_inicio = tk.Button(root, text="Iniciar", command=inicio, bg="lightgreen")
btn_inicio.pack(pady=5)

imagen = Image.open("imagen.png") 
imagen = imagen.resize((150, 70))
imagen_tk = ImageTk.PhotoImage(imagen)
label = tk.Label(root, image=imagen_tk)
label.pack(pady=5)

btn_fin = tk.Button(root, text="Salir", command=salir, bg="red", fg="white")
btn_fin.pack(pady=5)

root.mainloop()