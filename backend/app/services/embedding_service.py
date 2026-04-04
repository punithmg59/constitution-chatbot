from app.services.loader_service import loader

def get_embedding(text: str):
    return loader.model.encode([text])