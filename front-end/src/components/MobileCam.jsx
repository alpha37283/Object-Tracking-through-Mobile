import { useEffect, useRef, useState } from 'react';
import { socket } from '../websocket';

export default function MobileCam() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [dot, setDot] = useState(null); // dot is { x, y }

  useEffect(() => {
    // Get webcam access
   navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    videoRef.current.srcObject = stream;
    console.log('Camera stream started');
  })
  .catch((err) => {
    console.error('Error accessing camera:', err.name, err.message);
    alert('Camera access failed: ' + err.message);
  });



    // Listen for incoming WebSocket messages
    socket.onmessage = (event) => {
      try {
        const { x, y } = JSON.parse(event.data);
        if (typeof x === 'number' && typeof y === 'number') {
          setDot({ x, y });
        }
      } catch (e) {
        console.warn('Invalid message:', event.data);
      }
    };

    // Periodically send camera frame
    const interval = setInterval(() => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      if (!canvas || !video) return;

      const ctx = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);
      const frame = canvas.toDataURL('image/jpeg', 0.5);
      socket.send(JSON.stringify({ type: 'frame', data: frame }));
    }, 100);

    return () => clearInterval(interval);
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
