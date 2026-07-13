from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.database import engine
from app.modules.auth.models import Base
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.websocket.router import router as websocket_router

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(websocket_router)


# Create Database Tables
Base.metadata.create_all(bind=engine)