# Digital Saarthi Frontend

Accessibility-first React frontend for the Digital Saarthi application.

## Features

- **Voice Interface**: Speak naturally in Hindi/English
- **Document Scanner**: Upload Aadhaar cards for automatic data extraction
- **Accessible Design**: Large buttons, high contrast, text-to-speech
- **Step-by-Step Guidance**: Visual action plans for government services
- **Real-time Updates**: Live progress through each step

## Installation

```bash
# Install dependencies
cd frontend
npm install
```

## Running the App

```bash
# Development server
npm start

# Production build
npm run build
```

The app will open at http://localhost:3000

## Accessibility Features

- Large touch targets (min 64px height)
- High contrast colors
- Text-to-speech support
- Voice input capability
- Keyboard navigation support
- Screen reader friendly
- Reduced motion support

## API Integration

The frontend connects to the FastAPI backend at http://localhost:8000

Required endpoints:
- `POST /api/voice-query` - Process voice/text input
- `POST /api/scan-document` - Extract data from documents
- `POST /api/check-eligibility` - Verify scheme eligibility
- `GET /api/schemes` - Get available government schemes