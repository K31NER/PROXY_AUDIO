import requests
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI(title="Proxy para reproducción de audio")

@app.get("/audio")
def proxy_audio(GCP_URL: str):
    # Pedir al bucket el archivo original en modo stream
    r = requests.get(GCP_URL.strip(), stream=True)

    if r.status_code != 200:
        return Response(
            content=f"Error {r.status_code} al obtener el audio",
            status_code=r.status_code
        )

    # Detectar content-type original (mp3, wav, etc.)
    content_type = r.headers.get("content-type", "audio/mpeg")
    content_length = r.headers.get("content-length")

    headers = {}
    if content_length:
        headers["Content-Length"] = content_length

    return StreamingResponse(
        r.iter_content(1024),
        media_type=content_type,
        headers=headers
    )
