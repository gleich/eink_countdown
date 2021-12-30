import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, MutableMapping

import toml
from apscheduler.schedulers.blocking import BlockingScheduler

import display

(DISPLAY, IMAGE, DRAW) = display.setup()
scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", minute=0)
def main() -> None:
    conf = load_config()
    diff = calculated_time(conf)
    display.show_diff(DISPLAY, IMAGE, DRAW, conf, diff)


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


if __name__ == "__main__":
    time.sleep(20)
    main()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
