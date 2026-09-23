"""
Generate PDF from Digital Saarthi Architecture Documentation using xhtml2pdf
"""

import markdown
from xhtml2pdf import pisa
from pathlib import Path

# File paths
base_dir = Path(__file__).parent
md_file = base_dir / "ARCHITECTURE.md"
pdf_file = base_dir / "Digital_Saarthi_Architecture.pdf"

# Custom CSS for PDF rendering
css = """
@page {
    size: a4 portrait;
    @frame header_frame {
        -pdf-frame-content: header_content;
        left: 50pt; width: 495pt; top: 30pt; height: 30pt;
    }
    @frame content_frame {
        left: 50pt; width: 495pt; top: 60pt; height: 720pt;
    }
    @frame footer_frame {
        -pdf-frame-content: footer_content;
        left: 50pt; width: 495pt; top: 790pt; height: 30pt;
    }
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #222222;
}

h1 {
    font-size: 22pt;
    color: #1a202c;
    border-bottom: 2px solid #3182ce;
    padding-bottom: 5px;
    margin-top: 15px;
    margin-bottom: 15px;
}

h2 {
    font-size: 16pt;
    color: #2b6cb0;
    margin-top: 20px;
    margin-bottom: 10px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 3px;
}

h3 {
    font-size: 12pt;
    color: #2d3748;
    margin-top: 15px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 10px;
}

ul, ol {
    margin-left: 20px;
    margin-bottom: 10px;
}

li {
    margin-bottom: 4px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}

th, td {
    border: 1px solid #cbd5e0;
    padding: 6px 8px;
    font-size: 9pt;
    text-align: left;
}

th {
    background-color: #edf2f7;
    font-weight: bold;
    color: #2d3748;
}

pre {
    background-color: #2d3748;
    color: #f7fafc;
    padding: 10px;
    font-family: Courier, monospace;
    font-size: 8pt;
    margin: 10px 0;
    white-space: pre-wrap;
}

code {
    background-color: #edf2f7;
    padding: 2px 4px;
    font-family: Courier, monospace;
    font-size: 9pt;
}

.diagram-box {
    background-color: #f7fafc;
    border: 1px solid #cbd5e0;
    padding: 10px;
    margin: 15px 0;
    font-family: Courier, monospace;
    font-size: 8pt;
}

.cover-title {
    font-size: 32pt;
    font-weight: bold;
    color: #2b6cb0;
    text-align: center;
    margin-top: 150px;
}

.cover-subtitle {
    font-size: 18pt;
    color: #4a5568;
    text-align: center;
    margin-top: 20px;
}

.cover-desc {
    font-size: 12pt;
    color: #718096;
    text-align: center;
    margin-top: 40px;
}

.cover-meta {
    font-size: 10pt;
    color: #a0aec0;
    text-align: center;
    margin-top: 150px;
}
"""

# HTML template with page frames
html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        {css}
    </style>
</head>
<body>
    <!-- Header and Footer content -->
    <div id="header_content" style="text-align: right; color: #a0aec0; font-size: 8pt;">
        Digital Saarthi — Architecture Documentation
    </div>
    <div id="footer_content" style="text-align: center; color: #a0aec0; font-size: 8pt;">
        Page <pdf:pagenumber/> of <pdf:pagecount/>
    </div>

    <!-- Cover Page -->
    <div class="cover-title">Digital Saarthi</div>
    <div class="cover-subtitle">Architecture Documentation</div>
    <div class="cover-desc">AI-Powered Action-Guidance Layer for Government Services</div>
    <div class="cover-meta">Version 1.0 &nbsp;|&nbsp; September 2026 &nbsp;|&nbsp; Comprehensive Technical Guide</div>

    <pdf:nextpage />

    <!-- Main Content -->
    {content}
</body>
</html>
"""

# Read the markdown content
with open(md_file, 'r', encoding='utf-8') as f:
    markdown_text = f.read()

# Convert markdown to HTML
md = markdown.Markdown(extensions=['tables', 'fenced_code'])
html_body = md.convert(markdown_text)

# Replace mermaid code blocks with nicer formatting
html_body = html_body.replace('<pre><code class="language-mermaid">', '<div class="diagram-box"><pre>')
html_body = html_body.replace('</code></pre>', '</pre></div>')

# Combine into full HTML
full_html = html_template.format(css=css, content=html_body)

# Convert to PDF using xhtml2pdf
with open(pdf_file, "wb") as f_pdf:
    pisa_status = pisa.CreatePDF(full_html, dest=f_pdf)

if not pisa_status.err:
    print(f"Successfully created PDF: {pdf_file}")
else:
    print(f"Error creating PDF: {pisa_status.err}")