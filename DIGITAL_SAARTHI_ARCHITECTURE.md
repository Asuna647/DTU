# Digital Saarthi
## AI-Powered Action-Guidance Layer for Government Services

---

**Project**: Digital Saarthi  
**Hackathon**: DTU Vivekananda Innovation Hackathon 2026  
**Date**: October 2026  
**Version**: 1.0

---

# Table of Contents

1. Executive Summary
2. Problem Statement
3. System Architecture
4. Component Details
5. AI/ML Models & Integration
6. API Documentation
7. Implementation Guide
8. Marketing & Pitch Strategy
9. Appendix

---

# 1. Executive Summary

Digital Saarthi is an **AI-powered "Action-Guidance Layer"** designed to help elderly citizens and people with low digital literacy access government services. Unlike existing platforms like UMANG or DigiLocker that assume technical proficiency, Digital Saarthi provides:

- **Voice-first interaction** in Hindi/English
- **Document scanning** with automatic data extraction
- **Step-by-step guidance** with visual action plans
- **Verified information** through hardcoded rule engine
- **Accessibility-first UI** with large buttons, high contrast, and text-to-speech

### Key Features

| Feature | Description |
|---------|-------------|
| Voice Input | Natural language queries in Hindi/English |
| Document Scanner | OCR-powered Aadhaar/document extraction |
| Eligibility Engine | Hardcoded rules prevent hallucinations |
| Knowledge Base | Verified government schemes data (RAG) |
| TTS Support | Text-to-speech for accessibility |

### Target Impact

- **72 million** elderly citizens in India (60+ age group)
- **Millions** of digitally excluded citizens
- **Social workers** helping multiple beneficiaries

---

# 2. Problem Statement

## The Challenge

A large number of people, particularly **elderly citizens**, **people with low digital literacy**, **persons with disabilities**, and **people from rural communities**, struggle to use digital services.

### Common Pain Points

| Problem | Impact |
|---------|--------|
| Complex interfaces | Users don't know where to start |
| English-only content | 70%+ Indians prefer local languages |
| No voice support | Cannot type or read |
| Eligibility confusion | Don't know if they qualify |
| Document requirements | Unclear what documents needed |
| No step-by-step guidance | Forms abandoned halfway |

### Why Existing Solutions Fail

1. **UMANG/DigiLocker** - Assume users can navigate digital systems
2. **Generic Chatbots** - Unreliable, can hallucinate eligibility rules
3. **Government Websites** - Complex legal language, poor accessibility
4. **Customer Service** - Long wait times, limited availability

---

# 3. System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DIGITAL SAARTHI SYSTEM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      USER INTERFACE (React)                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │ Voice Input │  │ Doc Scanner │  │Result Cards │                │   │
│  │  │  🎤 mic     │  │  📷 upload  │  │  📋 steps   │                │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                │   │
│  │         │                 │                  │                      │   │
│  │         └─────────────────┼──────────────────┘                      │   │
│  │                           ▼                                           │   │
│  │                   ┌───────────────┐                                  │   │
│  │                   │  FastAPI API  │                                  │   │
│  │                   └───────┬───────┘                                  │   │
│  └───────────────────────────┼───────────────────────────────────────────┘   │
│                              │                                                │
│  ┌───────────────────────────┼───────────────────────────────────────────┐   │
│  │                      BACKEND LAYER                                    │   │
│  │                           │                                            │   │
│  │  ┌────────────┐  ┌────────▼───────┐  ┌────────────┐                 │   │
│  │  │  Speech    │  │  Rule Engine   │  │    RAG     │                 │   │
│  │  │  Service   │  │  (Safety Core) │  │  Service   │                 │   │
│  │  └────────────┘  └────────────────┘  └────────────┘                 │   │
│  │         │                  │                  │                       │   │
│  │         └──────────────────┼──────────────────┘                       │   │
│  │                            ▼                                            │   │
│  │  ┌─────────────────────────────────────────────────────────────┐     │   │
│  │  │                   OCR Service (Tesseract)                    │     │   │
│  │  └─────────────────────────────────────────────────────────────┘     │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │                        AI/ML LAYER                                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │  Whisper    │  │   Tesseract │  │    LLM      │                  │   │
│  │  │  (STT)      │  │    (OCR)    │  │ (Explanation)│                  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Voice Query Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │────▶│ Frontend │────▶│  Voice   │────▶│  Intent  │────▶│ Response │
│  Speaks  │     │          │     │ Service  │     │Detection │     │  + TTS   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                                    │
                                                                    ▼
                                                            ┌──────────────┐
                                                            │ Suggest Next │
                                                            │    Action    │
                                                            └──────────────┘
