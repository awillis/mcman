#!/usr/bin/python3

import blessings
from provider import Mojang, Purpur, Paper

# create a new instance
# use provider api to select available versions
# fetch version if it does not exist (or is corrupt?) and link instance to it

# Providers:
# purpur https://api.purpurmc.org/
# paper https://api.papermc.io/
# vanilla https://piston-meta.mojang.com/mc/game/version_manifest_v2.json (use json query to get server.jar, sha and size)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.
    provider = Mojang()
    provider.fetch()


if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
