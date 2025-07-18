import React, { useEffect, useRef } from "react";
import { connectWebSocket, sendMessage } from "../../websocket";

export default function LaptopView() {
  const canvasRef = useRef(null);

  useEffect(() => {
    // Set up WebSocket connection
    connectWebSocket("laptop", (event) => {
      const img = new Image();
      img.onload = () => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0); // Render received frame
      };
      img.src = URL.createObjectURL(event.data); // Convert blob to image
    });

    return () => {
      // Cleanup WebSocket if needed
    };
  }, []);

  const handleClick = (event) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    // Normalize coordinates to [0, 1]
    const x = (event.clientX - rect.left) / canvas.width;
    const y = (event.clientY - rect.top) / canvas.height;
    sendMessage(JSON.stringify({ x, y })); // Send to WebSocket
  };

  return (
    <canvas
      ref={canvasRef}
      onClick={handleClick}
      style={{ width: "100%", height: "100vh", objectFit: "contain" }}
    />
  );
}