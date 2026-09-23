import React, { useState } from 'react';
import { VoiceInterface } from './components/VoiceInterface';
import { DocUpload } from './components/DocUpload';
import { ResultCard } from './components/ResultCard';
import './index.css';

// API Base URL - change in production
const API_BASE = 'http://localhost:8000';

interface ExtractedData {
  name: string;
  age: number;
  has_bpl: boolean;
  gender: string;
  dob: string;
}

interface EligibilityResult {
  eligible: boolean;
  scheme: string;
  verdict: string;
  reasons: string[];
  steps: string[];
  warning?: string;
}

function App() {
  const [currentView, setCurrentView] = useState<'home' | 'voice' | 'document' | 'result'>('home');
  const [isLoading, setIsLoading] = useState(false);
  const [extractedData, setExtractedData] = useState<ExtractedData | null>(null);
  const [eligibilityResult, setEligibilityResult] = useState<EligibilityResult | null>(null);
  const [voiceResponse, setVoiceResponse] = useState<string>('');

  // Handle voice query
  const handleVoiceQuery = async (query: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/voice-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await response.json();
      setVoiceResponse(data.response_text);

      // If query is about pension, guide to document scan
      if (data.suggested_actions?.includes('scan_document') || data.suggested_actions?.includes('check_eligibility')) {
        setCurrentView('document');
      }
    } catch (error) {
      console.error('Voice query error:', error);
      // Fallback for demo
      setVoiceResponse('मैं आपकी पेंशन में मदद कर सकता हूं। कृपया अपना आधार कार्ड स्कैन करें।');
      setCurrentView('document');
    }
    setIsLoading(false);
  };

  // Handle document upload
  const handleDocumentUpload = async (file: File | null, useDemo: boolean) => {
    setIsLoading(true);
    try {
      if (useDemo) {
        // Use demo data from API
        const response = await fetch(`${API_BASE}/api/scan-document?demo_mode=true`, {
          method: 'POST',
          // For demo, we send empty form data
          body: new FormData()
        });
        const data = await response.json();
        if (data.success) {
          setExtractedData(data.extracted_data);
          // Automatically check eligibility
          await checkEligibility(data.extracted_data);
        }
      } else if (file) {
        // Real file upload
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch(`${API_BASE}/api/scan-document?demo_mode=false`, {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        if (data.success) {
          setExtractedData(data.extracted_data);
          await checkEligibility(data.extracted_data);
        }
      }
    } catch (error) {
      console.error('Document upload error:', error);
      // Fallback demo data
      setExtractedData({
        name: 'Ramkali Devi',
        age: 72,
        has_bpl: true,
        gender: 'Female',
        dob: '12/03/1954'
      });
      await checkEligibility({
        name: 'Ramkali Devi',
        age: 72,
        has_bpl: true,
        gender: 'Female',
        dob: '12/03/1954'
      });
    }
    setIsLoading(false);
  };

  // Check eligibility based on extracted data
  const checkEligibility = async (data: ExtractedData) => {
    try {
      const response = await fetch(`${API_BASE}/api/check-eligibility`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scheme: 'ignoaps',
          age: data.age,
          has_bpl: data.has_bpl
        })
      });
      const result = await response.json();
      setEligibilityResult(result);
      setCurrentView('result');
    } catch (error) {
      console.error('Eligibility check error:', error);
      // Fallback result
      setEligibilityResult({
        eligible: data.age >= 60 && data.has_bpl,
        scheme: 'IGNOAPS',
        verdict: data.age >= 60 && data.has_bpl
          ? 'पेंशन के लिए पात्र'
          : 'अभी पात्र नहीं',
        reasons: [
          data.age >= 60
            ? `✓ आयु ${data.age} वर्ष है — 60 वर्ष की न्यूनतम आवश्यकता पूरी होती है`
            : `आयु ${data.age} वर्ष है। न्यूनतम आवश्यकता 60 वर्ष है।`,
          data.has_bpl
            ? '✓ BPL कार्ड स्थिति की पुष्टि।'
            : 'BPL कार्ड स्थिति का पता नहीं चला।'
        ],
        steps: data.age >= 60 && data.has_bpl
          ? [
              'Step 1 — दस्तावेज इकट्ठा करें: आधार कार्ड, BPL राशन कार्ड, बैंक पासबुक (पहला पृष्ठ), और पासपोर्ट साइज फोटो।',
              'Step 2 — अपने स्थानीय ग्राम पंचायत / वार्ड कार्यालय जाएं और IGNOAPS आवेदन पत्र (Form P-1) मांगें।',
              'Step 3 — अधिकारी की मदद से फॉर्म भरें। सभी दस्तावेजों की स्व-प्रमाणित प्रतियां संलग्न करें।',
              'Step 4 — कार्यालय में फॉर्म जमा करें और रसीद लें। सत्यापन के बाद 60 दिनों में आपकी पेंशन शुरू हो जाएगी।'
            ]
          : data.age < 60
          ? ['आपकी आयु 60 वर्ष से कम है। IGNOAPS के लिए आवेदन करने के लिए 60 वर्ष का होना आवश्यक है।']
          : ['पहले BPL कार्ड के लिए आवेदन करें।']
      });
      setCurrentView('result');
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1>🚶‍♂️ दिग्दर्शन सारथी</h1>
        <p>AI-powered Government Services Helper</p>
      </header>

      {/* Home View */}
      {currentView === 'home' && (
        <div>
          {/* Service Selection */}
          <div className="service-grid">
            <div
              className="service-card"
              onClick={() => setCurrentView('voice')}
            >
              <div className="service-icon">🏛️</div>
              <h3>पेंशन सहायता</h3>
              <p>IGNOAPS के लिए जांच करें</p>
            </div>

            <div
              className="service-card"
              onClick={() => setCurrentView('document')}
            >
              <div className="service-icon">📇</div>
              <h3>दस्तावेज जांच</h3>
              <p>आधार कार्ड स्कैन करें</p>
            </div>

            <div
              className="service-card"
              onClick={() => {
                setExtractedData({
                  name: 'Ramkali Devi',
                  age: 72,
                  has_bpl: true,
                  gender: 'Female',
                  dob: '12/03/1954'
                });
                checkEligibility({
                  name: 'Ramkali Devi',
                  age: 72,
                  has_bpl: true,
                  gender: 'Female',
                  dob: '12/03/1954'
                });
              }}
            >
              <div className="service-icon">⚡</div>
              <h3>त्वरित डेमो</h3>
              <p>पूर्ण प्रक्रिया देखें</p>
            </div>
          </div>

          {/* Voice Button */}
          <div style={{ textAlign: 'center', marginTop: '32px' }}>
            <p style={{ fontSize: '18px', marginBottom: '16px', color: '#666' }}>
              या बस बोलें:
            </p>
            <button
              className="btn btn-primary btn-large"
              onClick={() => setCurrentView('voice')}
              style={{ maxWidth: '300px', margin: '0 auto' }}
            >
              🎤 बोलना शुरू करें
            </button>
          </div>
        </div>
      )}

      {/* Voice View */}
      {currentView === 'voice' && (
        <VoiceInterface
          onQuery={handleVoiceQuery}
          isLoading={isLoading}
          lastResponse={voiceResponse}
        />
      )}

      {/* Document View */}
      {currentView === 'document' && (
        <DocUpload
          onDocumentUpload={handleDocumentUpload}
          isLoading={isLoading}
          extractedData={extractedData || undefined}
        />
      )}

      {/* Result View */}
      {currentView === 'result' && eligibilityResult && (
        <ResultCard
          eligible={eligibilityResult.eligible}
          scheme={eligibilityResult.scheme}
          verdict={eligibilityResult.verdict}
          reasons={eligibilityResult.reasons}
          steps={eligibilityResult.steps}
          warning={eligibilityResult.warning}
        />
      )}

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <button
          className={`nav-item ${currentView === 'home' ? 'active' : ''}`}
          onClick={() => setCurrentView('home')}
        >
          <span>🏠</span>
          होम
        </button>
        <button
          className={`nav-item ${currentView === 'voice' ? 'active' : ''}`}
          onClick={() => setCurrentView('voice')}
        >
          <span>🎤</span>
          बोलें
        </button>
        <button
          className={`nav-item ${currentView === 'document' ? 'active' : ''}`}
          onClick={() => setCurrentView('document')}
        >
          <span>📷</span>
          स्कैन
        </button>
      </nav>

      {/* Spacer for bottom nav */}
      <div style={{ height: '80px' }}></div>
    </div>
  );
}

export default App;