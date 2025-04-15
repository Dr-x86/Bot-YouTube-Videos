import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Definir los alcances de la API (YouTube Upload)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    credentials = None

    # Si ya existe un token guardado, lo cargamos
    if os.path.exists("token.pickle"):
        print("CREDENCIALES FUNCIONAN")
        with open("token.pickle", "rb") as token_file:
            credentials = pickle.load(token_file)
    else:
        # Si no hay credenciales válidas, autenticamos
        if credentials or credentials.expired or credentials.refresh_token:
            print("CREDENCIALES NO VALIDAS RE-SOLICITANDO (...)")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=8080)  # Autenticación manual la primera vez
            # Guardamos las credenciales en un archivo para futuras ejecuciones
            with open("token.pickle", "wb") as token_file:
                pickle.dump(credentials, token_file)

    return build("youtube", "v3", credentials=credentials)
    
def subirVideo(video_path, titulo, desc):
    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": titulo,
                "description": desc,
                "tags": ["Viral", "Meme"],
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "public",
            },
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True),
    )

    response = request.execute()
    print(f"¡Video subido con éxito! ID: {response['id']}")