```

### Document Scan Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │────▶│ Frontend │────▶│   API    │────▶│  Tesseract│────▶│  Regex   │
│  Uploads │     │          │     │ Endpoint │     │   (OCR)   │     │  Parser  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                                          │
                                                                          ▼
                                                               ┌──────────────────┐
                                                               │ Extracted Data   │
                                                               │ (name, age, BPL) │
                                                               └──────────────────┘
```

### Eligibility Check Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Extracted  │────▶│    Rule      │────▶│   Decision   │────▶│   Step-by-   │
│     Data     │     │   Engine     │     │              │     │    Step      │
│ (age: 72,    │     │ (age >= 60,  │     │ ELIGIBLE /   │     │   Guidance   │
│  has_bpl: T) │     │  has_bpl=T)  │     │ NOT ELIGIBLE │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React + TypeScript | Accessible UI |
| **Backend** | FastAPI (Python) | REST API |
| **Database** | In-memory (MVP) | Scheme data storage |
| **Speech-to-Text** | Whisper | Voice transcription |
| **OCR** | Tesseract | Document text extraction |
| **LLM** | Claude/GPT | Explanation layer |
| **RAG** | Custom knowledge base | Verified scheme info |

---

# 4. Component Details

## 4.1 Rule Engine (`app/rule_engine.py`)

### Purpose
The **Safety Core** of Digital Saarthi - hardcoded eligibility rules that never hallucinate.

### How It Works

```python
# IGNOAPS Eligibility Rules
IGNOAPS_RULES = {
    "min_age": 60,
    "requires_bpl": True,
    "documents": ["Aadhaar", "BPL Card", "Bank Passbook"]
}

def check_ignoaps(age: int, has_bpl: bool) -> EligibilityResult:
    # Rule 1: Age check
    if age < 60:
        return EligibilityResult(
            eligible=False,
            reasons=["Age is below 60 years. Minimum required: 60 years."]
        )
    
    # Rule 2: BPL check
    if not has_bpl:
        return EligibilityResult(
            eligible=False,
            reasons=["BPL card required. Apply at local Tehsil office."]
        )
    
    # Both pass → Eligible
    return EligibilityResult(
        eligible=True,
        steps=[
            "Step 1: Gather documents...",
            "Step 2: Visit Gram Panchayat...",
            "Step 3: Submit application...",
            "Step 4: Collect acknowledgement..."
        ]
    )
```

### Integration Points
- **Input**: Age (int), has_bpl (bool)
- **Output**: EligibilityResult with eligible, reasons, steps
- **Called by**: `/api/check-eligibility` endpoint

### Why This Approach?

| Benefit | Explanation |
|---------|-------------|
| No hallucinations | Hardcoded rules = guaranteed correct |
| Auditable | Anyone can verify the logic |
| Fast | O(1) boolean checks, no API calls |
| Reliable | Works offline, no external dependencies |

---

## 4.2 OCR Service (`app/ocr_service.py`)

### Purpose
Extract structured data from government documents (Aadhaar cards, letters, notices).

### How It Works

```
Image Input → Tesseract OCR → Raw Text → Regex Parser → Structured Data
```

### Text Extraction Pipeline

1. **Tesseract Processing** (if available):
   ```python
   image = Image.open(io.BytesIO(image_bytes))
   raw_text = pytesseract.image_to_string(image, lang="eng+hin")
   ```

