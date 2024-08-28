from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

import os
from backend.Loggs.logger_config import logger 
from dotenv import load_dotenv

load_dotenv()


'''
Класс для инициализации клента AWS S3
    и создания функций:
        - Отправки файлов на s3
        - Получения файлов с s3
        - Удаления фалов на s3
        - Получение singed url видео для передачи на фронтенд
'''
class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            bucket_name: str,
    ):
        '''
        При инициализации класса передаются секртеные ключи и имя бакета
        '''
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

   
    @asynccontextmanager
    async def get_client(self):
        '''
        Создание клиента aws s3 с использованием контекстного менеджера (хз как это работает)
        '''
        async with self.session.create_client("s3", **self.config) as client:
            yield client


    async def upload_file(
            self,
            object_name,
            content
    ):
        '''
        Метод для загрузки файлов в бакет - требуется только передать video_id
        ''' 
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
            

    async def delete_file(self, object_name: str):
        '''
        Метод удаления файлов с бакета
        '''
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            logger.debug(f"Error deleting file: {e}")
            
   
    async def get_file(self, object_name: str):
        '''
        Метод получения файлов с бакета
        '''
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


    async def get_url(self, object_name):
        '''
        Метод получения подписанного url файла с бакета для встраивания во фронтенд
        '''
        async with self.get_client() as client:
            url = await client.generate_presigned_url(
                "get_object",
                Params={
                        'Bucket': self.bucket_name,
                        'Key': object_name
                    },
                ExpiresIn=360000
            )

            return url