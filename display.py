from datetime import datetime

import board
import busio
import digitalio
import humanize
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from loguru import logger
from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
REGULAR_FONT = ImageFont.truetype("./fonts/SpaceMono-Regular.ttf", 20)
ITALIC_FONT = ImageFont.truetype("./fonts/SpaceMono-Italic.ttf", 20)
SMALL_FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)


def setup():
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    ecs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D22)
    rst = digitalio.DigitalInOut(board.D27)
    busy = digitalio.DigitalInOut(board.D17)
    display = Adafruit_SSD1680(
        122,
        250,
        spi,
        cs_pin=ecs,
        dc_pin=dc,
        sramcs_pin=None,
        rst_pin=rst,
        busy_pin=busy,
    )
    display.rotation = 1
    display.power_up()
    display.fill(Adafruit_EPD.WHITE)

    image = Image.new("RGB", (display.width, display.height), color=WHITE)
    draw = ImageDraw.Draw(image)
    logger.success("Setup display")
    return (display, image, draw)


def show_diff(display, image, draw, conf, diff) -> None:
    draw.rectangle((0, 0, display.width, display.height), fill=WHITE)
    draw.text(
        (0, 0),
        conf["event"],
        font=ITALIC_FONT,
        fill=BLACK,
    )
    draw.rectangle((0, 26, display.width, 31), outline=BLACK, fill=BLACK)
    draw.text(
        (0, 28),
        "{} and {} hours\ntill {}".format(
            humanize.naturaldelta(diff), 10, conf["date"]
        ),
        font=REGULAR_FONT,
        fill=BLACK,
    )
    draw.text(
        (0, 105),
        "Last updated at " + datetime.now().strftime("%-I:%-M:%-S %p"),
        font=SMALL_FONT,
        fill=BLACK,
    )
    display.image(image)
    display.display()
    logger.success("Updated display")
