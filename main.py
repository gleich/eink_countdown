import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, MutableMapping

from adafruit_epd.ssd1680 import Adafruit_SSD1680
from adafruit_epd.epd import Adafruit_EPD
import busio
import digitalio
import toml
import board
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
import humanize

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main() -> None:
    (display, image, draw) = setup()
    regular_font = ImageFont.truetype("./fonts/SpaceMono-Regular.ttf", 20)
    italic_font = ImageFont.truetype("./fonts/SpaceMono-Italic.ttf", 20)
    while True:
        conf = load_config()
        diff = calculated_time(conf)
        display_diff(display, regular_font, italic_font, image, draw, conf, diff)
        time.sleep(600)  # 10 minutes


def setup():
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    ecs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D22)
    rst = digitalio.DigitalInOut(board.D27)
    busy = digitalio.DigitalInOut(board.D17)
    display = Adafruit_SSD1680(  # Newer eInk Bonnet
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


def load_config() -> MutableMapping[str, Any]:
    config_location = os.path.join(
        Path.home(), ".config", "eink_countdown", "config.toml"
    )
    with open(config_location) as config_file:
        config = toml.load(config_file)
        return config


def calculated_time(config: MutableMapping[str, Any]) -> timedelta:
    now = datetime.now()
    return datetime.combine(config["date"], datetime.min.time()) - now


def display_diff(display, regular_font, italic_font, image, draw, conf, diff) -> None:
    draw.rectangle((0, 0, display.width, display.height), fill=WHITE)
    draw.text(
        (0, 0),
        conf["event"],
        font=italic_font,
        fill=BLACK,
    )
    draw.rectangle((0, 26, display.width, 31), outline=BLACK, fill=BLACK)
    draw.text(
        (0, 28),
        humanize.naturaldelta(diff) + " till " + humanize.naturaldate(conf["date"]),
        font=regular_font,
        fill=BLACK,
    )
    display.image(image)
    display.display()
    logger.success("Updated display")


if __name__ == "__main__":
    main()
