# Digital Saarthi Backend

This is the FastAPI backend for the Digital Saarthi application - an AI-powered assistance system for government services.

## Features

- **OCR Service**: Extract information from government documents (Aadhaar cards, etc.)
- **Rule Engine**: Hardcoded eligibility verification for government schemes
- **Speech Service**: Voice interaction and text-to-speech capabilities
- **RAG Service**: Verified knowledge base for government schemes and procedures

## Installation

1. Install Python 3.8+ and pip
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For OCR functionality, install Tesseract:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

## Running the Server

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python -m app.main
```

The API will be available at http://localhost:8000

## API Documentation

- Interactive API docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

## Supported Schemes

- **IGNOAPS**: Indira Gandhi National Old Age Pension Scheme
- **E-Shram**: Unorganised Workers Registration Portal
- **PM-Kisan**: Pradhan Mantri Kisan Samman Nidhi

## Demo Mode

The application includes a demo mode with realistic test data for hackathon presentations. Set `demo_mode=true` in document upload requests to use predefined responses.