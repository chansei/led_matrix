from machine import Pin, SPI, UART
import st7789
import tft_config
import led_base_16x16 as base_font
import led_time_11x16 as time_font
import led_colon_11x4 as colon_font
import vga2_16x16 as vga_font
import uasyncio as asyncio

import time
import _thread
import random
import network
import socket
import uasyncio as asyncio

from class_train import train

X_OFFSET = 16
Y_OFFSET = 42

spi = SPI(1, baudrate=400000000, polarity=1, sck=Pin(14), mosi=Pin(11))

tft = st7789.ST7789(spi, 240, 320, reset=Pin(22, Pin.OUT), dc=Pin(21, Pin.OUT), cs=Pin(13, Pin.OUT))

tft.init()
tft.rotation(1)
tft.png("img2.png", 0, 0)

tft.fill_rect(0, 34, 8, 70, st7789.color565(75, 75, 75))
tft.fill_rect(312, 34, 8, 70, st7789.color565(75, 75, 75))
tft.fill_rect(0, Y_OFFSET+56, 320, 16, st7789.color565(75, 75, 75))

tft.text(base_font, "mjmmmjmmmlm", X_OFFSET, Y_OFFSET, st7789.WHITE, st7789.BLACK)
tft.text(base_font, "00000000000", X_OFFSET, Y_OFFSET+16, st7789.BLACK, st7789.WHITE)
tft.text(base_font, "00000000000", X_OFFSET, Y_OFFSET+32, st7789.BLACK, st7789.WHITE)
time.sleep(10)

# シリアル設定
# uart = UART(0, baudrate=115200)


