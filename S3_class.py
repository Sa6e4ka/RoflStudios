import asyncio
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

import os
from logger_config import logger 
from dotenv import load_dotenv

load_dotenv()


'''
Класс для инициализации клента AWS S3
    и создания функций:
        - Отправки файлов на s3
        - Получения файлов с s3
        - Удаления фалов на s3
'''
class S3Client:
    '''
    При инициализации класса передаются секртеные ключи и имя бакета
    '''
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        self.bucket_name = bucket_name
        self.session = get_session()


    '''
    Создание клиента aws s3 с использованием контекстного менеджера (хз как это работает)
    '''
    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client


    '''
    Метод для загрузки файлов в бакет - требуется только передать video_id
    '''
    async def upload_file(
            self,
            object_name,
            content
    ):
        try:
            # С созданием клиента отправляем видео в хранилище
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=content,
                )
                logger.info(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            logger.debug(f"Error uploading file: {e}")
            

    '''
    Метод удаления файлов с бакета
    '''
    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            logger.debug(f"Error deleting file: {e}")
            

    '''
    Метод получения файлов с бакета
    '''
    async def get_file(self, object_name: str):
        try:
            if not os.path.exists("static/videos/"):
                os.mkdir("static/videos/")
 
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                # Запись файла
                with open(f"static/videos/{object_name}", "wb") as file:
                    file.write(data)
                logger.info(f"File {object_name} downloaded")
        except ClientError as e:
            logger.debug(f"Error downloading file: {e}")

'''
Пример инициализации класса
'''
# async def main():
#     s3_client = S3Client(
#     access_key=os.environ.get("AWS_ACCESS_KEY"),
#     secret_key=os.environ.get("AWS_SECRET_KEY"),
#     bucket_name=os.environ.get("AWS_BUCKET_NAME")
# )   
#     await s3_client.get_file(object_name="meme.mp4")



# if __name__ == "__main__":
#     asyncio.run(main())

    