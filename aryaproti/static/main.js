// Backend setup (Node.js with Express and Socket.IO)
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*", // Change this to your frontend URL in production
    methods: ["GET", "POST"]
  }
});

// When a client connects
io.on('connection', (socket) => {
  console.log('Client connected');
  
  // Send initial status
  socket.emit('status', { text: '✅ Connected — Waiting for voice commands…' });
  
  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

// Function to send log messages to all connected clients
function sendLogMessage(who, text) {
  io.emit('log', { who, text });
  console.log(`${who}: ${text}`); // This will show in your VS Code terminal
}

// Function to update status
function updateStatus(text) {
  io.emit('status', { text });
}

// Function to control hologram
function toggleHologram(on) {
  io.emit('holo', { on });
}

// Start server
server.listen(3000, () => {
  console.log('Server running on port 3000');
});