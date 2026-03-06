import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 10293))
print("Connected to server!")

def receive_messages():
    while True:
        try: 
            data = client.recv(1024)

            if not data:
                print("\r── Server closed the connection ──")
                break
            
            message = data.decode("utf-8").strip()
            print(f"\r── {message} ──")
            print("You: ", end='', flush=True)

        except EOFError:
            break

recv_thread = threading.Thread(target=receive_messages)
recv_thread.daemon = True
recv_thread.start()

while True:
    print("You: ", end='', flush=True)

    try: 
        message = input()

    except OSError:
        break

    if not message: 
        continue

    client.sendall(message.encode("utf-8"))
    
    if message == "/quit":
        break

client.close()
