#!/usr/bin/python3

from blessings import Terminal
from provider import Mojang, Purpur, Paper
from instance import Instance


def main():
    term = Terminal()

    with term.fullscreen():
        print("List running instances")
        print("Create new instance")
        # select mine craft server provider
        # present available versions
        # select version
        # provide instance name
        # build instance
        print("Start instance by name")
        print("Stop instance by name")
        print("Disable instance by name")


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
