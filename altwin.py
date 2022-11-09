#!/usr/bin/python3

import os
import json
import argparse

parser = argparse.ArgumentParser(prog = "altwin")

parser.add_argument("command", choices=["toggle", "noswap", "swap", "status"], default="status") 
args = parser.parse_args()

CONFIG_PATH = "/org/gnome/desktop/input-sources/xkb-options"
OPTION_VALUE = "altwin:swap_alt_win"

MESSAGE_SWAPPED = "Alt-win swapped [Win=Alt, Alt=Win]"
MESSAGE_SWAP_REMOVED = "Alt-win swap removed [Win=Win, Alt=Alt]"
MESSAGE_ALREADY_SWAPPED = "Alt-win already swapped [Win=Alt, Alt=Win]"

stream = os.popen("dconf read %s" % CONFIG_PATH)

# xkb = json.loads('{"options": %s}' % stream.read().strip().replace("'", '"'))
options = json.loads(stream.read().replace("'", '"'))
message = ""

if args.command == "noswap":
    options.remove(OPTION_VALUE)
    message = MESSAGE_SWAP_REMOVED
elif args.command == "swap":
    if OPTION_VALUE not in options:
        options.append(OPTION_VALUE)
        message = MESSAGE_SWAPPED
    else:
        message = MESSAGE_ALREADY_SWAPPED
elif args.command == "toggle":
    if OPTION_VALUE in options:
        options.remove(OPTION_VALUE)
        message = MESSAGE_SWAP_REMOVED
    else:
        options.append(OPTION_VALUE)
        message = MESSAGE_SWAPPED
else:
    swapped = OPTION_VALUE in options
    if OPTION_VALUE in options:
        message = "Swapped [Win=Alt, Alt=Win]"
    else:
        message = "Not swapped [Win=Win, Alt=Alt]"

value = json.dumps(options).replace('"', '\\"')
command = "dconf write %s \"%s\"" % ( CONFIG_PATH,  value)

os.system(command)

print(message)




