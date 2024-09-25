import socket
import threading
import time
from datetime import datetime

keys = {}

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
            elif data.lower().startswith("set"):
                data_arr = data.split(" ")
                key, value = data_arr[1], data_arr[2]
                final_value = [value]
                if "px" in data.lower():
                    ttl = int(data_arr[4])
                    curr_time = datetime.now()
                    final_value.append(curr_time)
                    final_value.append(ttl)
                keys[key] = tuple(final_value)
                client_socket.send("OK\r\n".encode())
            elif data.lower().startswith("get"):
                _, key = data.split(" ")
                if len(list(keys[key])) > 1:
                    curr_time = datetime.now()
                    recorded_time = keys[key][1]
                    diff = curr_time - recorded_time
                    milliseconds_diff = diff.total_seconds() * 1000
                    ttl = keys[key][2]
                    if milliseconds_diff >= ttl:
                        del keys[key]  
                        client_socket.send("-1\r\n".encode())
                        return
                value = keys[key][0]
                client_socket.send(f"{value}\r\n".encode())

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
