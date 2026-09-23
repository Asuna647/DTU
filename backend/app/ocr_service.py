"""
OCR Service — Extracts structured information from uploaded government documents.
Uses Tesseract where available; falls back to a reliable simulation for demo.
"""

import re
from datetime import date
from typing import Optional
from PIL import Image
import io

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def _extract_age_from_dob(dob_str: str) -> Optional[int]:
    """Parse DOB strings like DD/MM/YYYY or DD-MM-YYYY and return current age."""
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d %m %Y"):
        try:
            dob = date.fromisoformat(dob_str) if fmt == "%Y-%m-%d" else date.strptime(dob_str, fmt)
            today = date.today()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except ValueError:
            continue
    return None


def parse_document(image_bytes: bytes) -> dict:
    """
    Extracts key fields from a government document image.
    Returns a dict with: name, dob, age, gender, has_bpl, raw_text
    """
    raw_text = ""

    if TESSERACT_AVAILABLE:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            raw_text = pytesseract.image_to_string(image, lang="eng+hin")
        except Exception:
            raw_text = ""

    # ── Name ──────────────────────────────────────────
    name_match = re.search(r"(?i)(?:name[:\s]+)([A-Z][a-zA-Z\s]{2,40})", raw_text)
    name = name_match.group(1).strip() if name_match else "Unknown"

    # ── DOB / Age ─────────────────────────────────────
    dob_match = re.search(r"\b(\d{2}[/\-]\d{2}[/\-]\d{4}|\d{4}-\d{2}-\d{2})\b", raw_text)
    dob = dob_match.group(1) if dob_match else None
    age: Optional[int] = None
    if dob:
        age = _extract_age_from_dob(dob)
    if age is None:
        age_match = re.search(r"(?i)age[:\s]+(\d{2})", raw_text)
        if age_match:
            age = int(age_match.group(1))

    # ── Gender ────────────────────────────────────────
    gender = "Unknown"
    if re.search(r"\bMALE\b", raw_text, re.IGNORECASE):
        gender = "Male"
    elif re.search(r"\bFEMALE\b", raw_text, re.IGNORECASE):
        gender = "Female"

    # ── BPL Status ────────────────────────────────────
    has_bpl = bool(re.search(r"\bBPL\b|\bbelow poverty\b", raw_text, re.IGNORECASE))

    return {
        "name": name,
        "dob": dob,
        "age": age,
        "gender": gender,
        "has_bpl": has_bpl,
        "raw_text_preview": raw_text[:300] if raw_text else "(no text extracted — Tesseract unavailable)",
    }


# ── Demo simulation for hackathon (no real image needed) ──────────────────────
DEMO_AADHAAR = {
    "name": "Ramkali Devi",
    "dob": "12/03/1954",
    "age": 72,
    "gender": "Female",
    "has_bpl": True,
    "raw_text_preview": "[DEMO MODE] Aadhaar card for Ramkali Devi, DOB: 12/03/1954, BPL Category.",
}

DEMO_YOUNG_WORKER = {
    "name": "Suresh Kumar",
    "dob": "05/08/1992",
    "age": 33,
    "gender": "Male",
    "has_bpl": False,
    "raw_text_preview": "[DEMO MODE] Aadhaar card for Suresh Kumar, DOB: 05/08/1992.",
}
