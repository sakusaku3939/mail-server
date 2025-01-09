import base64
import socket
import datetime
import threading

SMTP_PORT = 3939
POP_PORT = 2414
BUFSIZE = 4096

smtp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pop_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

smtp_server.bind(("", SMTP_PORT))
smtp_server.listen()
print("Started SMTP server")

pop_server.bind(("", POP_PORT))
pop_server.listen()
print("Started POP server")


def handle_connection_smtp(client):
    thread_id = threading.get_ident()
    print(f"[SMTP] Handling connection in thread {thread_id}")

    response = f"SMTP Hello from thread {thread_id}\n".encode("utf-8")
    client.sendall(response)

    data = client.recv(BUFSIZE)
    print(f"[SMTP] Received: {data.decode('utf-8')}")

    split_texts = data.decode('utf-8').split(";")
    print(split_texts)

    from_name_decoded = base64.b64decode(split_texts[0]).decode()
    to_name_decoded = base64.b64decode(split_texts[1]).decode()
    subject_text_decoded = base64.b64decode(split_texts[2]).decode()
    body_text_decoded = base64.b64decode(split_texts[3]).decode()

    print(f"from_name_decoded: {from_name_decoded}, to_name_decoded: {to_name_decoded}, subject_text_decoded: {subject_text_decoded}, body_text_decoded: {body_text_decoded}")

    client.close()


def handle_connection_pop(client):
    thread_id = threading.get_ident()
    print(f"[POP] Handling connection in thread {thread_id}")

    response = f"POP Hello from thread {thread_id}\n".encode("utf-8")
    client.sendall(response)

    data = client.recv(BUFSIZE)
    print(f"[POP] Received: {data.decode('utf-8')}")

    client.close()


def accept_connections(server, handler):
    while True:
        client, address = server.accept()
        print(f"{datetime.datetime.now()} 接続要求あり: {address}")
        thread = threading.Thread(target=handler, args=(client,))
        thread.start()


# SMTPサーバーとPOPサーバーの接続受付をそれぞれ別スレッドで実行
smtp_thread = threading.Thread(target=accept_connections, args=(smtp_server, handle_connection_smtp))
smtp_thread.start()

pop_thread = threading.Thread(target=accept_connections, args=(pop_server, handle_connection_pop))
pop_thread.start()

smtp_thread.join()
pop_thread.join()
