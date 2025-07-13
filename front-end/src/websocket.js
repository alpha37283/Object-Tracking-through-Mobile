export const socket = new WebSocket(`wss://${window.location.host}/ws`);

socket.onopen = () => {
  console.log("WebSocket connected ✅");
};

socket.onclose = () => {
  console.log("WebSocket disconnected ❌");
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};
