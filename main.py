import requests
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="Proxy para reproducion de audio")

@app.get("/audio")
def proxy_audio(GCP_URL:str):
    r = requests.get(GCP_URL, stream=True)
    return StreamingResponse(r.iter_content(1024), media_type="audio/mp3")
