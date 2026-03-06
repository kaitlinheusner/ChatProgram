import socket 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 10293))

server.listen(5)
print("The server is listening")

clients = []
lock = threading.Lock()

def broadcast(message, sender=None):
    with lock:
        for client in clients:
            if client is sender:
                continue

            try: 
                client.sendall(message.encode("utf-8"))

            except OSError:
                clients.remove(client)

def handle_client(conn, addr):
    conn.sendall("Enter your username: ".encode("utf-8"))
    username = conn.recv(1024).decode("utf-8").strip()

    print(f"{username} joined from {addr}")
    broadcast(f"{username} has joined the chat!\n", sender=conn)

    while True:
        try: 
            data = conn.recv(1024)

        except(ConnectionResetError, OSError):
            with lock:
                if conn in clients:
                    clients.remove(conn)
            conn.close()
            broadcast(f"{username} has left the chat.\n")
            print(f"{username} disconnected")
            break

        if not data:
            with lock:
                clients.remove(conn)
            conn.close()
            broadcast(f"{username} has left the chat.\n")
            print(f"{username} disconnected")
            break

        message = data.decode("utf-8")

        if message == "/quit":
            with lock:
                clients.remove(conn)
            conn.close()
            broadcast(f"{username} has left the chat.\n")
            break

        print(f"[{username}]: {message}")
        broadcast(f"[{username}]: {message}\n", sender=conn)

while True:
    conn, addr = server.accept()
    with lock:
        clients.append(conn)
    thread = threading.Thread(target= handle_client, args=(conn, addr))
    thread.daemon = True
    thread.start()
  