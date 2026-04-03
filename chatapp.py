import socket
import threading
def broadcast(message, sender, clients):
    for client in clients:
        if client != sender:
            client.send(message.encode())
def start_server():
    clients = []
    def handle_client(client_socket, address):
        print(f"[CONNECTED] {address}")
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"{address}: {message}")
                broadcast(f"{address}: {message}", client_socket, clients)
            except:
                break
        print(f"[DISCONNECTED] {address}")
        clients.remove(client_socket)
        client_socket.close()
    def server_send():
        while True:
            msg = input("")
            broadcast(f"SERVER: {msg}", None, clients)
            print(f"SERVER: {msg}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen()
    print("Server started... Waiting for users...")
    threading.Thread(target=server_send, daemon=True).start()
    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 5000))
    print("Connected to server!")
    def receive():
        while True:
            try:
                msg = client.recv(1024).decode()
                print("\n" + msg)
            except:
                break
    def send():
        while True:
            client.send(input("").encode())
    threading.Thread(target=receive, daemon=True).start()
    threading.Thread(target=send, daemon=True).start()
    while True:
        pass
print("Chat Application\n1. Server\n2. Client")
choice = input("Choose (1/2): ")
if choice == "1":
    start_server()
elif choice == "2":
    start_client()
else:
    print("Invalid choice!")