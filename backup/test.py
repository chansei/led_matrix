import utime
import st7789
import tft_config
import vga2_16x16 as font
from machine import Pin, SPI, UART
import uasyncio as asyncio
import st7789

spi = SPI(1, baudrate=40000000, polarity=1, sck=Pin(14), mosi=Pin(11))

tft = st7789.ST7789(spi, 240, 320, reset=Pin(22, Pin.OUT), dc=Pin(23, Pin.OUT), cs=Pin(13, Pin.OUT))

tft.init()
tft.rotation(1)

async def scroll(tft, x, y, text, width):
    """
    テキストを水平スクロールで描画する関数

    Parameters:
        tft (st7789.ST7789): ST7789ディスプレイインスタンス
        x (int): スクロール開始位置のx座標
        y (int): スクロール開始位置のy座標
        text (str): 表示するテキスト
        width (int): テキストのスクロール範囲の幅
    """
    text_width = len(text)*16
    pos_x = x

    while True:
        tft.fill_rect(x, y, width, 16, st7789.BLACK)  # テキストの背景をクリア
        tft.text(font, text, pos_x, y)        # テキストを描画
        pos_x -= 1                                                   # 左に1ドット移動

        if pos_x < x - text_width:                                   # テキストが左端に達したらリセット
            pos_x = x + width

        await asyncio.sleep(0.01)

async def main():
    # 表示切り替えとインデックス更新、シリアル入力を並行実行
    display_task = asyncio.create_task(scroll(tft, 0, 10, "Hello, World!", 240))

    await asyncio.gather(display_task)

# 非同期処理を実行
asyncio.run(main())