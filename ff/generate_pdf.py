import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors

def build_pdf():
    pdf_path = "C:/Users/user/Documents/GitHub/Digital_Saarthi_Architecture_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1A202C'),
        backColor=colors.HexColor('#EDF2F7'),
        borderPadding=6,
        spaceAfter=8
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Digital Saarthi: Technical Architecture & System Guide", title_style))
    story.append(Paragraph("End-to-End System Design, AI Model Integration, Implementation Details & Reliability Safeguards", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph(
        "<b>Digital Saarthi</b> serves as an AI-powered <i>Action-Guidance Layer</i> tailored specifically for underserved, "
        "elderly, and low-literacy citizens seeking government welfare services. Rather than attempting to duplicate or replace "
        "large government aggregator portals (such as UMANG or DigiLocker), Digital Saarthi acts as a digital bridge. It transforms "
        "complex bureaucratic notifications, confusing portals, and eligibility documents into step-by-step, verified actions "
        "using accessible voice, OCR scanning, and factual rule-backed retrieval.",
        body_style
    ))

    # System Architecture Section
    story.append(Paragraph("2. System Architecture & Component Graph", h1_style))
    story.append(Paragraph(
        "The architecture is modularly separated into an Accessibility-First Frontend, an API/Orchestration Gateway, "
        "specialized AI processing engines, and a deterministic safety core.",
        body_style
    ))

    img_path = "C:/Users/user/Documents/GitHub/architecture.png"
    if os.path.exists(img_path):
        img = Image(img_path, width=450, height=220)
        story.append(img)
        story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Figure 1:</b> High-level data and control flow across frontend, backend inference modules, rule engine, and LLM explanation layer.", ParagraphStyle('Caption', parent=body_style, fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor('#718096'))))
    story.append(Spacer(1, 10))

    # Comprehensive Component Details
    story.append(Paragraph("3. Detailed Component Breakdown & AI Models", h1_style))

    components = [
        ("Accessibility-First Frontend (React / Flutter)",
         "Provides high-contrast, large touch targets, single-tap voice capture, and camera/upload integration for documents. "
         "It abstracts digital complexity by guiding users visually and audibly through each stage of interaction."),

        ("Speech-to-Text: OpenAI Whisper / Bhashini",
         "<b>How it works:</b> Utilizes an encoder-decoder Transformer trained on extensive multilingual speech audio. Converts speech waveforms to log-mel spectrograms, which are processed into linguistic tokens.<br/>"
         "<b>Why it is helpful:</b> Enables voice interaction in local vernacular languages and accents, eliminating literacy barriers and handling background noise effectively."),

        ("Document OCR: Tesseract / EasyOCR",
         "<b>How it works:</b> Performs image binarization, adaptive thresholding, line/word segmentation, and neural character recognition (LSTM/CRNN) to extract raw text from captured Aadhaar cards, BPL cards, and ration cards.<br/>"
         "<b>Why it is helpful:</b> Removes manual data entry friction for elderly citizens by parsing fields like Age, DOB, Gender, and BPL status via structured regex extraction."),

        ("Intent Detection & Request Router",
         "<b>How it works:</b> Employs lightweight sentence embedding matching / classification to route citizen queries (e.g., pension inquiry vs ration status vs document verification) to the correct processing pipeline.<br/>"
         "<b>Why it is helpful:</b> Ensures fast routing, low latency, and deterministic workflow selection without relying on expensive end-to-end model calls."),

        ("Deterministic Rule Engine (The Safety Core)",
         "<b>How it works:</b> Implements hardcoded, auditable boolean evaluation logic based directly on gazetted eligibility criteria (e.g., IGNOAPS: Age >= 60 AND BPL == True).<br/>"
         "<b>Why it is helpful:</b> Eliminates hallucinations in eligibility determination. The model never guesses eligibility; the Rule Engine authoritatively computes it."),

        ("Retrieval-Augmented Generation (RAG Knowledge Base)",
         "<b>How it works:</b> Indexes verified official government scheme documentation into a vector database (e.g., ChromaDB/FAISS) with dense retrieval embeddings.<br/>"
         "<b>Why it is helpful:</b> Grounding LLM responses strictly in retrieved official context ensures high factual fidelity, up-to-date scheme requirements, and source reference traceability."),

        ("LLM Explanation Layer (e.g., Llama 3 / Claude / GPT)",
         "<b>How it works:</b> Acts strictly as a natural language synthesizer and action translator. It receives the deterministic Rule Engine outcome and retrieved RAG context to format a conversational, compassionate, step-by-step guide.<br/>"
         "<b>Why it is helpful:</b> Formats complex eligibility logic into clear, non-jargon steps in the user's native dialect while preventing ungrounded advice.")
    ]

    for title, desc in components:
        story.append(Paragraph(f"• <b>{title}</b>", h2_style))
        story.append(Paragraph(desc, bullet_style))

    story.append(PageBreak())

    # API Specification
    story.append(Paragraph("4. Backend API Endpoints Reference", h1_style))
    story.append(Paragraph(
        "The backend is built with FastAPI for asynchronous performance, OpenAPI schema validation, and low-latency response times.",
        body_style
    ))

    api_table_data = [
        [Paragraph("<b>Endpoint</b>", body_style), Paragraph("<b>Method & Payload</b>", body_style), Paragraph("<b>Function & Response</b>", body_style)],
        [
            Paragraph("<b>/api/voice-query</b>", body_style),
            Paragraph("POST<br/><code>{\"query\": \"...\"}</code>", code_style),
            Paragraph("Detects intent from speech text, queries RAG, returns guidance text and suggested UI actions (e.g. scan document).", body_style)
        ],
        [
            Paragraph("<b>/api/scan-document</b>", body_style),
            Paragraph("POST (Multipart)<br/><code>file=@Aadhaar.jpg</code>", code_style),
            Paragraph("Extracts textual fields via OCR, parses age, DOB, BPL card status, and returns structured user attributes.", body_style)
        ],
        [
            Paragraph("<b>/api/check-eligibility</b>", body_style),
            Paragraph("POST<br/><code>{\"scheme\":\"ignoaps\", \"age\":72, \"has_bpl\":true}</code>", code_style),
            Paragraph("Executes deterministic rule verification. Returns eligibility boolean, detailed rationale, and concrete application steps.", body_style)
        ],
        [
            Paragraph("<b>/api/schemes</b>", body_style),
            Paragraph("GET<br/><code>?query=pension</code>", code_style),
            Paragraph("Lists matching government schemes with eligibility criteria, required documents, and benefit descriptions.", body_style)
        ]
    ]

    t = Table(api_table_data, colWidths=[120, 150, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2D3748')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Implementation & Code Workflow
    story.append(Paragraph("5. Step-by-Step Implementation & Run Guide", h1_style))
    story.append(Paragraph("<b>Step 1: Backend Setup & Execution</b>", h2_style))
    story.append(Paragraph("Navigate to the backend directory, install dependencies, and launch FastAPI with Uvicorn:", body_style))
    story.append(Paragraph("cd backend<br/>pip install -r requirements.txt<br/>python -m app.main  # Running on http://localhost:8000", code_style))

    story.append(Paragraph("<b>Step 2: Frontend Setup & Execution</b>", h2_style))
    story.append(Paragraph("Navigate to the frontend directory, install Node dependencies, and start the development server:", body_style))
    story.append(Paragraph("cd frontend<br/>npm install<br/>npm start  # App running on http://localhost:3000", code_style))

    story.append(Paragraph("<b>Step 3: Verification with cURL</b>", h2_style))
    story.append(Paragraph("Test backend endpoints directly:", body_style))
    story.append(Paragraph(
        'curl -X POST http://localhost:8000/api/check-eligibility ^<br/>'
        '  -H "Content-Type: application/json" ^<br/>'
        '  -d "{\\\"scheme\\\":\\\"ignoaps\\\",\\\"age\\\":72,\\\"has_bpl\\\":true}"',
        code_style
    ))

    # Anti-Hallucination & Safety Principles
    story.append(Paragraph("6. Anti-Hallucination & Privacy Safeguards", h1_style))
    story.append(Paragraph(
        "To ensure high trust and avoid common pitfalls of AI in civic tech, Digital Saarthi enforces three foundational pillars:<br/>"
        "1. <b>Zero Decision Delegation:</b> LLMs never make eligibility judgments. Judgments are made purely by deterministic code.<br/>"
        "2. <b>PII Protection:</b> User documents are processed ephemerally in-memory and never sent to external public LLM training queues.<br/>"
        "3. <b>Source Grounding:</b> Every guidance recommendation links back to verifiable official government department guidelines.",
        body_style
    ))

    doc.build(story)
    print("PDF generated successfully at:", pdf_path)

if __name__ == '__main__':
    build_pdf()
