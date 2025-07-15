export const socket = new WebSocket(`ws://192.168.100.216:8765`);



socket.onopen = () => {
  console.log("WebSocket connected ✅");
};

socket.onclose = () => {
  console.log("WebSocket disconnected ❌");
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};
