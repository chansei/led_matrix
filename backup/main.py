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

from class_train import train

X_OFFSET = 16
Y_OFFSET = 42

spi = SPI(1, baudrate=400000000, polarity=1, sck=Pin(14), mosi=Pin(11))

tft = st7789.ST7789(spi, 240, 320, reset=Pin(22, Pin.OUT), dc=Pin(23, Pin.OUT), cs=Pin(13, Pin.OUT))

tft.init()
tft.rotation(1)
tft.png("img2.png", 0, 0)

tft.fill_rect(0, 34, 8, 70, st7789.color565(75, 75, 75))
tft.fill_rect(312, 34, 8, 70, st7789.color565(75, 75, 75))
tft.fill_rect(0, Y_OFFSET+56, 320, 16, st7789.color565(75, 75, 75))

tft.text(base_font, "00000000000", X_OFFSET, Y_OFFSET, st7789.BLACK, st7789.WHITE)
tft.text(base_font, "00000000000", X_OFFSET, Y_OFFSET+16, st7789.BLACK, st7789.WHITE)
tft.text(base_font, "00000000000", X_OFFSET, Y_OFFSET+32, st7789.BLACK, st7789.WHITE)
time.sleep(1)

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

all_trains = [
    train("各駅停車", "2301", "東京", 12),
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
show_jpn_limit = 8
show_eng_limit = 3


async def display_trains():
    global current_index, normal_display_timer, show_jpn_limit, show_eng_limit
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


async def show_event():
    global interrupt_flag
    while True:
        await asyncio.sleep(10)
        if random.randint(1, 10) > 8:
            interrupt_flag = True
            write_row_approach(2)
            await asyncio.sleep(10)
            interrupt_flag = False
        elif random.randint(1, 10) > 8:
            interrupt_flag = True
            write_row_pass(2)
            await asyncio.sleep(10)
            interrupt_flag = False

# シリアル経由で非同期に割り込みコマンドを受信する関数


async def main():
    # 表示切り替えとインデックス更新、シリアル入力を並行実行
    display_task = asyncio.create_task(display_trains())
    update_task = asyncio.create_task(update_index())
    # event_task = asyncio.create_task(show_event())

    await asyncio.gather(display_task, update_task)

# 非同期処理を実行
asyncio.run(main())
