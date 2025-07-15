import { useEffect, useRef, useState } from 'react';
import { socket } from '../websocket';

export default function MobileCam() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [dot, setDot] = useState(null);
  const [cameraStarted, setCameraStarted] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    let stream;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((mediaStream) => {
        stream = mediaStream;
        videoRef.current.srcObject = stream;
        setCameraStarted(true);
        console.log('✅ Camera started');
      })
      .catch((err) => {
        console.error('Camera access error:', err);
        setError(err.message);
        setCameraStarted(false);
      });

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  useEffect(() => {
  let stream;

  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((mediaStream) => {
      stream = mediaStream;

      const tryAssign = () => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          setCameraStarted(true);
          console.log('✅ Camera started');
        } else {
          requestAnimationFrame(tryAssign);
        }
      };

      tryAssign();
    })
    .catch((err) => {
      console.error('Camera access error:', err);
      setError(err.message);
      setCameraStarted(false);
    });

  return () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
  };
}, []);

 

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      <video
        ref={videoRef}
        autoPlay
        muted
        playsInline
        style={{ width: '100%' }}
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      {dot && (
        <div
          style={{
            position: 'absolute',
            left: `${dot.x}px`,
            top: `${dot.y}px`,
            width: 10,
            height: 10,
            borderRadius: '50%',
            backgroundColor: 'red',
            transform: 'translate(-50%, -50%)',
          }}
        />
      )}
    </div>
  );
}
