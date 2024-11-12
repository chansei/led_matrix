from machine import Pin, SPI
import st7789
import tft_config
import led_base_16x16 as base_font
import led_time_11x16 as time_font
import led_colon_11x4 as colon_font

import time

spi = SPI(1, baudrate=40000000, polarity=1, sck=Pin(14), mosi=Pin(11))

tft = st7789.ST7789(spi, 240, 320,
                    reset=Pin(22, Pin.OUT),
                    dc=Pin(21, Pin.OUT),
                    cs=Pin(13, Pin.OUT)
                    )

tft.init()
tft.rotation(1)

tft.png("img2.png", 0, 0)

while True:
    tft.text(base_font, "123", 0, 40, st7789.RED, st7789.WHITE)
    tft.text(time_font, "23", 48, 40, st7789.WHITE)
    tft.text(colon_font, ":", 70, 40, st7789.WHITE)
    tft.text(time_font, "31", 78, 40, st7789.WHITE)
    tft.text(base_font, "@0A<>", 100, 40, st7789.WHITE)

    tft.text(base_font, "JKLMNOPQ", 0, 56, st7789.RED, st7789.BLACK)

    time.sleep(6)
    tft.text(base_font, "456", 0, 40, st7789.RED, st7789.WHITE)
    tft.text(base_font, "BCD=?", 100, 40, st7789.WHITE)

    tft.text(base_font, "456", 0, 56, st7789.RED, st7789.WHITE)
    tft.text(base_font, "GHI=?", 100, 56, st7789.WHITE)

    time.sleep(3)
