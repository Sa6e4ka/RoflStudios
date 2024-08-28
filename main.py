from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from backend import rofl_router_, micro_router

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rofl_router_)
app.include_router(micro_router)

if __name__ == "__main__":
    uvicorn.run(reload=True)