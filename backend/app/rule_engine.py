"""
Rule Engine — Safety Core for Digital Saarthi.
Encodes verified eligibility rules for government schemes.
LLM is never used here; rules are hardcoded and auditable.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EligibilityResult:
    eligible: bool
    scheme: str
    verdict: str  # Short label shown to user
    reasons: List[str]  # Human-readable explanation bullets
    steps: List[str]  # Action roadmap if eligible (or corrective steps if not)
    warning: Optional[str] = None  # Any cautionary note


# ──────────────────────────────────────────────
# IGNOAPS — Indira Gandhi National Old Age Pension
# ──────────────────────────────────────────────
IGNOAPS_STEPS = [
    "Step 1 — Gather documents: Aadhaar card, BPL ration card, bank passbook (first page), and a passport-size photo.",
    "Step 2 — Visit your local Gram Panchayat / Ward Office and ask for the IGNOAPS application form (Form P-1).",
    "Step 3 — Fill the form with the help of the ward officer. Attach self-attested photocopies of all documents.",
    "Step 4 — Submit the form at the office and collect the acknowledgement slip. Your pension will start within 60 days after verification.",
]

IGNOAPS_BPL_STEPS = [
    "You do not currently have a BPL card, which is required for IGNOAPS.",
    "Step A — Apply for a BPL card first: Visit your local Tehsil / Block office with your Aadhaar, income certificate, and ration card.",
    "Step B — Once you receive the BPL card, return here and follow the IGNOAPS steps.",
]


def check_ignoaps(age: Optional[int], has_bpl: bool) -> EligibilityResult:
    """
    IGNOAPS eligibility check.
    Rules:
      - Age must be >= 60
      - Must hold a BPL (Below Poverty Line) card
    """
    reasons: List[str] = []
    eligible = True

    if age is None:
        return EligibilityResult(
            eligible=False,
            scheme="IGNOAPS",
            verdict="Cannot determine eligibility",
            reasons=["Age could not be extracted from the document. Please upload a clearer Aadhaar card."],
            steps=[],
            warning="Please retry with a clearer document scan.",
        )

    if age < 60:
        eligible = False
        reasons.append(f"Age is {age} years. Minimum required age is 60 years.")
    else:
        reasons.append(f"✔ Age is {age} years — meets the minimum age requirement of 60.")

    if not has_bpl:
        eligible = False
        reasons.append("BPL (Below Poverty Line) card status not detected in document.")
    else:
        reasons.append("✔ BPL card status confirmed.")

    if eligible:
        return EligibilityResult(
            eligible=True,
            scheme="IGNOAPS",
            verdict="Eligible for IGNOAPS Pension",
            reasons=reasons,
            steps=IGNOAPS_STEPS,
        )
    else:
        corrective = IGNOAPS_BPL_STEPS if not has_bpl else []
        return EligibilityResult(
            eligible=False,
            scheme="IGNOAPS",
            verdict="Not currently eligible",
            reasons=reasons,
            steps=corrective,
            warning="Do not pay anyone to help you apply. This service is free.",
        )


# ──────────────────────────────────────────────
# E-Shram — Unorganised Worker Registration
# ──────────────────────────────────────────────
ESHRAM_STEPS = [
    "Step 1 — Visit eshram.gov.in or use the E-Shram app on your phone.",
    "Step 2 — Click 'Register on e-Shram'. Enter your Aadhaar number and mobile number linked to Aadhaar.",
    "Step 3 — An OTP will be sent to your mobile. Enter it to verify.",
    "Step 4 — Fill in your occupation, bank account details, and address. Submit the form.",
    "Step 5 — Download your E-Shram card (UAN card). This entitles you to accident insurance of ₹2 lakh.",
]


def check_eshram(age: Optional[int], is_organised_worker: bool) -> EligibilityResult:
    """
    E-Shram eligibility check.
    Rules:
      - Age between 16 and 59
      - Must be an unorganised sector worker (not an EPFO/ESIC member)
    """
    reasons: List[str] = []
    eligible = True

    if age is None:
        return EligibilityResult(
            eligible=False,
            scheme="E-Shram",
            verdict="Cannot determine eligibility",
            reasons=["Age could not be extracted from the document."],
            steps=[],
        )

    if not (16 <= age <= 59):
        eligible = False
        reasons.append(f"Age is {age}. E-Shram is for workers aged 16–59.")
    else:
        reasons.append(f"✔ Age is {age} — within the eligible 16–59 range.")

    if is_organised_worker:
        eligible = False
        reasons.append("Workers already covered by EPFO or ESIC are not eligible for E-Shram.")
    else:
        reasons.append("✔ Unorganised worker status confirmed.")

    return EligibilityResult(
        eligible=eligible,
        scheme="E-Shram",
        verdict="Eligible for E-Shram Registration" if eligible else "Not eligible for E-Shram",
        reasons=reasons,
        steps=ESHRAM_STEPS if eligible else [],
    )
