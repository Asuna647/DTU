import React, { useState, useEffect } from 'react';

interface Step {
  step: string;
}

interface ResultCardProps {
  eligible: boolean;
  scheme: string;
  verdict: string;
  reasons: string[];
  steps: string[];
  warning?: string;
}

export const ResultCard: React.FC<ResultCardProps> = ({
  eligible,
  scheme,
  verdict,
  reasons,
  steps,
  warning
}) => {
  const [speakEnabled, setSpeakEnabled] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  // Auto-advance through steps
  useEffect(() => {
    if (steps.length > 0) {
      const timer = setInterval(() => {
        setCurrentStep(prev => (prev + 1) % steps.length);
      }, 4000);
      return () => clearInterval(timer);
    }
  }, [steps.length]);

  // Text-to-speech effect
  useEffect(() => {
    if (speakEnabled && (reasons.length > 0 || steps.length > 0)) {
      const utterance = new SpeechSynthesisUtterance(
        eligible ? verdict + ". " + steps[currentStep] : reasons.join(". ")
      );
      utterance.lang = 'hi-IN';
      utterance.rate = 0.8;
      speechSynthesis.speak(utterance);
    }
  }, [speakEnabled, currentStep, eligible, reasons, steps, verdict]);

  const speakText = (text: string) => {
    if (speakEnabled) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'hi-IN';
      utterance.rate = 0.8;
      speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="result-section">
      {/* Status Badge */}
      <div className={`status-badge ${eligible ? 'success' : 'error'}`}>
        {eligible ? '✓ पात्र' : '✗ अपात्र'}
      </div>

      {/* Scheme Title */}
      <h2 style={{ fontSize: '28px', color: '#1a5f2a', marginBottom: '8px' }}>
        {scheme === 'IGNOAPS' ? '🏛️ इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना' : scheme}
      </h2>

      {/* Verdict */}
      <h3 style={{ fontSize: '24px', marginBottom: '16px' }}>
        {verdict}
      </h3>

      {/* TTS Toggle */}
      <div className="tts-toggle">
        <span style={{ fontSize: '18px', fontWeight: 600 }}>🔊 आवाज़ में सुनें</span>
        <div
          className={`toggle-switch ${speakEnabled ? 'active' : ''}`}
          onClick={() => setSpeakEnabled(!speakEnabled)}
          role="switch"
          aria-checked={speakEnabled}
          tabIndex={0}
        />
      </div>

      {/* Reasons */}
      {reasons.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ fontSize: '20px', marginBottom: '12px' }}>📝 जांच परिणाम:</h4>
          {reasons.map((reason, idx) => (
            <p
              key={idx}
              style={{
                fontSize: '18px',
                marginBottom: '8px',
                paddingLeft: '8px',
                borderLeft: reason.includes('✔') ? '3px solid #2e7d32' : '3px solid #b71c1c',
                cursor: speakEnabled ? 'pointer' : 'default'
              }}
              onClick={() => speakEnabled && speakText(reason)}
            >
              {reason}
            </p>
          ))}
        </div>
      )}

      {/* Steps - Only show if eligible */}
      {eligible && steps.length > 0 && (
        <div>
          <h4 style={{ fontSize: '20px', marginBottom: '12px' }}>
            📋 अगले कदम ({currentStep + 1}/{steps.length}):
          </h4>

          <div className="step-list">
            {steps.slice(0, currentStep + 1).map((step, idx) => (
              <div key={idx} className="step-item" style={{
                background: idx === currentStep ? '#fff8e1' : '#f9f9f9',
                borderLeftColor: idx === currentStep ? '#d4a017' : '#1a5f2a'
              }}>
                <span className="step-number">{idx + 1}</span>
                <div className="step-content">
                  <p
                    style={{ cursor: speakEnabled ? 'pointer' : 'default' }}
                    onClick={() => speakEnabled && speakText(step)}
                  >
                    {step.replace(/^Step \d+ — /, '')}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Progress Indicator */}
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '8px',
            marginTop: '16px'
          }}>
            {steps.map((_, idx) => (
              <div
                key={idx}
                style={{
                  width: '12px',
                  height: '12px',
                  borderRadius: '50%',
                  background: idx <= currentStep ? '#1a5f2a' : '#ccc'
                }}
              />
            ))}
          </div>
        </div>
      )}

      {/* Warning */}
      {warning && (
        <div className="warning-box">
          <p>⚠️ {warning}</p>
        </div>
      )}
    </div>
  );
};