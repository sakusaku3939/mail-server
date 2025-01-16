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

import socket

HOST = "bastion.jn.sfc.keio.ac.jp"
PORT = 2414
BUFSIZE = 4096
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

# サーバーにメッセージを送信
to_name = "test to aokiti"
send_request_text = f"{to_name};"
result = client.send(send_request_text.encode("utf-8"))

# サーバーからのメッセージを受信
data = client.recv(BUFSIZE)
print(data.decode("UTF-8"))
if data.decode("UTF-8") != "0":
    print("Success to receive message: ", data.decode("UTF-8"))
    print("Message: ", data.decode("UTF-8"))

client.close()

