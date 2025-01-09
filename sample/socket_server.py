import socket  # モジュールをインポート
import datetime

PORT = 3939  # 事前に決めたポートを設定

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 事前に決めたポートを設定

server.bind(("", PORT))  # 事前に決めたポートを設定
server.listen()  # 接続受付状態を開始

while True:  # プログラム実行中常にループし続けることで、待ち受け状態を維持
    client, addr = server.accept()  # 接続受付
    client.sendall(b"hello! this is aokiti server program!!\n")  # 自由に返却するメッセージを記述してください
    print(str(datetime.datetime.now()), "接続要求あり")  # ログ出力
    print(client)
    client.close()
