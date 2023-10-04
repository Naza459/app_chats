import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { io } from 'socket.io-client';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  socket: any;
  message: string | null = '';
  messages: string[] = [];
  chatsUsuario: any[] = [];
  chatsCliente: any[] = [];

  constructor(private http: HttpClient) { } // Inyecta el servicio HttpClient

  ngOnInit() {
    this.socket = io('http://localhost:3000');

    this.socket.on('mensajeCliente', (mensaje: string) => {
      this.messages.push(mensaje);
    });

    // Llama a las funciones getChatsUsuario y getChatsCliente cuando se inicia el componente
    this.getChatsUsuario();
    this.getChatsCliente();
  }

  updateMessage(event: Event) {
    const target = event.target as HTMLInputElement;
    this.message = target.value;
  }

  enviarMensaje(message: string, type_messages: string, user: string, client: string) {
  if (message) {
    const urlCliente = 'http://127.0.0.1:8000/chats/chats_Cliente/';
    const urlUsuario = 'http://127.0.0.1:8000/chats/chats_usuario/';

    const url = user === 'usuario' ? urlUsuario : urlCliente;

    const body = {
      messages: message,
      type_messages: type_messages,
      user: user,
      client: client
    };

    this.http.post(url, body).subscribe((response: any) => {
      // Maneja la respuesta aquí si es necesario
    });

    this.message = '';
  }
}

  // Función para obtener los chats del usuario
  getChatsUsuario() {
    const url = 'http://127.0.0.1:8000/chats/chats_usuario/';

    this.http.get(url).subscribe((data: any) => {
      this.chatsUsuario = data; // Asigna los datos a la propiedad chatsUsuario
    });
  }

  // Función para obtener los chats del cliente
  getChatsCliente() {
    console.log('GET CLIENTE')
    const url = 'http://127.0.0.1:8000/chats/chats_Cliente/';

    this.http.get(url).subscribe((data: any) => {
      this.chatsCliente = data; // Asigna los datos a la propiedad chatsCliente
    });
  }
}
