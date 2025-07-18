import React, { useEffect, useRef, useState } from "react";
import { connectWebSocket, sendMessage } from "../../websocket";

export default function MobileCam() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const dotRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Set up WebSocket connection
    connectWebSocket("mobile", (event) => {
      const video = videoRef.current;
      try {
        const { x, y } = JSON.parse(event.data);
        if (video && dotRef.current) {
          dotRef.current.style.left = `${x * video.clientWidth}px`;
          dotRef.current.style.top = `${y * video.clientHeight}px`;
          dotRef.current.style.display = "block";
        }
      } catch (e) {
        // Not a coordinate message, hide dot
        if (dotRef.current) dotRef.current.style.display = "none";
      }
    });
    setIsConnected(true);

    return () => {
      // Cleanup WebSocket if needed
    };
  }, []);

  useEffect(() => {
    if (!isConnected) return;

    // Access the camera
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      })
      .catch((err) => console.error("Camera access error:", err));

    // Capture and send video frames
    const captureFrame = () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (video && canvas) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        canvas.toBlob(
          (blob) => {
            sendMessage(blob); // Send frame to WebSocket
          },
          "image/jpeg",
          0.7 // Lower quality for less bandwidth
        );
      }
      setTimeout(captureFrame, 150); // ~10 fps
    };
    captureFrame();
  }, [isConnected]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100vh" }}>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
      <canvas ref={canvasRef} style={{ display: "none" }} />
      <div
        ref={dotRef}
        style={{
          position: "absolute",
          width: "10px",
          height: "10px",
          backgroundColor: "red",
          borderRadius: "50%",
          transform: "translate(-50%, -50%)",
          pointerEvents: "none",
        }}
      />
    </div>
  );
}