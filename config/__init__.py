import tomli, os
from pathlib import Path
from colored_text import colored

path_to_config = "cgjailConfig.toml"

config_file = Path(__file__).parent / path_to_config

if not config_file.exists():
    colored.print_red("Config file does not exist")
    exit()

try: 
    parsed_config = tomli.loads(config_file.read_text(encoding="utf-8"))

except tomli.TOMLDecodeError as ex:
    colored.print_red(f"Config file is not a valid toml file: {ex}")
    exit()

try: 
    path_to_storage = parsed_config["model_storage"]

except Exception as ex:
    colored.print_red("Config file must define model storage as follows:\nmodel_storage = \"path/to/directory\"")
    exit()

if not Path(path_to_storage).exists():
    colored.print_red(f"Specified storage {path_to_storage} does not exist")
    exit()

if not os.access(path_to_storage, os.W_OK):
    colored.print_red(f"Can not write to {path_to_storage}")
    exit()