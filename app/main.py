import socket
import threading

def handle_client(client_socket: socket.socket, address: tuple) -> None:
    with client_socket:
        print(f"Connection from {address} has been established!")
        while True:
            request: bytes = client_socket.recv(512)
            if not request:
                break
            data: str = request.decode().strip()
            print(f"Received: {data} from {address}")

            if "ping" in data.lower():
                client_socket.send(b"+PONG\r\n")
            elif data.lower().startswith("echo"):
                message = data[5:].strip()
                client_socket.send(f"${len(message)}\r\n{message}\r\n".encode())

def main():
    print("Server is starting...")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=[client_socket, addr])
        client_thread.start()

if __name__ == "__main__":
    main()
