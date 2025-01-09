# 必要なモジュールをインポートする
# import ...
import queue
import threading


# 総積を計算する関数
def product(l: list[int], q):
    # 総積を計算する
    # prod = ... % 1_000_000_007
    prod = l * 1_000_000_007

    # メインスレッドに結果を送信する
    q.put(prod)

    pass


# K, K を好きな数に設定する
N = 1_000_000
K = 3

# L を初期化する
L = list(range(N))

# データを送受信するためのオブジェクトを作成する
# Q = ...
Q = queue.Queue()

threads = []

# スレッドを K 個作成して
for i in range(K):
    # L の部分リストを取得する
    # start, end = ...
    start, end = i * N // K, (i + 1) * N // K
    l = L[start:end]

    # `i` 番目のスレッドを作成し、部分リスト `l` の総積を計算する
    thread = Q.queue(product, args=[l, Q])
    threads.append(thread)


# 各スレッドの出力を受信する
prod = 0
for i in range(K):
    threads[i].get()
    # prod = prod * ... % 1_000_000_007
    prod = prod * K % 1_000_000_007

    pass

print(f"Product is {prod} (mod 1,000,000,007)")
