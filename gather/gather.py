# how to beautify that? 
import sys
sys.path.insert(0, '../')

import config, parse
from colored_text import colored

colored.print_cyan(config.path_to_storage)

# colored.print_green(parse.args.pid)