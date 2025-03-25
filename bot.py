import subprocess
from moviepy.editor import VideoFileClip, clips_array
from uploader import subirVideo
import os

def editar(titulo, videoArriba, videoAbajo):
    # Nombres de archivos convertidos pre-definidos
    videoArribaConvertido = "video_arriba_convertido.mp4"
    videoAbajoConvertido = "video_abajo_convertido.mp4"
    
    """
    En esta parte se obtiene el de menor duracion para evitar recortes innecesarios
    """
    duracion1 = VideoFileClip(videoArriba).duration
    duracion2 = VideoFileClip(videoAbajo).duration
    duracionVideo = int(min(duracion1, duracion2))
    
    # Convertir videos si es necesario
    convertir_video(videoArriba, videoArribaConvertido, str(duracionVideo))
    convertir_video(videoAbajo, videoAbajoConvertido, str(duracionVideo))

    clip1 = VideoFileClip(videoArribaConvertido).resize(width=500)
    clip2 = VideoFileClip(videoAbajoConvertido).resize(width=500)
    # Cargar los videos convertidos en MoviePy

    clip1V = clip1.subclip(0, duracionVideo)
    clip2V = clip2.subclip(0, duracionVideo)
    
    array = [
        [clip1V], 
        [clip2V]
    ]
    video = clips_array(array)

    # Guardar el video final
    video.write_videofile(f"{titulo}.mp4", codec="libx264", threads=4, bitrate="3000k")
    
    # Eliminar los videos No queremos dejar rastro oh yeah!
    os.remove(videoArribaConvertido)
    os.remove(videoAbajoConvertido)
    
    return f"{titulo}.mp4"

def convertir_video(video_entrada, video_salida, duracion):
    """ Recorta y lo convierte a un formato compatible. psdt: Gracias ChatGPT!! """
    comando = [
        "ffmpeg","-y", "-i", video_entrada,  
        "-t", duracion, # obtiene los primeros 60 segundotes
        "-vf", "scale=1280:720", # Cambia la resolución a 1280x720
        "-r", "30", # Fuerza 30 FPS
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",  
        "-c:a", "aac", "-b:a", "128k",  # Convierte el audio a AAC
        "-movflags", "+faststart",  # Mejora la compatibilidad del archivo final
        video_salida,
    ]
    subprocess.run(comando, check=True)