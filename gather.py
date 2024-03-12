import tomli
from pathlib import Path
from colored_text.colored_text import colored

path_to_config = "cgjailConfig.toml"

config_file = Path(path_to_config)

if not config_file.exists():
    config_file = Path(f"../{path_to_config}")
    if not config_file.exists():
        colored.print_red("Config file does not exist")
        exit()

try:
    parsed_config = tomli.loads(config_file.read_text(encoding="utf-8"))

except tomli.TOMLDecodeError as ex:
    colored.print_red("Config file is not a valid toml file")
    exit()

path_to_storage = parsed_config["model_storage"]

print(path_to_storage)