2. **Regex Pattern Matching**:
   ```python
   # Name extraction
   name_pattern = r"(?i)(?:name[:\s]+)([A-Z][a-zA-Z\s]{2,40})"
   name = re.search(name_pattern, raw_text)
   
   # DOB extraction
   dob_pattern = r"\b(\d{2}[/\-]\d{2}[/\-]\d{4})\b"
   dob = re.search(dob_pattern, raw_text)
   
   # BPL status
   has_bpl = bool(re.search(r"\bBPL\b", raw_text, re.IGNORECASE))
   ```

3. **Age Calculation**:
   ```python
   def calculate_age(dob: str) -> int:
       dob_date = datetime.strptime(dob, "%d/%m/%Y")
       today = datetime.now()
       return today.year - dob_date.year
   ```

### Demo Mode
For hackathon presentations without Tesseract setup:
```python
DEMO_AADHAAR = {
    "name": "Ramkali Devi",
    "age": 72,
    "has_bpl": True,
    "gender": "Female"
}
```

---

## 4.3 Speech Service (`app/speech_service.py`)

### Purpose
Handle voice interaction and text-to-speech for accessibility.

### Intent Detection

```python
INTENT_KEYWORDS = {
    "pension_inquiry": ["pension", "पेंशन", "old age", "बुढ़ापा"],
    "eshram_inquiry": ["eshram", "ई-श्रम", "worker", "श्रमिक"],
    "document_help": ["document", "दस्तावेज", "aadhar", "आधार"]
}

def detect_intent(query: str) -> str:
    query_lower = query.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            return intent
    return "unknown"
```

### Response Generation

```python
VOICE_RESPONSES = {
    "pension": "मैं आपकी पेंशन में मदद कर सकता हूं। कृपया अपना आधार कार्ड स्कैन करें।",
    "eshram": "म���ं ई-श्रम रजिस्ट्रेशन में आपकी मदद करूंगा।",
    "help": "नमस्ते! मैं डिजिटल सारथी हूं। मैं सरकारी योजनाओं में मदद कर सकता हूं।"
}
```

### Text-to-Speech (Frontend)

```typescript
// React component for TTS
const speakText = (text: string) => {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'hi-IN';  // Hindi
  utterance.rate = 0.8;      // Slower for clarity
  speechSynthesis.speak(utterance);
};
```

---

## 4.4 RAG Service (`app/rag_service.py`)

### Purpose
Verified knowledge base for government schemes - ensures AI explanations are grounded in reality.

### Knowledge Base Structure

```python
SCHEMES_DB = {
    "ignoaps": {
        "name": "IGNOAPS",
        "full_name": "Indira Gandhi National Old Age Pension Scheme",
        "eligibility": "Age 60+, BPL status required",
        "documents": ["Aadhaar", "BPL Card", "Bank Passbook"],
        "benefits": "₹200-500/month",
        "website": "https://nsap.nic.in"
    },
    "eshram": {
        "name": "E-Shram",
        "full_name": "E-Shram Portal for Unorganised Workers",
        "eligibility": "Age 16-59, unorganised worker",
        "documents": ["Aadhaar", "Mobile", "Bank Details"],
        "benefits": "₹2 lakh accident insurance",
        "website": "https://eshram.gov.in"
    }
}
```

### Query Functions

```python
def search_schemes(query: str) -> List[Dict]:
    """Find schemes matching user query"""
    results = []
    for scheme_id, scheme in SCHEMES_DB.items():
        if query.lower() in scheme["name"].lower():
            results.append(scheme)
    return results

def get_scheme_details(scheme_id: str) -> Dict:
    """Get complete scheme information"""
    return SCHEMES_DB.get(scheme_id, {})

def get_common_documents() -> Dict:
    """List commonly required documents"""
    return {
        "essential": ["Aadhaar", "Bank Account", "Mobile"],
        "income_proof": ["BPL Card", "Income Certificate"],
        "address_proof": ["Aadhaar", "Voter ID"]
    }
```

---

# 5. AI/ML Models & Integration

## 5.1 Whisper (Speech-to-Text)

### What It Is
OpenAI's Whisper is a general-purpose speech recognition model trained on diverse audio data.

### How It's Used
- Transcribes user's voice input to text
- Handles Hindi-English code-switching
- Works with accented speech

