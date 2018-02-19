#!/usr/bin/env python3
# coding: utf-8

""" DOCSTRING
"""

import src.Controller as co
import database.updater as updater


class Udoff:
    """ DOCSTRING
    """

    def __init__(self):
        self.my_controller = co.Controller()
        self.my_controller.start()

if __name__ == "__main__":
    my_udoff = Udoff()