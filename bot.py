import subprocess
from moviepy.editor import VideoFileClip, clips_array
from uploader import subirVideo
import os
import random

def editar(titulo, videoArriba, videoAbajo="BG.mp4"):
    # Nombres de archivos convertidos pre-definidos
    videoArribaConvertido = "video_arriba_convertido.mp4"
    videoAbajoConvertido = "video_abajo_convertido.mp4"

    # Duración del video a crear
    duracion_principal = VideoFileClip(videoArriba).duration
    duracion_fondo = VideoFileClip(videoAbajo).duration
    duracion_total = int(min(duracion_principal, duracion_fondo))

    # Duración del fragmento random
    if duracion_total >= duracion_fondo:
        inicio = 0
    else:
        inicio = random.uniform(0, duracion_fondo - duracion_total)
    fin = inicio + duracion_total
    
    clipRandom = VideoFileClip(videoAbajo).subclip(inicio, fin)
    clipRandom.write_videofile("RandomBG.mp4",codec="libx264",threads=4,preset="ultrafast",audio=False)
    videoAbajo = "RandomBG.mp4"

    # Convertir videos si es necesario
    convertir_video(videoArriba, videoArribaConvertido, str(duracion_total))
    convertir_video(videoAbajo, videoAbajoConvertido, str(duracion_total))

    clip1 = VideoFileClip(videoArribaConvertido).resize(height=960, width=1080)
    clip2 = VideoFileClip(videoAbajoConvertido).resize(height=960, width=1080)
    
    array = [
        [clip1], 
        [clip2]
    ]
    video = clips_array(array).resize((1080, 1920))

    # Guardar el video final
    video.write_videofile(f"{titulo}Final.mp4", codec="libx264", threads=4, bitrate="3000k", preset="fast")

    # Eliminar los videos No queremos dejar rastro oh yeah!
    os.remove(videoArribaConvertido)
    os.remove(videoAbajoConvertido)
    os.remove(videoAbajo)
    
    return f"{titulo}Final.mp4"

def convertir_video(video_entrada, video_salida, duracion):
    """ Recorta y lo convierte a un formato compatible. psdt: Gracias ChatGPT!! """
    comando = [
        "ffmpeg","-y", "-i", video_entrada,  
        "-t", duracion, # obtiene los primeros N segundotes
        "-vf", "scale=1280:720", # Cambia la resolución a 1280x720
        "-r", "30", # Fuerza 30 FPS
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",  
        "-c:a", "aac", "-b:a", "128k",  # Convierte el audio a AAC
        "-movflags", "+faststart",  # Mejora la compatibilidad del archivo final
        video_salida,
    ]
    subprocess.run(comando, check=True)
    