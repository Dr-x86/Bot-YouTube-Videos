import subprocess
from tkinter import messagebox

def download_video(url, filename): 
    if not filename:
        filename = "%(title)s.%(ext)s" # Default filename if none provided
    try:
        # Run yt-dlp with custom output
        process = subprocess.run(
            ["yt-dlp.exe", "-o", filename, url], 
            text=True
        )
        if process.returncode != 0:
            return f"Error en el proceso código {process.returncode}"
        
    except Exception as e:
        return(f"Error {str(e)} 💀")
        
    #messagebox.showinfo("Correcto","Video descargado con exito")
    return f"{filename}.mp4"
