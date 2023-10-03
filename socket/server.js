const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);

// Configurar eventos WebSocket
io.on('connection', (socket) => {
  console.log('Cliente conectado al servidor WebSocket');

  // Escuchar eventos del cliente
  socket.on('message', (message) => {
    console.log('Mensaje recibido del cliente:', message);
    // Procesar el mensaje recibido desde el cliente

    // Enviar una respuesta al cliente
    socket.emit('message', 'Respuesta del servidor WebSocket');
  });

  socket.on('disconnect', () => {
    console.log('Cliente desconectado del servidor WebSocket');
  });
});

// Resto de tu código de configuración de Express

// Iniciar el servidor
server.listen(3000, () => {
  console.log('Servidor Express en ejecución');
});