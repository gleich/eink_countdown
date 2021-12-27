import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, MutableMapping

import adafruit_ssd1305
import busio
import digitalio
import toml
from board import D4, SCL, SDA
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
import humanize


def main() -> None:
    (display, font, image, draw) = setup()
    conf = load_config()
    diff = calculated_time(conf)
    display_diff(display, font, image, draw, conf, diff)


def setup():
    i2c = busio.I2C(SCL, SDA)
    display = adafruit_ssd1305.SSD1305_I2C(
        128, 32, i2c, addr=0x3C, reset=digitalio.DigitalInOut(D4)
    )
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)
    logger.success("Setup display and loaded font")
    return (display, font, image, draw)


def load_config() -> MutableMapping[str, Any]:
    config_location = os.path.join(
        Path.home(), ".config", "oled_countdown", "config.toml"
    )
    with open(config_location) as config_file:
        config = toml.load(config_file)
        logger.success("Loaded config")
        return config


def calculated_time(config: MutableMapping[str, Any]) -> timedelta:
    now = datetime.now()
    return datetime.combine(config["date"], datetime.min.time()) - now


def display_diff(display, font, image, draw, conf, diff):
    draw.text(
        (0, 0),
        conf["event"] + " on " + humanize.naturaldate(conf["date"]),
        font=font,
        fill=255,
    )
    draw.rectangle((0, 13, display.width, 13), outline=255, fill=255)
    draw.text((0, 13), str(diff), font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(2)


if __name__ == "__main__":
    main()
