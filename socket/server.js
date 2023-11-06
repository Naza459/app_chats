const express = require("express");
const app = express();
const http = require("http");
const cors = require("cors");
const socketIO = require("socket.io");

// Configura el servidor HTTP
const server = http.createServer(app);

// Configura CORS para permitir solicitudes desde cualquier origen (*)
app.use(cors());

// Inicializa Socket.IO y permite solicitudes CORS
const io = socketIO(server, {
  cors: {
    origin: "*",
  },
});

// Maneja la conexión de un cliente Socket.IO
io.on("connection", (socket) => {
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

  // Maneja el evento de mensaje de escritura desde el usuario
  socket.on("typing", (name) => {
    console.log("Escribiendo:", name);

    // Emite el mensaje al cliente
    io.emit("typingCliente", name);
  });

  // Maneja la desconexión de un cliente Socket.IO
  socket.on("disconnect", () => {
    console.log("Cliente desconectado", socket.id);
  });
});

// Inicia el servidor en el puerto 4000
const port = 4000;
server.listen(port, () => {
  console.log(`Servidor Socket.IO en funcionamiento en el puerto ${port}`);
});
