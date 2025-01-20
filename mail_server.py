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

# データベースの初期化
con = sqlite3.connect("mail.db", detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS mail (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, from_name TEXT, to_name TEXT, subject_text TEXT, body_text TEXT)"
)

# SQLite用のロック
lock = threading.Lock()

running = True


def handle_connection_smtp(client):
    try:
        thread_id = threading.get_ident()
        print(f"[SMTP] Handling connection in thread {thread_id}")

        data = client.recv(BUFSIZE)
        print(f"[SMTP] Received: {data.decode('utf-8')}")

        split_texts = data.decode('utf-8').split(";")
        print(split_texts)

        from_name, to_name, subject_text, body_text = split_texts

        from_name_decoded = base64.b64decode(from_name).decode()
        to_name_decoded = base64.b64decode(to_name).decode()
        subject_text_decoded = base64.b64decode(subject_text).decode()
        body_text_decoded = base64.b64decode(body_text).decode()

        print(
            f"from_name_decoded: {from_name_decoded}, to_name_decoded: {to_name_decoded}, subject_text_decoded: {subject_text_decoded}, body_text_decoded: {body_text_decoded}"
        )

        # メールをDBに保存
        with lock:
            cur.execute(
                "INSERT INTO mail (timestamp, from_name, to_name, subject_text, body_text) VALUES (?, ?, ?, ?, ?)",
                (datetime.datetime.now(), from_name, to_name, subject_text, body_text))
            con.commit()

        response = "1".encode("utf-8")
        client.sendall(response)

    except Exception as e:
        print(f"Error: {e}")
        response = "0".encode("utf-8")
        client.sendall(response)

    finally:
        client.close()


def handle_connection_pop(client):
    try:
        thread_id = threading.get_ident()
        print(f"[POP] Handling connection in thread {thread_id}")

        data = client.recv(BUFSIZE)
        print(f"[POP] Received: {data.decode('utf-8')}")

        to_name = data.decode('utf-8')
        to_name_decoded = base64.b64decode(to_name).decode()
        print(f"to_name_decoded: {to_name_decoded}")

        # メールをDBから取得
        cur.execute("SELECT * FROM mail WHERE to_name = ?", (to_name,))
        rows = cur.fetchall()
        print(f"DB rows: {rows}")

        if len(rows) == 0:
            response = "".encode("utf-8")
            client.sendall(response)
            return

        # メールをクライアントに送信
        for row in rows:
            from_name = row[2]
            to_name = row[3]
            subject_text = row[4]
            body_text = row[5]
            timestamp = row[1]

            response = (
                f"{from_name};{to_name};{subject_text};{body_text};{timestamp}"
                .encode("utf-8")
            )
            client.sendall(response)

            # 受信したメールをDBから削除
            # with lock:
            #     cur.execute("DELETE FROM mail WHERE id = ?", (row[0],))
            #     con.commit()

    except Exception as e:
        print(f"Error: {e}")
        response = "0".encode("utf-8")
        client.sendall(response)
    finally:
        client.close()


def accept_connections(server, handler, type):
    global running

    try:
        while running:
            server.settimeout(1.0)
            try:
                client, address = server.accept()
                print(f"{datetime.datetime.now()} 接続要求あり: {address}")
                thread = threading.Thread(target=handler, args=(client,))
                thread.start()
            except socket.timeout:
                continue
    finally:
        server.close()
        print(f"Stopped {type} server")


# SMTPサーバーとPOPサーバーの接続受付をそれぞれ別スレッドで実行
smtp_thread = threading.Thread(target=accept_connections, args=(smtp_server, handle_connection_smtp, "SMTP"))
smtp_thread.start()

pop_thread = threading.Thread(target=accept_connections, args=(pop_server, handle_connection_pop, "POP"))
pop_thread.start()

try:
    smtp_thread.join()
    pop_thread.join()
except KeyboardInterrupt:
    running = False
    print("\nStopping servers...")
