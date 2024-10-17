import socket  # モジュールをインポート

HOST = "ccx01.sfc.keio.ac.jp"  # 宛先を指定
PORT = 2414  # ポートを指定
BUFSIZE = 4096  # バッファサイズを指定
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET: IPv4, SOCK_STREAM: TCP を指定してソケットを生成

client.connect((HOST, PORT))  # HOST,PORTを指定して接続を実施
data = client.recv(BUFSIZE)  # サーバからの送信されたbyte列を受信
print(data.decode("UTF-8"))  # 受信したbyte列データをstringにデコード(文字コードはutf-8を指定

client.close()  # クライアントソケットを修了
