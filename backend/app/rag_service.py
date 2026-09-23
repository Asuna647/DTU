"""
RAG Service — Retrieval Augmented Generation for Digital Saarthi.
Contains verified knowledge base for government schemes and services.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class SchemeInfo:
    name: str
    full_name: str
    category: str
    eligibility_summary: str
    documents_required: List[str]
    application_process: List[str]
    benefits: List[str]
    official_website: str
    helpline: str


# Verified knowledge base for government schemes
SCHEMES_DB = {
    "ignoaps": SchemeInfo(
        name="IGNOAPS",
        full_name="Indira Gandhi National Old Age Pension Scheme",
        category="Social Security",
        eligibility_summary="Age 60+ years, Below Poverty Line (BPL) status required",
        documents_required=[
            "Aadhaar Card",
            "BPL Ration Card",
            "Bank Account Passbook (first page)",
            "Passport size photograph",
            "Age proof certificate (if DOB not clear on Aadhaar)"
        ],
        application_process=[
            "Visit local Gram Panchayat/Ward Office",
            "Collect IGNOAPS application form (Form P-1)",
            "Fill form with officer assistance",
            "Attach self-attested document copies",
            "Submit form and collect acknowledgement",
            "Verification process takes up to 60 days"
        ],
        benefits=[
            "Monthly pension of ₹200 (Central share)",
            "Additional state contribution varies by state",
            "Direct benefit transfer to bank account",
            "Life-long pension until death"
        ],
        official_website="https://nsap.nic.in",
        helpline="1800-11-0001"
    ),

    "eshram": SchemeInfo(
        name="E-Shram",
        full_name="E-Shram Portal for Unorganised Workers",
        category="Labor & Employment",
        eligibility_summary="Age 16-59 years, Unorganised sector worker, not EPFO/ESIC member",
        documents_required=[
            "Aadhaar Card",
            "Mobile number linked to Aadhaar",
            "Bank Account details",
            "Self-declaration of occupation"
        ],
        application_process=[
            "Visit eshram.gov.in or download E-Shram mobile app",
            "Click 'Register on e-Shram'",
            "Enter Aadhaar number and mobile number",
            "Verify OTP sent to mobile",
            "Fill occupation, bank details, address",
            "Submit form and download E-Shram card"
        ],
        benefits=[
            "Unique 12-digit Universal Account Number (UAN)",
            "Accident insurance coverage of ₹2,00,000",
            "Partial disability insurance of ₹1,00,000",
            "Access to government welfare schemes",
            "Portable social security benefits"
        ],
        official_website="https://eshram.gov.in",
        helpline="14434"
    ),

    "pmkisan": SchemeInfo(
        name="PM-Kisan",
        full_name="Pradhan Mantri Kisan Samman Nidhi",
        category="Agriculture",
        eligibility_summary="Small and marginal farmers with cultivable land up to 2 hectares",
        documents_required=[
            "Aadhaar Card",
            "Bank Account details",
            "Land ownership documents",
            "Mobile number"
        ],
        application_process=[
            "Visit pmkisan.gov.in or local CSC",
            "Register with Aadhaar number",
            "Provide land and bank details",
            "Upload required documents",
            "Submit application for verification"
        ],
        benefits=[
            "₹6,000 per year in three installments",
            "₹2,000 every four months",
            "Direct benefit transfer to bank account",
            "Income support for agricultural expenses"
        ],
        official_website="https://pmkisan.gov.in",
        helpline="155261"
    )
}


def search_schemes(query: str) -> List[Dict[str, Any]]:
    """
    Search through the schemes database based on user query.
    Returns relevant scheme information.
    """
    query = query.lower()
    results = []

    # Keywords mapping for better search
    search_mappings = {
        "pension": ["ignoaps"],
        "पेंशन": ["ignoaps"],
        "old age": ["ignoaps"],
        "बुढ़ापा": ["ignoaps"],
        "worker": ["eshram"],
        "श्रमिक": ["eshram"],
        "labour": ["eshram"],
        "farmer": ["pmkisan"],
        "किसान": ["pmkisan"],
        "agriculture": ["pmkisan"]
    }

    # Find matching schemes
    matching_schemes = set()
    for keyword, schemes in search_mappings.items():
        if keyword in query:
            matching_schemes.update(schemes)

    # If no keyword match, search in scheme descriptions
    if not matching_schemes:
        for scheme_id, scheme in SCHEMES_DB.items():
            if (query in scheme.name.lower() or
                query in scheme.full_name.lower() or
                query in scheme.eligibility_summary.lower()):
                matching_schemes.add(scheme_id)

    # Format results
    for scheme_id in matching_schemes:
        scheme = SCHEMES_DB[scheme_id]
        results.append({
            "id": scheme_id,
            "name": scheme.name,
            "full_name": scheme.full_name,
            "category": scheme.category,
            "eligibility": scheme.eligibility_summary,
            "documents": scheme.documents_required,
            "process": scheme.application_process,
            "benefits": scheme.benefits,
            "website": scheme.official_website,
            "helpline": scheme.helpline
        })

    return results


def get_scheme_details(scheme_id: str) -> Dict[str, Any]:
    """Get detailed information for a specific scheme."""
    scheme = SCHEMES_DB.get(scheme_id)
    if not scheme:
        return {"error": "Scheme not found"}

    return {
        "id": scheme_id,
        "name": scheme.name,
        "full_name": scheme.full_name,
        "category": scheme.category,
        "eligibility": scheme.eligibility_summary,
        "documents": scheme.documents_required,
        "process": scheme.application_process,
        "benefits": scheme.benefits,
        "website": scheme.official_website,
        "helpline": scheme.helpline
    }


def get_common_documents() -> Dict[str, List[str]]:
    """Return commonly required documents across schemes."""
    return {
        "essential": ["Aadhaar Card", "Bank Account Passbook", "Mobile Number"],
        "age_proof": ["Aadhaar Card", "Birth Certificate", "School Leaving Certificate"],
        "income_proof": ["BPL Card", "Income Certificate", "Ration Card"],
        "address_proof": ["Aadhaar Card", "Voter ID", "Utility Bill", "Ration Card"]
    }


def get_verification_checklist(scheme_id: str) -> List[Dict[str, Any]]:
    """Get verification checklist for a scheme application."""
    checklists = {
        "ignoaps": [
            {"item": "Age verification", "description": "Must be 60 years or older", "critical": True},
            {"item": "BPL status", "description": "Must have Below Poverty Line card", "critical": True},
            {"item": "Bank account", "description": "Active bank account for pension transfer", "critical": True},
            {"item": "Document verification", "description": "All documents should be self-attested", "critical": False}
        ],
        "eshram": [
            {"item": "Age verification", "description": "Must be between 16-59 years", "critical": True},
            {"item": "Worker status", "description": "Must be unorganised sector worker", "critical": True},
            {"item": "Mobile verification", "description": "Mobile number linked to Aadhaar", "critical": True},
            {"item": "EPFO/ESIC check", "description": "Should not be EPFO or ESIC member", "critical": True}
        ]
    }

    return checklists.get(scheme_id, [])