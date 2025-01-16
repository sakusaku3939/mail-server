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
import base64

HOST = "bastion.jn.sfc.keio.ac.jp"
PORT = 3939
BUFSIZE = 4096
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to the server...")
client.connect((HOST, PORT))

# サーバーにメッセージを送信
from_name = "test from zackey"
to_name = "test to aokiti"
subject_text = "test message"
body_text = "this is test text;; ."

from_name_encoded = base64.b64encode(from_name.encode()).decode()
to_name_encoded = base64.b64encode(to_name.encode()).decode()
subject_text_encoded = base64.b64encode(subject_text.encode()).decode()
body_text_encoded = base64.b64encode(body_text.encode()).decode()

send_request_text = f"{from_name_encoded};{to_name_encoded};{subject_text_encoded};{body_text_encoded}"

# サーバーにメッセージを送信
result = client.send(send_request_text.encode("utf-8"))
print("Message: ", send_request_text)

# サーバーからのメッセージを受信
data = client.recv(BUFSIZE)
if data.decode("UTF-8") == "1":
    print("Success to send message")
else:
    print("Fail to send message")

client.close()
