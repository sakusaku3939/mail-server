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
import base64
import socket

HOST = "bastion.jn.sfc.keio.ac.jp"
PORT = 2414
BUFSIZE = 4096


def parse_data(data):
    if data == "0":
        return "Failed to receive message"

    if data == "":
        return "No up-to-date message"

    split_texts = data.split(";")
    from_name, to_name, subject_text, body_text, timestamp = split_texts

    from_name_decoded = base64.b64decode(from_name).decode()
    to_name_decoded = base64.b64decode(to_name).decode()
    subject_text_decoded = base64.b64decode(subject_text).decode()
    body_text_decoded = base64.b64decode(body_text).decode()

    return f"""
    timestamp:
    {timestamp}
    
    from_name:
    {from_name_decoded}
    
    to_name:
    {to_name_decoded}
    
    subject_text:
    {subject_text_decoded}
    
    body_text:
    {body_text_decoded}
    """


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

# サーバーにメッセージを送信
to_name = "test to aokiti"

to_name_encoded = base64.b64encode(to_name.encode()).decode()
result = client.send(to_name_encoded.encode("utf-8"))

# サーバーからのメッセージを受信
recv_data = client.recv(BUFSIZE).decode("UTF-8")
print(parse_data(recv_data))

client.close()
