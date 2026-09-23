import React, { useState } from 'react';

interface VoiceInterfaceProps {
  onQuery: (query: string) => void;
  isLoading: boolean;
  lastResponse?: string;
}

export const VoiceInterface: React.FC<VoiceInterfaceProps> = ({ onQuery, isLoading, lastResponse }) => {
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleVoiceClick = () => {
    if (!isListening) {
      setIsListening(true);
      // In real app: use Web Speech API here
      // For demo: simulate listening
      setTimeout(() => {
        setIsListening(false);
        setText('Mujhe pension ke baare mein batayein'); // Example query
      }, 2000);
    }
  };

  return (
    <div className="card">
      <h2 style={{ textAlign: 'center', marginBottom: '16px', fontSize: '24px' }}>
        🎤 बोलें — मैं सुन रहा हूं
      </h2>

      <div style={{ textAlign: 'center' }}>
        <button
          className={`voice-btn ${isListening ? 'listening' : ''}`}
          onClick={handleVoiceClick}
          disabled={isLoading}
          aria-label={isListening ? 'वॉइस इनपुट रुका जा रहा है' : 'वॉइस इनपुट शुरू करें'}
        >
          {isListening ? '⏹' : '🎤'}
        </button>

        {isListening && (
          <div className="voice-wave">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}

        <p style={{ fontSize: '18px', color: '#666', marginBottom: '16px' }}>
          या टाइप करें:
        </p>

        <textarea
          className="input-field"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="यहां लिखें... जैसे: मुझे पेंशन के बारे में बताइए"
          rows={3}
          style={{ minHeight: '80px', resize: 'none' }}
          aria-label="टेक्स्ट क्वेरी इनपुट"
        />

        <div style={{ marginTop: '16px' }}>
          <button
            className="btn btn-primary btn-large"
            onClick={() => text && onQuery(text)}
            disabled={isLoading || !text.trim()}
            style={{ width: '100%' }}
          >
            {isLoading ? '⏳ जांच हो रही है...' : 'चलिए शुरू करते हैं ▶'}
          </button>
        </div>

        {lastResponse && (
          <div style={{
            marginTop: '20px',
            padding: '16px',
            background: '#e8f5e9',
            borderRadius: '12px',
            border: '2px solid #2e7d32'
          }}>
            <p style={{ margin: 0, fontSize: '18px', fontWeight: 600, color: '#2e7d32' }}>
              ✓ कहा: "{lastResponse}"
            </p>
          </div>
        )}
      </div>
    </div>
  );
};