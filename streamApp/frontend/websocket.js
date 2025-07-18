let ws;

export function connectWebSocket(role, onMessage) {
  // Use ngrok domain if available, otherwise fallback to window.location.hostname
  const ngrokHost = 'b7be4e1f8a74.ngrok-free.app';
  const isNgrok = window.location.hostname === ngrokHost;
  const wsProtocol = isNgrok ? 'wss' : 'ws';
  const wsHost = isNgrok ? ngrokHost : window.location.hostname;
  ws = new WebSocket(`${wsProtocol}://${wsHost}:8765`);
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