import socket  # モジュールをインポート
import datetime
import threading

PORT = 3939  # 事前に決めたポートを設定

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 事前に決めたポートを設定

server.bind(("", PORT))  # 事前に決めたポートを設定
server.listen()  # 接続受付状態を開始

print("Started multi-threaded server")


# クライアントの要求を処理する関数
def handle_connection(client):
    # 自分のスレッド ID を取得する
    # thread_id = ...
    thread_id = threading.get_ident()

    # `thread_id`` を含めてレスポンスを返す
    # response = ...
    # client.sendall(...
    response = f"Hello from thread {thread_id}\n".encode("utf-8")
    client.sendall(response)
    client.close()


while True:
    # 接続を受け付ける
    # client, address = ...
    client, address = server.accept()
    print(str(datetime.datetime.now()), "接続要求あり")  # ログ出力

    # 新しいスレッドで処理を進める
    # thread = ...
    thread = threading.Thread(target=handle_connection, args=[client])
    thread.start()
