"""
グループ： zackey, aokiti
テキスト／バイナリ : テキスト
送信リクエストの例
from_name; to_name; subject_text; body_text;
上記は変数名。それぞれの変数には、文字列 -> base64でエンコードしたものを入れる。（ ; が使われないように変形するため。）
それぞれの要素は、; によって区切る。
また、要素は順番で定義する。
送信レスポンスの例
1 / 0
1 : success
0 : fail
受信リクエストの例
to_name;
受信レスポンスの例
from_name; to_name; subject_name; body_name; Timestamp;
DB上には、エンコードされた情報なので、デコードする。
DBに保存する内容
ID, Timestamp, from, to, subject, body
IDとTimestampは自動付与
受信レスポンスが完了したら、そのレコードはDB上から削除する
DB上にあるレコードはすべて、toに記録されているユーザーに受け渡されていないものとする。
"""

import socket  # モジュールをインポート

HOST = "133.27.42.127"  # 宛先を指定
PORT = 3939  # ポートを指定
BUFSIZE = 4096  # バッファサイズを指定
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET: IPv4, SOCK_STREAM: TCP を指定してソケットを生成

client.connect((HOST, PORT))  # HOST,PORTを指定して接続を実施

data = client.recv(BUFSIZE)  # サーバからの送信されたbyte列を受信
print(data.decode("UTF-8"))  # 受信したbyte列データをstringにデコード(文字コードはutf-8を指定

client.close()  # クライアントソケットを修了

