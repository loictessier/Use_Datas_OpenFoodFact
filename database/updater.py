#!/usr/bin/env python3
# coding: utf-8

""" Updater.py will be used as a script to initialise
    the database with datas that will be used by
    the application. To be functionnal it has
    prerequisites : a valid user granted with right on
    the local mysql database used for this application.
    These informations must match the config.json file
    (see local_database). You can also adapt the
    sample of categories requested for products in the
    API to your needs by editing the config.json file.
"""

from os import path
import logging as log
import json
import requests
import records
import re

# log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.CRITICAL)


class Updater:
    """ This class will be used at the launch
        of the application to create the database
        and fill it with datas.
    """

    def __init__(self):
        # Parameters for API queries
        self.category_req = ""
        self.product_base_req = ""
        self.product_base_params = dict()
        self.cat_vars = list()
        self.min_prod_per_cat = 0
        # Data from API 
        self.categories = list()
        self.products = list()
        # Database connection informations
        self.db_infos = dict()
        # Methods
        self._read_config_json('config.json')
        self.update()

    def update(self):
        ''' Call internal methods
        '''
        self._initialize_database()
        self._get_categories_datas()
        self._get_products_datas()
        self._insert_datas_to_db()

    def _read_config_json(self, filename):
        """ Read the config file and extract the informations
            we need to connect to the database and interact with
            the API
        """
        # Open the config file and read data
        directory = path.dirname(path.dirname(__file__))
        path_to_file = path.join(directory, "config", filename)

        try:
            with open(path_to_file) as json_data:
                data = json.load(json_data)
        except FileNotFoundError as err:
            log.critical('Error: %s' % err)

        # initiate data structures for the different requests
        self.category_req = data['category_list_request']
        self.product_base_req = data['products_request']['base_request']
        self.product_base_params = data['products_request']['parameters']
        self.cat_vars = data['products_request']['categories']
        self.db_infos = data['local_database']
        self.min_prod_per_cat = data['min_prod_per_cat']

    def _initialize_database(self):
        ''' Check if database structure already
            exist on localhost, if not it creates it.
        '''
        db = records.Database(
            'mysql+pymysql://{username}:{password}@localhost'.format(
                username=self.db_infos['user']['name'], 
                password=self.db_infos['user']['password']))

        rows = db.query("SELECT count(SCHEMA_NAME) AS db_exist \
                         FROM INFORMATION_SCHEMA.SCHEMATA \
                         WHERE SCHEMA_NAME = 'udoff'")
        if not rows.first().db_exist:
            # Open and read the file
            directory = path.dirname(path.dirname(__file__))
            fd = open(path.join(directory, "database", 'INI_DB.sql'), 'r')
            sql_file = fd.read()
            fd.close()

            # all SQL commands (splits on ';')
            sql_commands = sql_file.rstrip(';').split(';')

            # Execute every command
            for command in sql_commands:
                db.query(command)
        else:
            log.debug('Database already exists')

    def _get_categories_datas(self):
        """ Interact with the API by using the requests
            from the config file to get categories datas
        """
        # Get categories datas
        r = requests.get(self.category_req)
        r.encoding = 'UTF-8'
        data = r.json()
        for my_dict in data['tags']:
            # only retrieve category with name not having ':' in it
            if ":" not in my_dict['name'] \
                    and len(my_dict['name']) < 150:
                category = {
                    "name": my_dict['name'],
                    "id": my_dict['id']
                }
                category["id"] = re.sub(r'.*:', '', category["id"])
                self.categories.append(category)

    def _get_products_datas(self):
        """ Interact with the API by using the requests
            from the config file to get products datas
        """
        # Get product datas
        payload = self.product_base_params
        for cat in self.cat_vars:
            payload['tag_0'] = cat['name']
            # Récupérer des éléments à rechercher
            count = self._process_product_requests(payload, 'e')
            if count < (self.min_prod_per_cat // 2):
                count = self._process_product_requests(payload, 'd')
            # récupérer des substituts
            count = self._process_product_requests(payload, 'a')
            if count < (self.min_prod_per_cat // 2):
                count = self._process_product_requests(payload, 'b')

    def _process_product_requests(self, r_payload, nutrition_grade):
        ''' Analyze and sort product data obtained
            with the input parameters
        '''
        cpt_new_products = 0
        r_payload['tag_1'] = nutrition_grade
        response = requests.get(self.product_base_req, params=r_payload)
        response.encoding = 'UTF-8'
        data = response.json()
        if data['products']:
            for it in data['products']:
                try:
                    item = self._extract_product(it)
                    if not any(
                            p['product_name'].upper() ==
                            item['product_name'].upper() or
                            [i for i in p['brands'].split(",") 
                                if i in item['brands'].split(",")]
                            for p in self.products):
                        self.products.append(item)
                        cpt_new_products += 1
                except KeyError as err:
                    log.debug("KeyError : " + str(err))
        return cpt_new_products

    def _extract_product(self, product_raw_data):
        ''' Extracts informations that we need from
            the raw data of the product and returns it
            as a new dictionary.
        '''
        product = {
            "product_name": product_raw_data['product_name_fr'],
            "ingredients": product_raw_data['ingredients_text_fr'],
            "stores": product_raw_data['stores'],
            "product_url": product_raw_data['url'],
            "nutriscore": product_raw_data['nutrition_grades'],
            "popularity_score": product_raw_data['unique_scans_n'],
            "brands": product_raw_data['brands'],
            "categories": product_raw_data['categories']
        }
        return product

    def _insert_datas_to_db(self):
        ''' Insert datas to the database
        '''
        # Connect to database
        db = records.Database(
            'mysql+pymysql://{name}:{pwd}@localhost/{db}?{cset}'.format(
                    name=self.db_infos['user']['name'],
                    pwd=self.db_infos['user']['password'],
                    db=self.db_infos['name'],
                    cset='charset=utf8mb4'))
        db.query("SET NAMES 'utf8mb4'")
        # Delete all datas before inserting
        db.query("DELETE FROM Product_Category")
        db.query("DELETE FROM Product")
        db.query("DELETE FROM Category")
        # insert Categories entities
        for cat in self.categories:
            db.query(
                "INSERT INTO Category (category_name, category_id_off) \
                    VALUES(:name, :id) \
                    ON DUPLICATE KEY UPDATE category_name = category_name",
                name=cat['name'], id=cat['id'])
        # insert Products entities
        for p in self.products:
            db.query(
                "INSERT INTO Product ( \
                    product_name, \
                    ingredients, \
                    stores, \
                    product_url, \
                    nutriscore, \
                    popularity_score) \
                VALUES( \
                    :name, \
                    :ingredients, \
                    :stores, \
                    :url, \
                    :nutriscore, \
                    :pop_score)",
                name=p['product_name'] + " (" + p['brands'] + ")",
                ingredients=p['ingredients'],
                stores=p['stores'],
                url=p['product_url'],
                nutriscore=p['nutriscore'],
                pop_score=p['popularity_score'])
            # insert Product_Category relations
            id_p = db.query("SELECT LAST_INSERT_ID() AS id").first()
            for c in p["categories"].split(","):
                try:
                    id_cat = db.query(
                        "SELECT id \
                        FROM Category \
                        WHERE category_name = :cat \
                        OR category_id_off = :cat",
                        cat=c).first()
                    db.query(
                        "INSERT INTO Product_Category (id_product, id_category) \
                        VALUES(:id_product, :id_category)",
                        id_product=id_p['id'],
                        id_category=id_cat['id'])
                except TypeError as err:
                    log.debug(
                        ("Error: {err} (While inserting product_category, "
                         "corresponding category not found)").format(err=err))


if __name__ == "__main__":
    MY_UPDATER = Updater()