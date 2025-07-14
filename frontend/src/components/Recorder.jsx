import { useState, useRef, useEffect } from 'react';
import { getApiUrl } from '../config';

const Recorder = ({ onTranscription }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    if (isRecording) {
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } else {
      setRecordingTime(0);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isRecording]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await transcribeAudio(audioBlob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Error accessing microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const transcribeAudio = async (audioBlob) => {
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'recording.webm');

      const response = await fetch(getApiUrl('/transcribe'), {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      onTranscription(data.text);
    } catch (error) {
      console.error('Error transcribing audio:', error);
      alert('Error transcribing audio. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="recorder">
      <div className="recorder-container">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
          className={`record-button ${isRecording ? 'recording' : ''} ${isProcessing ? 'processing' : ''}`}
          title={isProcessing ? 'Processing...' : isRecording ? 'Stop Recording' : 'Start Recording'}
        >
          {isProcessing ? (
            <div className="processing-spinner">
              <div className="spinner"></div>
            </div>
          ) : isRecording ? (
            <span className="stop-icon">⏹️</span>
          ) : (
            <span className="mic-icon">🎙️</span>
          )}
        </button>
        
        {isRecording && (
          <div className="recording-info">
            <div className="recording-indicator">
              <div className="waveform">
                {[...Array(5)].map((_, i) => (
                  <div 
                    key={i} 
                    className="wave-bar"
                    style={{
                      animationDelay: `${i * 0.1}s`,
                      height: `${20 + Math.random() * 30}px`
                    }}
                  ></div>
                ))}
              </div>
              <span className="recording-text">Recording {formatTime(recordingTime)}</span>
            </div>
          </div>
        )}
        
        {isProcessing && (
          <div className="processing-info">
            <div className="processing-spinner-small"></div>
            <span>Processing audio...</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recorder; 