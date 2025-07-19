let ws;

export function connectWebSocket(role, onMessage) {
  // Always use new ngrok backend for WebSocket
  ws = new WebSocket('wss://72da959561a7.ngrok-free.app:8765');
  ws.onopen = () => {
    ws.send(role); // Identify as "mobile" or "laptop"
    console.log(`${role} WebSocket connected`);
  };
  ws.onmessage = onMessage;
  ws.onclose = () => console.log("WebSocket closed");
  ws.onerror = (error) => console.error("WebSocket error:", error);
}

export function sendMessage(message) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(message);
  }
}