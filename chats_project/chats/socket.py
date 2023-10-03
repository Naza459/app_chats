import websocket

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("Connection closed")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/conversations/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                timeout=5)  # Establece un timeout de 5 segundos
    ws.run_forever()