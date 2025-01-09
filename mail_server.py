import socket
import datetime
import threading

PORT = 3939
BUFSIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("", PORT))
server.listen()

print("Started multi-threaded server")


def handle_connection(client):
    thread_id = threading.get_ident()

    response = f"Hello from thread {thread_id}\n".encode("utf-8")
    client.sendall(response)

    data = client.recv(BUFSIZE)
    print(data.decode("UTF-8"))

    client.close()


while True:
    client, address = server.accept()
    print(str(datetime.datetime.now()), "接続要求あり")

    thread = threading.Thread(target=handle_connection, args=[client])
    thread.start()
