const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Middleware personalizado para agregar encabezados CORS
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8000'); // Reemplaza la URL con la correcta
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});


// Configura la ruta para la vista del usuario

// Maneja la conexión de un cliente Socket.IO
io.on('connection', (socket) => {
  console.log("Cliente conectado", socket.id);

  // Maneja el evento de unirse a una sala de chats
  socket.on("join_room", (roomName) => {
    console.log(`El cliente ${socket.id} se ha unido a la sala ${roomName}`);
    socket.join(roomName);
  });

  // Maneja el evento de mensaje enviado desde el usuario
  socket.on("mensajeUsuario", (mensaje) => {
    console.log("Mensaje recibido del usuario:", mensaje);

    // Emite el mensaje al cliente
    io.emit("mensajeCliente", mensaje);
  });

  // Maneja el evento de mensaje enviado desde el cliente
  socket.on("mensajeCliente", (mensaje) => {
    console.log("Mensaje recibido del cliente:", mensaje);

    // Emite el mensaje al usuario
    io.emit("mensajeUsuario", mensaje);
  });

  // Maneja la desconexión de un cliente Socket.IO
  socket.on("disconnect", (socket) => {
    console.log("Cliente desconectado", socket.id);
  });
});

// Inicia el servidor
const port = 4000;
server.listen(port, () => {
  console.log(`Servidor Socket.IO en funcionamiento en el puerto ${port}`);
});