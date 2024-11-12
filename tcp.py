import socket

# Raspberry Pi Pico WのIPアドレスとポート番号
HOST = '192.168.2.73'  # 例: '192.168.1.10'
PORT = 8080  # Pico Wのサーバーで指定したポート

# サーバーに接続する関数


def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())
        print(f"Sent: {message}")


# メッセージを送信
message = "pass"  # "approach" または "pass" を指定
send_message(message)
