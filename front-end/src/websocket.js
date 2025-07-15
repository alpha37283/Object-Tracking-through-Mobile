//export const socket = new WebSocket(`ws://284bcbe8d7e5.ngrok-free.app`);


export const socket = new WebSocket("wss://284bcbe8d7e5.ngrok-free.app/ws");



socket.onopen = () => {
  console.log("WebSocket connected ✅");
};

socket.onclose = () => {
  console.log("WebSocket disconnected ❌");
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};