### Implementation
```python
# For MVP: Use Web Speech API in frontend
const recognizeSpeech = () => {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'hi-IN';
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    sendToBackend(transcript);
  };
  recognition.start();
};
```

### Why Whisper
| Factor | Consideration |
|--------|---------------|
| Accuracy | 85%+ on Indian languages |
| Speed | <1s transcription |
| Offline | Can run locally (large model) |
| Cost | Free (offline) or API pricing |

---

## 5.2 Tesseract OCR

### What It Is
Google's Tesseract is an open-source OCR engine that extracts text from images.

### How It's Used
```
User uploads Aadhaar photo → Tesseract extracts text → Regex parses data
```

### Installation
```bash
# Linux
sudo apt-get install tesseract-ocr tesseract-ocr-hin

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Performance Considerations

| Scenario | Accuracy |
|----------|----------|
| Clear scanned document | 95%+ |
| Phone photo, good light | 80-90% |
| Low light/blurry | 60-70% |

**MVP Solution**: Demo mode with simulated OCR data for reliable hackathon demos.

---

## 5.3 LLM (Explanation Layer)

### What It Is
Large Language Model (Claude, GPT) for generating natural language explanations.

### How It's Used (Carefully!)
```
Rule Engine Result + RAG Data → LLM → Simple Hindi/English Explanation
```

**CRITICAL**: LLM only explains VERIFIED outputs - never makes eligibility decisions.

### Why This Approach Prevents Hallucinations

| Traditional Chatbot | Digital Saarthi |
|---------------------|-----------------|
| LLM generates eligibility | LLM explains rule engine result |
| May invent rules | Rules are hardcoded |
| Unreliable | Verifiable |
| "You might be eligible..." | "Age 72 ≥ 60 ✓, BPL ✓ = Eligible" |

### Example

```
User Query: "Am I eligible for pension?"

Rule Engine: age=72, has_bpl=true → ELIGIBLE

RAG Data: IGNOAPS requires age≥60 AND BPL

LLM Input: "User is 72 years old and has BPL card. 
           IGNOAPS requires age≥60 and BPL status.
           Generate a friendly Hindi explanation."

LLM Output (safe): 
"बधाई हो! आप पेंशन के लिए पात्र हैं। 
आपकी उम्र 72 है (60+ आवश्यक) और आपके पास BPL कार्ड है।
अब चार आसान स्टेप में आवेदन करें..."
```

---

# 6. API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 6.1 Voice Query
**POST** `/api/voice-query`

Process voice/text input and detect user intent.

**Request:**
```json
{
  "query": "Mujhe pension ke baare mein batayein",
  "language": "auto"
}
```

**Response:**
```json
{
  "success": true,
  "intent": "pension_inquiry",
  "confidence": 0.9,
  "response_text": "मैं आपकी पेंशन में मदद कर सकता हूं। कृपया अपना आधार कार्ड स्कैन करें।",
  "suggested_actions": ["scan_document", "check_eligibility"]
}
```

---

### 6.2 Document Scan
**POST** `/api/scan-document`

Extract data from uploaded document image.

**Request:**
- `file`: Image file (multipart/form-data)
- `demo_mode`: boolean (optional, default: true)

**Response:**
```json
{
  "success": true,
  "extracted_data": {
    "name": "Ramkali Devi",
    "age": 72,
    "gender": "Female",
    "dob": "12/03/1954",
    "has_bpl": true
  },
  "document_type": "aadhaar_card",
  "confidence": 0.95
}
```

---

### 6.3 Check Eligibility
**POST** `/api/check-eligibility`

Run rule engine to verify scheme eligibility.

**Request:**
```json
{
  "scheme": "ignoaps",
  "age": 72,
  "has_bpl": true
}
```

**Response:**
```json
{
  "success": true,
  "eligible": true,
  "scheme": "IGNOAPS",
  "verdict": "Eligible for IGNOAPS Pension",
  "reasons": [
    "✓ Age is 72 years — meets minimum 60 years",
    "✓ BPL card status confirmed"
  ],
  "steps": [
    "Step 1 — Gather documents: Aadhaar, BPL card, bank passbook...",
    "Step 2 — Visit Gram Panchayat and ask for Form P-1...",
    "Step 3 — Fill form with officer assistance...",
    "Step 4 — Submit and collect acknowledgement..."
  ],
  "warning": null
}
```

---

### 6.4 Get Schemes
**GET** `/api/schemes`

Search government schemes knowledge base.

**Query Parameters:**
- `query`: Search term (optional)

**Response:**
```json
{
  "success": true,
  "schemes": [
    {
      "id": "ignoaps",
      "name": "IGNOAPS",
      "eligibility": "Age 60+, BPL required",
      "documents": ["Aadhaar", "BPL Card", "Bank Passbook"],
      "benefits": "₹200-500/month",
      "helpline": "1800-11-0001"
    }
  ]
}
```

---

### 6.5 Health Check
**GET** `/api/health`

Check API service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Digital Saarthi API",
  "components": {
    "ocr_service": "operational",
    "rule_engine": "operational",
    "speech_service": "operational",
    "rag_service": "operational"
  }
}
```

