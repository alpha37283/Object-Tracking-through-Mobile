import { useEffect, useRef } from 'react';
import { socket } from '../websocket';

export default function LaptopView() {
  const canvasRef = useRef(null);

  useEffect(() => {
    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'frame') {
          const ctx = canvasRef.current.getContext('2d');
          const img = new Image();
          img.onload = () => {
            canvasRef.current.width = img.width;
            canvasRef.current.height = img.height;
            ctx.drawImage(img, 0, 0);
          };
          img.src = message.data;
        }
      } catch (err) {
        console.warn('Invalid data received:', err);
      }
    };
  }, []);

  const handleClick = (event) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    socket.send(JSON.stringify({ type: 'click', x, y }));
  };

  return (
    <canvas
      ref={canvasRef}
      onClick={handleClick}
      style={{
        width: '100%',
        border: '1px solid #ccc',
        cursor: 'crosshair',
        display: 'block',
      }}
    />
  );
}
