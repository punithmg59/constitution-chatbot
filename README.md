# Constitution Chatbot

An AI-powered conversational system for intelligent Q&A about indian constitutional documents.

A project combining a Python FastAPI backend and Flutter frontend.

## Project Structure

- **backend/** - Python FastAPI application with RAG capabilities
  - `app/` - Main application code
    - `routes/` - API endpoints
    - `services/` - Business logic (LLM, embeddings, RAG)
    - `db/` - Database configuration
  - `requirements.txt` - Python dependencies
  - `run.py` - Start the backend server

- **frentend/** - Flutter mobile/web application
  - `lib/` - Flutter source code
  - `pubspec.yaml` - Flutter dependencies

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv myvenv
myvenv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frentend
flutter pub get
flutter run
```

## Requirements

- Python 3.8+
- Flutter SDK
- PostgreSQL (for backend)

## License

[Add your license]