---

# 7. Implementation Guide

## 7.1 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd digital-saarthi-app/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python -m app.main
# OR
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd digital-saarthi-app/frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Access the App

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/openapi.json

---

## 7.2 Directory Structure

```
digital-saarthi-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app & routes
│   │   ├── rule_engine.py   # Eligibility verification
│   │   ├── ocr_service.py   # Document parsing
│   │   ├── speech_service.py# Voice processing
│   │   └── rag_service.py   # Knowledge base
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceInterface.tsx
│   │   │   ├── DocUpload.tsx
│   │   │   └── ResultCard.tsx
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── DIGITAL_SAARTHI_ARCHITECTURE.md  # This document
└── README.md
```

---

## 7.3 Testing

### Test API Endpoints

```bash
# Test voice query
curl -X POST http://localhost:8000/api/voice-query \
  -H "Content-Type: application/json" \
  -d '{"query": "pension ke baare mein"}'

# Test eligibility check
curl -X POST http://localhost:8000/api/check-eligibility \
  -H "Content-Type: application/json" \
  -d '{"scheme": "ignoaps", "age": 72, "has_bpl": true}'

# Test schemes search
curl "http://localhost:8000/api/schemes?query=pension"
```

---

## 7.4 24-Hour Hackathon Timeline

| Hour | Task |
|------|------|
| 1-2 | Backend: main.py, rule_engine.py |
| 3-4 | Backend: ocr_service.py, speech_service.py |
| 5-6 | Backend: rag_service.py, API testing |
| 7-9 | Frontend: Layout, VoiceInterface, DocUpload |
| 10-12 | Frontend: ResultCard, Accessibility, TTS |
| 13-14 | Integration testing, bug fixes |
| 15-18 | Polish, accessibility improvements |
| 19-22 | Documentation, demo preparation |
| 23-24 | Pitch practice, final checks |

---

# 8. Marketing & Pitch Strategy

## 8.1 Problem Statement for Judges

> **"72 million elderly Indians struggle with digital government services. Digital Saarthi bridges the literacy gap with voice-first, step-by-step guidance."**

### The Problem We Solve

| Statistic | Source |
|-----------|--------|
| 72M+ elderly (60+) in India | Census 2021 |
| 90%+ don't use internet | TRAI Report |
| Most abandon forms halfway | Government studies |

### Our Unique Position

We don't compete with UMANG/DigiLocker - we **supplement** them by helping users who can't use these platforms independently.

---

## 8.2 Demo Script (3-5 Minutes)

### Opening (30 seconds)
> "Good morning judges. Today I'll demonstrate Digital Saarthi - an AI assistant that helps elderly citizens access government services through voice and simple step-by-step guidance."

### Problem (30 seconds)
> "Consider Ramkali Devi, a 72-year-old widow in a village. She hears there's a pension she might qualify for. She goes to theCommon Service Center, waits 3 hours, and is told to come back with documents she doesn't understand. She gives up.
>
> This happens millions of times every year."

### Solution Demo (3 minutes)

**Step 1: Voice Query**
> "Let's see how Digital Saarthi helps. User speaks: 'Mujhe pension ke baare mein batayein'"

