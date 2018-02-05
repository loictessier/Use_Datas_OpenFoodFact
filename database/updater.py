#! /usr/bin/env python3
# coding: utf-8

"""DOCSTRING
"""

from os import path
import logging as log
import json
import requests
import records

log.basicConfig(level=log.DEBUG)
# log.basicConfig(level=log.CRITICAL)


class Updater:
    """ DOCSTRING
    """

    def __init__(self):
        self.category_req = ""
        self.product_base_req = ""
        self.product_base_params = dict()
        self.product_vars = list()
        self.dbinfos = dict()
        self.categories = list()
        self.products = list()
        self.initialize_database()

    def update(self):
        '''DOCSTRING
        '''
        self.read_config_json('config.json')
        self.get_categories_datas()
        self.get_products_datas()

    def initialize_database(self):
        '''DOCSTRING
        '''
        db = records.Database('mysql+pymysql://udoff_user:udoff_pwd@localhost')
        rows = db.query("SELECT count(SCHEMA_NAME) AS db_exist \
                         FROM INFORMATION_SCHEMA.SCHEMATA \
                         WHERE SCHEMA_NAME = 'udoff'")
        if not rows.first().db_exist:
            # Open and read the file
            directory = path.dirname(path.dirname(__file__))
            fd = open(path.join(directory, "config", 'INI_DB.sql'), 'r')
            sql_file = fd.read()
            fd.close()

            # all SQL commands (splits on ';')
            sql_commands = sql_file.rstrip(';').split(';')

            # Execute every command
            for command in sql_commands:
                db.query(command)
        else:
            log.debug('Database already exists.')

    def read_config_json(self, filename):
        """ Read the config file and extract the requests
            and parameters associated
        """
        # Open the config file and read data
        directory = path.dirname(path.dirname(__file__))
        path_to_file = path.join(directory, "config", filename)

        try:
            with open(path_to_file) as json_data:
                data = json.load(json_data)
        except FileNotFoundError as err:
            log.critical('Error: %s', err)

        # initiate data structures for the different requests
        self.category_req = data['category_list_request']
        self.product_base_req = data['products_request']['base_request']
        self.product_base_params = data['products_request']['parameters']
        self.product_vars = data['products_request']['products_by_categories']
        self.dbinfos = data['local_database'] 

    def get_categories_datas(self):
        """ Interact with the API by using the requests
            from the config file to get categories datas
        """
        # Get categories datas
        r = requests.get(self.category_req)
        data = r.json()
        for my_dict in data['tags']:
            # only retrieve category with name not starting by $$:
            if ":" not in my_dict['name']:
                category = {
                    "name": my_dict['name'],
                    "id": my_dict['id']
                }
                self.categories.append(category)

    def get_products_datas(self):
        """ Interact with the API by using the requests
            from the config file to get products datas
        """
        # Get product datas
        payload = self.product_base_params
        for my_dict in self.product_vars:
            payload['tag_0'] = my_dict['name']
            for product in my_dict['products']:
                payload['search_terms'] = product['search_terms']
                payload['tag_1'] = product['nutrition_grade']
                response = requests.get(self.product_base_req, params=payload)
                data = response.json()
                if data['products']:
                    self.products.append(
                        self.extract_product(data['products'][0]))
                else:
                    print("ERROR : " + payload['search_terms'])

    def extract_product(self, product_raw_data):
        ''' Extracts informations that we need from
            the raw data of the product and returns it
            as a dictionary.
        '''
        product = {
            "product_name":
                product_raw_data['product_name_fr'] +
                product_raw_data['brands'],
            "ingredients": product_raw_data['ingredients_text_fr'],
            "stores": product_raw_data['stores'],
            "product_url": product_raw_data['url'],
            "nutriscore": product_raw_data['nutrition_grades'],
            "categories": product_raw_data['categories']
        }
        return product


if __name__ == "__main__":
    MY_UPDATER = Updater()
    # print(len(MY_UPDATER.categories))
    # for d in MY_UPDATER.categories:
    #     for key, value in d.items():
    #         print(key + " : " + value)
    # for d in MY_UPDATER.products:
    #     for key, value in d.items():
    #         print(key + " : " + value)
    # print('==================================================================')
    # print('base req : ' + MY_UPDATER.category_req)
    # print('==================================================================')
    # print('product base req : ' + MY_UPDATER.product_base_req)
    # print('==================================================================')
    # print('product parameters : ')
    # for key, value in MY_UPDATER.product_base_params.items():
    #     print(key + " : " + value)
    # print('==================================================================')
    # print('product vars : ')
    # for d in MY_UPDATER.product_vars:
    #     print("nom catégorie : " + d['name'])
    #     for di in d['products']:
    #         for key, value in di.items():
    #             print(key + " : " + value)
    # print('==================================================================')