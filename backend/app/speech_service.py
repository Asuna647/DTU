"""
Speech Service — Voice interaction layer for Digital Saarthi.
Handles speech-to-text and text-to-speech for accessibility.
"""

from typing import Dict, Any
import re


# Mock voice responses for demonstration
VOICE_RESPONSES = {
    "pension": "मैं आपकी पेंशन के बारे में मदद कर सकता हूं। कृपया अपना आधार कार्ड स्कैन करें।",
    "eshram": "मैं ई-श्रम रजिस्ट्रेशन में आपकी मदद करूंगा। आपका आधार कार्ड देखने दीजिए।",
    "documents": "आपको कौन से दस्तावेज की जानकारी चाहिए? मैं आधार, पैन या वोटर आईडी की मदद कर सकता हूं।",
    "help": "नमस्ते! मैं डिजिटल सारथी हूं। मैं सरकारी योजनाओं में आपकी मदद कर सकता हूं।",
    "error": "क्षमा करें, मैं आपकी बात समझ नहीं पाया। कृपया फिर से कोशिश करें।"
}


def process_voice_query(query: str) -> Dict[str, Any]:
    """
    Processes voice/text input and determines user intent.
    Returns structured response with intent, confidence, and suggested actions.
    """
    query = query.lower().strip()

    # Intent detection based on keywords
    intent = "unknown"
    confidence = 0.0
    response_key = "help"

    # Pension-related queries
    pension_keywords = ["pension", "पेंशन", "old age", "बुढ़ापा", "ignoaps"]
    if any(keyword in query for keyword in pension_keywords):
        intent = "pension_inquiry"
        confidence = 0.9
        response_key = "pension"

    # E-Shram related queries
    eshram_keywords = ["eshram", "ई-श्रम", "worker", "श्रमिक", "registration", "रजिस्ट्रेशन"]
    elif any(keyword in query for keyword in eshram_keywords):
        intent = "eshram_inquiry"
        confidence = 0.9
        response_key = "eshram"

    # Document help queries
    doc_keywords = ["document", "दस्तावेज", "paper", "कागज", "aadhar", "आधार", "pan", "voter"]
    elif any(keyword in query for keyword in doc_keywords):
        intent = "document_help"
        confidence = 0.8
        response_key = "documents"

    # General help
    help_keywords = ["help", "मदद", "सहायता", "kya kar sakte", "क्या कर सकते"]
    elif any(keyword in query for keyword in help_keywords):
        intent = "general_help"
        confidence = 0.7
        response_key = "help"

    return {
        "intent": intent,
        "confidence": confidence,
        "original_query": query,
        "response_text": VOICE_RESPONSES.get(response_key, VOICE_RESPONSES["error"]),
        "suggested_actions": _get_suggested_actions(intent),
        "language_detected": "mixed" if any(ord(char) > 127 for char in query) else "english"
    }


def _get_suggested_actions(intent: str) -> list:
    """Returns suggested next steps based on detected intent."""
    actions = {
        "pension_inquiry": ["scan_document", "check_eligibility"],
        "eshram_inquiry": ["scan_document", "verify_worker_status"],
        "document_help": ["scan_document", "explain_document"],
        "general_help": ["show_services", "voice_guide"],
        "unknown": ["show_help", "try_again"]
    }
    return actions.get(intent, ["show_help"])


def generate_audio_response(text: str) -> Dict[str, str]:
    """
    Mock text-to-speech functionality.
    In a real implementation, this would generate audio.
    """
    return {
        "audio_url": f"/api/audio/{hash(text) % 10000}.mp3",  # Mock URL
        "text": text,
        "duration_seconds": len(text) * 0.1,  # Rough estimate
        "language": "hi-IN" if any(ord(char) > 127 for char in text) else "en-IN"
    }


# Pre-defined responses for common scenarios
GUIDED_RESPONSES = {
    "eligible_pension": {
        "hindi": "बधाई हो! आप पेंशन के लिए योग्य हैं। अब मैं आपको चार आसान स्टेप बताता हूं।",
        "english": "Congratulations! You are eligible for pension. Let me guide you through four easy steps."
    },
    "not_eligible_age": {
        "hindi": "क्षमा करें, पेंशन के लिए 60 साल की उम्र होनी चाहिए। अभी आपकी उम्र कम है।",
        "english": "Sorry, you need to be 60 years old for pension. You are currently under the age requirement."
    },
    "need_bpl_card": {
        "hindi": "पेंशन के लिए आपको पहले BPL कार्ड बनवाना होगा। मैं इसके लिए गाइड करूंगा।",
        "english": "You need to get a BPL card first for pension eligibility. Let me guide you through this process."
    }
}


def get_guided_response(scenario: str, language: str = "hindi") -> str:
    """Get pre-scripted response for common scenarios."""
    response_set = GUIDED_RESPONSES.get(scenario, {})
    return response_set.get(language, response_set.get("hindi", "मैं आपकी मदद करने की कोशिश कर रहा हूं।"))