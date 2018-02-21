#!/usr/bin/env python3
# coding: utf-8

""" Starting point of the application
    use_data_open_food_fact (udoff)
"""

from os import path
import argparse
import datetime
import logging as log
import json
import monthdelta as md
import sqlalchemy
import app.controller as co
import database.updater as updater

# log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.CRITICAL)


def parse_arguments():
    """ Add options at the launch of the application
            -u force update of the database
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--update",
        help="""Force the update of the database""",
        action='store_true'
    )
    return parser.parse_args()


def is_time_to_update(filename):
    """ Return True if the last update date
        in the config file is more than a month ago
        or if it's not filled
    """
    directory = path.dirname(path.dirname(__file__))
    path_to_file = path.join(directory, "config", filename)
    try:
        with open(path_to_file) as json_data:
            data = json.load(json_data)
    except FileNotFoundError as err:
        log.critical('Error: %s', err)
    last_update = data['last_update']
    if last_update:
        last_update = \
            datetime.datetime.strptime(last_update, '%d/%m/%Y')
        if datetime.datetime.now() - md.monthdelta(1) <= last_update:
            return False
    return True


def set_last_update_datetime(filename):
    """ Set the last update date in the config file
        to today's date
    """
    directory = path.dirname(path.dirname(__file__))
    path_to_file = path.join(directory, "config", filename)
    try:
        with open(path_to_file, "r") as json_file:
            data = json.load(json_file)

        data["last_update"] = datetime.datetime.now().strftime('%d/%m/%Y')

        with open(path_to_file, "w") as json_file:
            json.dump(data, json_file)
    except FileNotFoundError as err:
        log.critical('Error: %s', err)


def main():
    """ Main fonction executed at the start of the application
        Call the update script to create and update the database
        if necessary. Then start the application main menu.
    """
    try:
        my_updater = updater.Updater()
        # if database doesn't exist, creates it
        print("Connexion à la base de données...")
        is_init = my_updater.initialize_database()
        # run update on database if argument -u has been specified
        # or if no update were made in the past month
        # or on the first execution
        args = parse_arguments()
        if args.update or is_time_to_update('config.json') or is_init:
            print("Mise à jour de la base de données...")
            my_updater.update()
            set_last_update_datetime('config.json')
        # run the application
        my_controller = co.Controller()
        my_controller.start()
    except sqlalchemy.exc.OperationalError as err:
        log.critical(
            "Impossible d'accéder à la base de données. "
            "Informations de connexion incorrectes. "
            "Error: %s", err)

if __name__ == "__main__":
    main()
