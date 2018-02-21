#!/usr/bin/env python3
# coding: utf-8

""" DOCSTRING
"""

from os import path
import argparse
import datetime
import monthdelta as md
import logging as log
import json
import src.Controller as co
import database.updater as updater

# log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.CRITICAL)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--update",
        help="""Force the update of the database""",
        action='store_true'
    )
    return parser.parse_args()


def is_time_to_update(filename):
    directory = path.dirname(path.dirname(__file__))
    path_to_file = path.join(directory, "config", filename)
    try:
        with open(path_to_file) as json_data:
            data = json.load(json_data)
    except FileNotFoundError as err:
        log.critical('Error: %s' % err)
    last_update = data['last_update']
    if last_update:
        last_update = \
            datetime.datetime.strptime(last_update, '%d/%m/%Y')
        if md.monthmod(
                last_update,
                datetime.datetime.now())[0] <= md.monthdelta(1):
            return False
    return True


def set_last_update_datetime(filename):
    directory = path.dirname(path.dirname(__file__))
    path_to_file = path.join(directory, "config", filename)
    try:
        with open(path_to_file, "r") as jsonFile:
            data = json.load(jsonFile)

        data["last_update"] = datetime.datetime.now().strftime('%d/%m/%Y')

        with open(path_to_file, "w") as jsonFile:
            json.dump(data, jsonFile)
    except FileNotFoundError as err:
        log.critical('Error: %s' % err)


def main():
    # run update on database if argument -u has been specified
    # or if no update were made in the past month
    # or on the first execution
    args = parse_arguments()
    if args.update or is_time_to_update('config.json'):
        print("Mise à jour de la base de donnée...")
        updater.Updater()
        set_last_update_datetime('config.json')
    # run the application
    my_controller = co.Controller()
    my_controller.start()

if __name__ == "__main__":
    main()
