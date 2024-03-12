import sys
sys.path.insert(0, '../')

import config
from colored_text import colored

colored.print_cyan(config.path_to_storage)
