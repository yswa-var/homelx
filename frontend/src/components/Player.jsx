import { useState, useRef, useEffect } from 'react';

const Player = ({ audioBlob, autoPlay = true }) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioBlob) {
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
      
      return () => {
        URL.revokeObjectURL(url);
      };
    }
  }, [audioBlob]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.addEventListener('play', () => setIsPlaying(true));
      audioRef.current.addEventListener('pause', () => setIsPlaying(false));
      audioRef.current.addEventListener('ended', () => setIsPlaying(false));
      audioRef.current.addEventListener('timeupdate', handleTimeUpdate);
      audioRef.current.addEventListener('loadedmetadata', handleLoadedMetadata);
      audioRef.current.addEventListener('volumechange', updateVolumeFromAudio);
    }
  }, [audioUrl]);

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const updateVolumeFromAudio = () => {
    if (audioRef.current) {
      setVolume(audioRef.current.volume);
    }
  };

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
    }
  };

  const handleSeek = (e) => {
    if (audioRef.current) {
      const rect = e.currentTarget.getBoundingClientRect();
      const percent = (e.clientX - rect.left) / rect.width;
      const newTime = percent * duration;
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.volume = newVolume;
      setVolume(newVolume);
    }
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  if (!audioUrl) {
    return null;
  }

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={audioUrl}
        autoPlay={autoPlay}
        style={{ display: 'none' }}
      />
      
      <div className="audio-controls">
        <button
          onClick={togglePlay}
          className={`play-button ${isPlaying ? 'playing' : ''}`}
          title={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? '⏸️' : '▶️'}
        </button>
        
        <div className="audio-progress">
          <div className="progress-bar" onClick={handleSeek}>
            <div 
              className="progress-fill"
              style={{ width: `${(currentTime / duration) * 100}%` }}
            ></div>
            <div 
              className="progress-handle"
              style={{ left: `${(currentTime / duration) * 100}%` }}
            ></div>
          </div>
          <div className="time-display">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>
        
        <div className="volume-control">
          <span className="volume-icon">🔊</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={handleVolumeChange}
            className="volume-slider"
            title="Volume"
          />
        </div>
      </div>
      
      <div className="audio-info">
        <span>AI Response</span>
        <span className="audio-duration">{formatTime(duration)}</span>
      </div>
    </div>
  );
};

export default Player; 