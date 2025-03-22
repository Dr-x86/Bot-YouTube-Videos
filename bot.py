import subprocess
from moviepy.editor import VideoFileClip, clips_array
from uploader import subirVideo
import os

def convertir_video(video_entrada, video_salida):
    """ Recorta el video a 60 segundos y lo convierte a un formato compatible. """
    comando = [
        "ffmpeg","-y", "-i", video_entrada,  
        "-t", "60", # obtiene los primeros 60 segundotes
        "-vf", "scale=1280:720", # Cambia la resolución a 1280x720
        "-r", "30", # Fuerza 30 FPS
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",  
        "-c:a", "aac", "-b:a", "128k",  # Convierte el audio a AAC
        "-movflags", "+faststart",  # Mejora la compatibilidad del archivo final
        video_salida,
    ]
    subprocess.run(comando, check=True)


def editar(titulo, videoArriba, videoAbajo):
    """ Pega dos videos uno sobre otro después de convertirlos si es necesario. """
    # Nombres de archivos convertidos
    videoArribaConvertido = "video_arriba_convertido.mp4"
    videoAbajoConvertido = "video_abajo_convertido.mp4"

    # Convertir videos si es necesario
    convertir_video(videoArriba, videoArribaConvertido)
    convertir_video(videoAbajo, videoAbajoConvertido)

    # Cargar los videos convertidos en MoviePy
    clip1 = VideoFileClip(videoArribaConvertido).resize(width=500)
    clip2 = VideoFileClip(videoAbajoConvertido).resize(width=500)

    clip1V = clip1.subclip(0, 60)
    clip2V = clip2.subclip(0, 60)
    
    array = [
        [clip1V], 
        [clip2V]
    ]
    video = clips_array(array)

    # Guardar el video final
    video.write_videofile(f"{titulo}.mp4", codec="libx264", threads=4, bitrate="3000k")
    
    # Temporalmente se eliminan los videos con la conversión necesaria
    os.remove(videoArribaConvertido)
    os.remove(videoAbajoConvertido)
    
    return f"{titulo}.mp4"