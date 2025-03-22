import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from bot import subirVideo, editar
from PIL import Image, ImageTk
import os
from win10toast import ToastNotifier

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


def inicio():
    """ Parametros """
    titulo = entradaTitulo.get()
    desc = entradaDescripcion.get("1.0", "end-1c")
    video1 = videos[0]
    video2 = videos[1]
    
    if(titulo == "" or desc == "" or videos is None):
        print("Falta llenar un campo")
        messagebox.showerror("Error","Campos incompletos")
        return
        
    video = editar(titulo, video1, video2)
    subirVideo(video,titulo, desc)
    
    toaster = ToastNotifier()
    toaster.show_toast("Completado", "¡Video subido a la plataforma!", duration=5)

    
def obtener_entradas():
    # Obtener el texto de las entradas
    
    print(f"Descripción: {desc}")

# Crear ventana
root = tk.Tk()
root.title("Granja-Bot-YT")
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
