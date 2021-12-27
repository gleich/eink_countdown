import os
from pathlib import Path
from typing import Any, MutableMapping
from datetime import datetime, timedelta

import toml
from loguru import logger


def main() -> None:
    """Main function for the program"""
    conf = config()
    diff = calculated_time(conf)
    print(diff)


def config() -> MutableMapping[str, Any]:
    """Load the config file for oled_countdown

    Returns:
        MutableMapping[str, Any]: The loaded TOML file
    """
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


if __name__ == "__main__":
    main()
