import socket
import time

# 非同期ノンブロッキング処理


def nonblocking_way():
    sock = socket.socket()
    sock.setblocking(False)

    try:
        sock.connect(('www.ricoh.co.jp', 80))
    except BlockingIOError:
        pass

    request = 'GET / HTTP/1.0\r\nHost: https://www.ricoh.co.jp/\r\n\r\n'
    data = request.encode('ascii')
    # Socketの接続がいつ確立されるか予測できないので送信を繰り返す
    while 1:
        try:
            sock.send(data)
            break
        except OSError:
            pass

    response = b''
    # レスポンスがいつ読み取れるか予測ができないため受信を繰り返す
    while 1:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                # blocking
                chunk = sock.recv(4096)
            break
        except OSError:
            pass

    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(nonblocking_way())
    return len(res)


if __name__ == '__main__':
    elapsed_times = 0
    rec_len = 0

    for _ in range(10):
        start = time.time()
        rec_len = sync_way()
        elapsed_time = time.time() - start
        elapsed_times += elapsed_time
        print(
            f"elapsed_time: {(elapsed_time):.2f}[sec] recieve size: {(rec_len):d}[byte]")

    print(f"mean_elapsed_time: {(elapsed_times/10):.2f}[sec]")
