"""
Digital Saarthi — Main FastAPI application.
AI-powered Action-Guidance Layer for government services.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json

from app.ocr_service import parse_document, DEMO_AADHAAR, DEMO_YOUNG_WORKER
from app.rule_engine import check_ignoaps, check_eshram, EligibilityResult
from app.speech_service import process_voice_query, generate_audio_response, get_guided_response
from app.rag_service import search_schemes, get_scheme_details, get_common_documents

app = FastAPI(
    title="Digital Saarthi API",
    description="AI-powered assistance for government services and digital literacy",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request/Response Models ──────────────────────────────────────────
class VoiceQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "auto"

class EligibilityCheckRequest(BaseModel):
    scheme: str
    age: Optional[int]
    has_bpl: Optional[bool] = False
    is_organised_worker: Optional[bool] = False

class DocumentData(BaseModel):
    name: str
    dob: Optional[str]
    age: Optional[int]
    gender: str
    has_bpl: bool
    raw_text_preview: str


# ── API Endpoints ───────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "Digital Saarthi API — Your AI-powered guide for government services",
        "version": "1.0.0",
        "endpoints": {
            "voice": "/api/voice-query",
            "document": "/api/scan-document",
            "eligibility": "/api/check-eligibility",
            "schemes": "/api/schemes"
        }
    }


@app.post("/api/voice-query")
async def process_voice(request: VoiceQueryRequest):
    """
    Process voice/text input and return structured guidance.
    """
    try:
        result = process_voice_query(request.query)

        # Generate audio response for accessibility
        audio_response = generate_audio_response(result["response_text"])

        return {
            "success": True,
            "intent": result["intent"],
            "confidence": result["confidence"],
            "response_text": result["response_text"],
            "audio": audio_response,
            "suggested_actions": result["suggested_actions"],
            "language_detected": result["language_detected"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")


@app.post("/api/scan-document")
async def scan_document(file: UploadFile = File(...), demo_mode: bool = True):
    """
    Extract information from uploaded government document.
    Uses demo data when demo_mode=True for hackathon presentation.
    """
    try:
        if demo_mode:
            # For hackathon demo — return realistic test data
            if "young" in file.filename.lower() or "suresh" in file.filename.lower():
                extracted_data = DEMO_YOUNG_WORKER
            else:
                extracted_data = DEMO_AADHAAR
        else:
            # Real OCR processing
            content = await file.read()
            extracted_data = parse_document(content)

        return {
            "success": True,
            "extracted_data": extracted_data,
            "document_type": "aadhaar_card",
            "confidence": 0.95 if demo_mode else 0.8,
            "message": "Document processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")


@app.post("/api/check-eligibility")
async def check_eligibility(request: EligibilityCheckRequest):
    """
    Run rule engine to check scheme eligibility and generate action steps.
    """
    try:
        result: EligibilityResult

        if request.scheme.lower() == "ignoaps":
            result = check_ignoaps(request.age, request.has_bpl)
        elif request.scheme.lower() == "eshram":
            result = check_eshram(request.age, request.is_organised_worker)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scheme: {request.scheme}")

        # Generate appropriate guided response
        if result.eligible:
            guided_text = get_guided_response("eligible_pension")
        elif request.age and request.age < 60:
            guided_text = get_guided_response("not_eligible_age")
        elif not request.has_bpl:
            guided_text = get_guided_response("need_bpl_card")
        else:
            guided_text = "मैं आपकी स्थिति की जांच कर रहा हूं।"

        audio_response = generate_audio_response(guided_text)

        return {
            "success": True,
            "eligible": result.eligible,
            "scheme": result.scheme,
            "verdict": result.verdict,
            "reasons": result.reasons,
            "steps": result.steps,
            "warning": result.warning,
            "guided_response": {
                "text": guided_text,
                "audio": audio_response
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eligibility check failed: {str(e)}")


@app.get("/api/schemes")
async def get_schemes(query: Optional[str] = None):
    """
    Search and retrieve government schemes information.
    """
    try:
        if query:
            schemes = search_schemes(query)
        else:
            # Return all available schemes
            schemes = [
                get_scheme_details("ignoaps"),
                get_scheme_details("eshram"),
                get_scheme_details("pmkisan")
            ]

        return {
            "success": True,
            "schemes": schemes,
            "common_documents": get_common_documents()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scheme search failed: {str(e)}")


@app.get("/api/schemes/{scheme_id}")
async def get_scheme(scheme_id: str):
    """
    Get detailed information for a specific scheme.
    """
    try:
        scheme = get_scheme_details(scheme_id)
        if "error" in scheme:
            raise HTTPException(status_code=404, detail=scheme["error"])

        return {
            "success": True,
            "scheme": scheme
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scheme details: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "Digital Saarthi API",
        "components": {
            "ocr_service": "operational",
            "rule_engine": "operational",
            "speech_service": "operational",
            "rag_service": "operational"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)