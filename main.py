from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from dotenv import load_dotenv
from S3_class import S3Client  # Импортируйте ваш класс S3Client
import os

load_dotenv()

# Инициализация клиента S3
s3_client = S3Client(
        access_key=os.environ.get("AWS_ACCESS_KEY"),
        secret_key=os.environ.get("AWS_SECRET_KEY"),
        bucket_name=os.environ.get("AWS_BUCKET_NAME")
    )   

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_video(request: Request):

    video_name = "meme.mp4"  # Название видео в вашем бакете

    # Загрузка видео с S3
    await s3_client.get_file(object_name=video_name)

    return templates.TemplateResponse("index.html", {"request": request, "video_name": video_name})


@app.get("/videos/{video_name}")
async def serve_video(video_name: str):
    video_path = f"static/videos/{video_name}"
    if os.path.exists(video_path):
        return FileResponse(video_path)
    else:
        raise HTTPException(status_code=404, detail="Video not found")
