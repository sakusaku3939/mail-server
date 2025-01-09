import threading
import time


def run(i: int):
    print(f"Thread [{threading.get_ident()}] started")

    # `i` 秒スリープする
    time.sleep(i)

    print(f"Thread [{threading.get_ident()}] finished")


for i in range(3):
    # `i` 番目のスレッドを作成し、 `run(i)` を実行する
    threading.Thread(target=run, args=[i]).start()