[Show app - Voice interface]
> "Our AI understands Hindi voice input and guides the user to scan their document."

**Step 2: Document Scan**
> "User uploads Aadhaar card. Our OCR extracts: Name - Ramkali Devi, Age - 72, BPL - Yes"

[Show extracted data]
> "This takes seconds, not hours."

**Step 3: Eligibility Check**
> "Behind the scenes, our Rule Engine verifies: Age 72 ≥ 60 ✓, BPL Status ✓"

[Show eligibility result]
> "Result: ELIGIBLE for IGNOAPS Pension"

**Step 4: Step-by-Step Guidance**
> "Most importantly, we don't just say 'eligible.' We provide 4 clear steps:"

[Show steps with progress]
> "Step 1: Gather documents
> Step 2: Visit Gram Panchayat
> Step 3: Fill form
> Step 4: Submit and wait"

### Closing (30 seconds)
> "Digital Saarthi doesn't replace government portals. We bridge the literacy gap, making Digital India accessible for everyone. Thank you."

---

## 8.3 Judges' Scorecard

| Criteria | How We Score |
|----------|--------------|
| **Problem Understanding** | ✓ Clearly defined literacy/access gap |
| **Technical Complexity** | ✓ FastAPI, React, OCR, Voice, LLM+RAG |
| **Innovation** | ✓ Verified Action-Guidance Layer |
| **Impact** | ✓ 72M+ elderly, millions more |
| **Demo Quality** | ✓ Working prototype with demo mode |
| **Feasibility** | ✓ MVP in 24 hours |

---

## 8.4 Competitive Analysis

| Feature | Digital Saarthi | UMANG | Generic Chatbots |
|---------|----------------|-------|------------------|
| Voice Input | ✓ | ✗ | Limited |
| Step-by-Step | ✓ | ✗ | ✗ |
| Document Scan | ✓ | ✗ | ✗ |
| Rule-Based Safety | ✓ | ✓ | ✗ |
| Elderly-First Design | ✓ | ✗ | ✗ |
| Hindi Support | ✓ | Limited | Varies |

---

# 9. Appendix

## A. API Request/Response Examples

### Complete User Journey

**1. Voice Query**
```json
// Request
POST /api/voice-query
{"query": "pension"}

// Response
{
  "intent": "pension_inquiry",
  "confidence": 0.9,
  "response_text": "मैं आपकी पेंशन में मदद कर सकता हूं।",
  "suggested_actions": ["scan_document"]
}
```

**2. Document Scan**
```json
// Request
POST /api/scan-document?demo_mode=true

// Response
{
  "extracted_data": {
    "name": "Ramkali Devi",
    "age": 72,
    "gender": "Female",
    "has_bpl": true
  }
}
```

**3. Eligibility Check**
```json
// Request
POST /api/check-eligibility
{"scheme": "ignoaps", "age": 72, "has_bpl": true}

// Response
{
  "eligible": true,
  "verdict": "Eligible for IGNOAPS Pension",
  "steps": [
    "Step 1 — Gather documents...",
    "Step 2 — Visit Gram Panchayat...",
    "Step 3 — Fill form...",
    "Step 4 — Submit and wait..."
  ]
}
```

---

## B. Environment Variables

```bash
# Backend (.env)
PORT=8000
DEBUG=true
DEMO_MODE=true

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TTS_ENABLED=true
```

---

## C. Known Limitations & Future Work

### Current Limitations
- OCR accuracy depends on image quality
- Limited to Hindi/English for MVP
- Single scheme (IGNOAPS) in demo

### Future Enhancements
- More government schemes (PM-Kisan, Ayushman Bharat)
- Regional language support (Tamil, Bengali, Marathi, etc.)
- WhatsApp integration
- Offline mode with local processing
- Admin dashboard for social workers

---

## D. Team & Credits

**Project**: Digital Saarthi  
**Hackathon**: DTU Vivekananda Innovation Hackathon 2026  
**Theme**: Ideas for a Better Tomorrow

---

*This document was generated for the DTU Hackathon 2026 presentation.*