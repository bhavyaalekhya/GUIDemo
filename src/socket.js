// socket.js
import { w3cwebsocket } from "websocket";

const socket = new w3cwebsocket('ws://localhost:8000');
const listeners = {};

socket.onopen = () => console.log("Connected to WebSocket");
socket.onclose = () => console.log("Disconnected from WebSocket");
socket.onerror = (error) => console.error("WebSocket error:", error);

socket.onmessage = (message) => {
  const server_message = JSON.parse(message.data);
  const message_type = server_message.type;
  
  if (listeners[message_type]) {
    listeners[message_type].forEach(callback => callback(server_message.details));
  }
};

const addListener = (messageType, callback) => {
  if (!listeners[messageType]) {
    listeners[messageType] = [];
  }
  listeners[messageType].push(callback);
};

const removeListener = (messageType, callback) => {
  if (listeners[messageType]) {
    listeners[messageType] = listeners[messageType].filter(cb => cb !== callback);
  }
};

const sendMessage = (messageType, data) => {
  if (socket.readyState === socket.OPEN) {
    socket.send(JSON.stringify({ type: messageType, details: data }));
  } else {
    console.error('WebSocket is not open.');
  }
};

export {
  addListener,
  removeListener,
  sendMessage
};