def write_row(train, row):
    if train is None:
        tft.text(base_font, "000000000000", X_OFFSET, Y_OFFSET+(row-1)*16, st7789.WHITE, st7789.BLACK)
    else:
        tft.text(base_font, train.convert_class_to_led()[0], X_OFFSET, Y_OFFSET+(row-1)*16, train.convert_class_to_led()[1][0], train.convert_class_to_led()[1][1])
        if train.train_time == "::::":
            tft.text(time_font, ";;", X_OFFSET+48, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(colon_font, ";", X_OFFSET+70, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(time_font, ";;", X_OFFSET+78, Y_OFFSET+(row-1)*16, st7789.WHITE)
        else:
            tft.text(time_font, train.train_time[:2], X_OFFSET+48, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(colon_font, ":", X_OFFSET+70, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(time_font, train.train_time[2:], X_OFFSET+78, Y_OFFSET+(row-1)*16, st7789.WHITE)
        tft.text(base_font, train.convert_destination_to_led()[0], X_OFFSET+100, Y_OFFSET+(row-1)*16,train.convert_destination_to_led()[1][0], train.convert_destination_to_led()[1][1])
        tft.text(base_font, train.convert_length_to_led()[0], X_OFFSET+148, Y_OFFSET+(row-1)*16, train.convert_length_to_led()[1][0], train.convert_length_to_led()[1][1])


def write_row_eng(train, row):
    if train is None:
        tft.text(base_font, "000000000000", X_OFFSET, Y_OFFSET+(row-1)*16, st7789.WHITE, st7789.BLACK)
    else:
        tft.text(base_font, train.convert_class_to_led_eng()[0], X_OFFSET, Y_OFFSET+(row-1)*16, train.convert_class_to_led_eng()[1][0], train.convert_class_to_led_eng()[1][1])
        if train.train_time == "::::":
            tft.text(time_font, ";;", X_OFFSET+48, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(colon_font, ";", X_OFFSET+70, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(time_font, ";;", X_OFFSET+78, Y_OFFSET+(row-1)*16, st7789.WHITE)
        else:
            tft.text(time_font, train.train_time[:2], X_OFFSET+48, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(colon_font, ":", X_OFFSET+70, Y_OFFSET+(row-1)*16, st7789.WHITE)
            tft.text(time_font, train.train_time[2:], X_OFFSET+78, Y_OFFSET+(row-1)*16, st7789.WHITE)
        tft.text(base_font, train.convert_destination_to_led_eng()[0], X_OFFSET+100, Y_OFFSET+(row-1)*16, train.convert_destination_to_led_eng()[1][0], train.convert_destination_to_led()[1][1])
        tft.text(base_font, train.convert_length_to_led_eng()[0], X_OFFSET+148, Y_OFFSET+(row-1)*16, train.convert_length_to_led_eng()[1][0], train.convert_length_to_led_eng()[1][1])


def write_row_approach(row):
    tft.text(base_font, "JKLMNOPQ00000 ", X_OFFSET, Y_OFFSET+(row-1)*16, st7789.RED, st7789.BLACK)

def write_row_pass(row):
    tft.text(base_font, "0000000000000", X_OFFSET, Y_OFFSET, st7789.WHITE, st7789.BLACK)
    tft.text(base_font, "JKLSTUPQ00000 ", X_OFFSET, Y_OFFSET+(row-1)*16, st7789.RED, st7789.BLACK)


# グローバル変数
current_index = 0  # all_trainsの表示開始インデックス
tft.text(vga_font, str(current_index), 0, 200)
language_flag = True  # True: 日本語, False: 英語
interrupt_flag = False  # True: イベント表示中
fixed_display_duration = 10  # イベント表示時間（秒）
SSID = "dlcl_4h"
PASSWORD = "dlcl18sysdev"
event_arrived = asyncio.Event()
event_passed = asyncio.Event()

async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        await asyncio.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())

all_trains = [
    train("中央特快", "2301", "東京", 12),
    train("普通", "::::", "JR", 0),
    train("普通", "2312", "三鷹", 10),
    train("快速", "2322", "新宿", 10),
    train("普通", "2326", "三鷹", 10),
    train("快速", "2333", "東京", 10),
    train("快速", "2351", "東京", 12),
    train("普通", ";003", "三鷹", 10),
    train("普通", ";025", "三鷹", 10)
]

# 表示内容を切り替える関数

normal_display_timer = 0
event_timer = 0
show_jpn_limit = 8
show_eng_limit = 3


async def display_trains():
    global current_index, normal_display_timer, event_timer, show_jpn_limit, show_eng_limit
    while True:
        train1 = None
        train2 = None
        train3 = None
        if current_index < len(all_trains):
            train1 = all_trains[current_index]
        if current_index + 1 < len(all_trains):
            train2 = all_trains[current_index + 1]
        if current_index + 2 < len(all_trains):
            train3 = all_trains[current_index + 2]
        
        if normal_display_timer == 0:
            write_row(train1, 1)
            write_row(train2, 2)
            write_row(train3, 3)
        elif normal_display_timer == show_jpn_limit:
            write_row_eng(train1, 1)
            write_row_eng(train2, 2)
            write_row_eng(train3, 3)
        elif normal_display_timer == show_jpn_limit + show_eng_limit:
            write_row_eng(train1, 1)
            write_row_eng(train2, 2)
            write_row_eng(train3, 3)
            normal_display_timer = -1
            
        if event_arrived.is_set():
            if event_timer > 10:
                event_arrived.clear()
                event_timer = 0
            elif event_timer % 2 == 1:
                write_row(None, 3)
            else:
                write_row_approach(3)
            event_timer += 1
        
        if event_passed.is_set():
            write_row(None, 1)
            write_row(None, 2)
            if event_timer > 10:
                event_passed.clear()
                event_timer = 0
            elif event_timer % 2 == 1:
                write_row(None, 3)
            else:
                write_row_pass(3)
            event_timer += 1

        await asyncio.sleep(1)
        normal_display_timer += 1


# 表示インデックスを更新する関数


async def update_index():
    global current_index
    while True:
        await asyncio.sleep(30)  # 30秒ごとにインデックスを更新
        if not interrupt_flag:
            current_index = current_index + 1  # 次の2本の列車情報に切り替え
            tft.text(vga_font, str(current_index), 0, 200)


async def handle_wifi_messages():
    global event_received
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)
    server.setblocking(False)  # 非ブロッキングモードに設定
    print("Listening for messages on", addr)

    while True:
        try:
            # ソケットの接続を非同期で受け入れる
            cl, addr = server.accept()
            print('Client connected from', addr)
            cl.setblocking(False)  # クライアントも非ブロッキングモードに設定
            
            while True:
                try:
                    message = cl.recv(1024)  # メッセージを受信
                    if not message:
                        break
                    
                    message = message.decode().strip()
                    print("Received message:", message)
                    
                    # メッセージに基づいてイベントを設定
                    if message == "approach":
                        event_arrived.set()  # イベント発火
                    elif message == "pass":
                        event_passed.set()  # イベント発火

                except OSError as e:
                    if e.errno == 11:  # EAGAINエラーを処理
                        await asyncio.sleep(0.1)  # 少し待機して再試行
                    else:
                        raise  # その他のエラーは再発生させる

            cl.close()
            print("Connection closed")

        except OSError as e:
            if e.errno == 11:  # EAGAINエラーを処理
                await asyncio.sleep(0.1)  # 少し待機して再試行
            else:
                raise  # その他のエラーは再発生させる


async def main():
    await connect_wifi()
    # 表示切り替えとインデックス更新、シリアル入力を並行実行
    display_task = asyncio.create_task(display_trains())
    update_task = asyncio.create_task(update_index())
    wifi_task = asyncio.create_task(handle_wifi_messages())

    await asyncio.gather(display_task, update_task, wifi_task)

# 非同期処理を実行
asyncio.run(main())
