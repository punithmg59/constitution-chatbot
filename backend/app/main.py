from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.services.loader_service import loader
from app.services.llm_service import init_client
from app.utils.logger import logger

app = FastAPI(title="ShareBot AI - Constitution & General Assistant")

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
    try:
        # Load embeddings
        logger.info("Loading embeddings...")
        loader.load()
        logger.info("✅ Embeddings loaded")
        
        # Initialize LLM client
        logger.info("Initializing LLM client...")
        init_client()
        logger.info("✅ LLM client initialized")
        
        logger.info("✅ All services initialized")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

app.include_router(chat_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "ShareBot API running 🚀", "version": "1.0.0"}