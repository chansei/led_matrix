import serial
import time

# シリアルポートの設定
PORT = "COM3"  # PCに接続されているポート名に置き換えてください（例: COM3, /dev/ttyUSB0など）
BAUDRATE = 115200  # Raspberry Pi Picoと一致するボーレート

# シリアル接続を開く
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # 接続が安定するまで待機
    print(f"Connected to {PORT} at {BAUDRATE} baud.")
except serial.SerialException as e:
    print(f"Could not open serial port {PORT}: {e}")
    exit(1)


def send_command(command):
    """シリアルポートにコマンドを送信"""
    try:
        ser.write((command + "\n").encode('utf-8'))  # コマンドに改行を追加して送信
        print(f"Sent command: {command}")
    except serial.SerialException as e:
        print(f"Error sending command: {e}")


# メインループ
try:
    while True:
        command = input("Enter command (A:表示送り, B:イベント表示, Q:終了): ").upper().strip()

        if command == "Q":
            print("Exiting...")
            break
        elif command in ("A", "B"):
            send_command(command)
        else:
            print("Invalid command. Please enter 'A', 'B', or 'Q'.")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    # シリアルポートを閉じる
    ser.close()
    print("Serial port closed.")
