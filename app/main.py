from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
# Import models so SQLAlchemy registers tables
from app.modules.auth import models as auth_models
from app.modules.chat import models as chat_models
from app.modules.library import models as library_models

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.websocket.router import router as websocket_router
from app.modules.chat.router import router as chat_router
from app.modules.library.router import router as library_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Static Files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/library-ui")
def library_ui():
    return FileResponse("frontend/library.html")

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
app.include_router(chat_router)
app.include_router(library_router)
