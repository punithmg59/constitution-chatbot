from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.services.loader_service import loader
from app.services.llm_service import init_client

app = FastAPI(title="ShareBot AI")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    loader.load()
    init_client()   # ✅ ADD THIS

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "API running 🚀"}