from fastapi import APIRouter
import os

from backend.S3client import S3Client

rofl_router_ = APIRouter()

s3_client = S3Client(
        access_key=os.environ.get("AWS_ACCESS_KEY"),
        secret_key=os.environ.get("AWS_SECRET_KEY"),
        bucket_name=os.environ.get("AWS_BUCKET_NAME")
    )   

@rofl_router_.get("/get_video")
async def get_video():
    url = await s3_client.get_url(object_name="meme.mp4")

    return url




