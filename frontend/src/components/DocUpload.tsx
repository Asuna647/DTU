import React, { useState } from 'react';

interface DocUploadProps {
  onDocumentUpload: (file: File | null, useDemo: boolean) => void;
  isLoading: boolean;
  extractedData?: {
    name: string;
    age: number;
    has_bpl: boolean;
    gender: string;
    dob: string;
  };
}

export const DocUpload: React.FC<DocUploadProps> = ({ onDocumentUpload, isLoading, extractedData }) => {
  const [demoMode, setDemoMode] = useState(true);

  return (
    <div className="card">
      <h2 style={{ textAlign: 'center', marginBottom: '16px', fontSize: '24px' }}>
        📷 दस्तावेज स्कैन करें
      </h2>

      <p style={{ fontSize: '18px', textAlign: 'center', marginBottom: '20px', color: '#666' }}>
        अपना आधार कार्ड स्कैन करें या डेमो मोड का उपयोग करें
      </p>

      {/* Demo Mode Toggle */}
      <div className="tts-toggle" style={{ justifyContent: 'space-between' }}>
        <span style={{ fontSize: '18px', fontWeight: 600 }}>🔧 डेमो मोड</span>
        <div
          className={`toggle-switch ${demoMode ? 'active' : ''}`}
          onClick={() => setDemoMode(!demoMode)}
          role="switch"
          aria-checked={demoMode}
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && setDemoMode(!demoMode)}
        />
      </div>

      {extractedData ? (
        // Show extracted data
        <div className="result-section">
          <h3 style={{ fontSize: '22px', color: '#1a5f2a', marginBottom: '16px' }}>
            📋 निकले हुए विवरण:
          </h3>

          <div className="info-row">
            <span className="info-label">नाम:</span>
            <span className="info-value">{extractedData.name}</span>
          </div>
          <div className="info-row">
            <span className="info-label">उम्र:</span>
            <span className="info-value">{extractedData.age} वर्ष</span>
          </div>
          <div className="info-row">
            <span className="info-label">लिंग:</span>
            <span className="info-value">{extractedData.gender}</span>
          </div>
          <div className="info-row">
            <span className="info-label">जन्म तिथि:</span>
            <span className="info-value">{extractedData.dob}</span>
          </div>
          <div className="info-row">
            <span className="info-label">BPL स्टेटस:</span>
            <span className={`info-value ${extractedData.has_bpl ? 'success' : 'error'}`}>
              {extractedData.has_bpl ? '✓ हां' : '✗ नहीं'}
            </span>
          </div>

          <button
            className="btn btn-outline"
            onClick={() => window.location.reload()}
            style={{ marginTop: '16px', width: '100%' }}
          >
            🔄 दस्तावेज दोबारा स्कैन करें
          </button>
        </div>
      ) : (
        // Upload area
        <div className="doc-preview">
          <div className="doc-preview-icon">📇</div>
          <p style={{ fontSize: '18px', marginBottom: '16px' }}>
            {demoMode
              ? 'डेमो मोड में हम सैंपल डेटा का उपयोग करेंगे'
              : 'अपना आधार कार्ड फोटो अपलोड करें'
            }
          </p>

          {isLoading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
            </div>
          ) : (
            <button
              className="btn btn-primary btn-large"
              onClick={() => onDocumentUpload(null, demoMode)}
              style={{ width: '100%', maxWidth: '300px', margin: '0 auto' }}
            >
              {demoMode ? '🎭 डेमो डेटा दिखाएं' : '📤 दस्तावेज अपलोड करें'}
            </button>
          )}
        </div>
      )}
    </div>
  );
};