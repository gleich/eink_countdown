import os
from pathlib import Path
from typing import Any, MutableMapping
from loguru import logger
import toml


def main() -> None:
    """Main function for the program"""
    print(config())


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


if __name__ == "__main__":
    main()
