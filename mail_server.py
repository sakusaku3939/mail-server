import base64
import socket
import datetime
import threading
import sqlite3

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


# datetime → テキストへのアダプタ
def adapt_datetime(dt):
    return dt.isoformat()


# テキスト → datetimeへのコンバータ
def convert_datetime(s):
    return datetime.datetime.fromisoformat(s.decode('utf-8'))


# カスタムアダプタとコンバータを登録
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)

con = sqlite3.connect("mail.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS mail (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, from_name TEXT, to_name TEXT, subject_text TEXT, body_text TEXT)"
)

cur.execute("INSERT INTO mail (timestamp, from_name, to_name, subject_text, body_text) VALUES (?, ?, ?, ?, ?)",
            (datetime.datetime.now(), "from_name_test", "to_name_test", "subject_text_test", "body_text_test"))
con.commit()

res = cur.execute("SELECT * FROM mail")
res.fetchone()
# JSON形式でデータを表示
for row in res:
    print(row)


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

    print(
        f"from_name_decoded: {from_name_decoded}, to_name_decoded: {to_name_decoded}, subject_text_decoded: {subject_text_decoded}, body_text_decoded: {body_text_decoded}")

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
