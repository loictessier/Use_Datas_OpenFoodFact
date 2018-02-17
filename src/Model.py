#!/usr/bin/env python3
# coding: utf-8

from os import path
import logging as log
import json
import records
import ast

# log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.CRITICAL)


class Model:
    ''' DOCSTRING
    '''

    def __init__(self):
        self.db_infos = dict()
        self._read_config_json('config.json')
        self.db = records.Database(
            'mysql+pymysql://{name}:{pwd}@localhost/{db}?{cset}'.format(
                    name=self.db_infos['user']['name'],
                    pwd=self.db_infos['user']['password'],
                    db=self.db_infos['name'],
                    cset='charset=utf8mb4'))

    def _read_config_json(self, filename):
        """ Read the config file and extract the informations
            we need to connect to the database
        """
        # Open the config file and read data
        directory = path.dirname(path.dirname(__file__))
        path_to_file = path.join(directory, "config", filename)
        try:
            with open(path_to_file) as json_data:
                data = json.load(json_data)
        except FileNotFoundError as err:
            log.critical('Error: %s' % err)
        # extract database informations
        self.db_infos = data['local_database']

    def get_categories(self):
        ''' Get the most populated categories
            from database and returns them
        '''
        rows = self.db.query(
            "SELECT Cat.id as Id, cat.category_name as Name "
            "FROM Category AS Cat "
            "INNER JOIN Product_Category AS Pc ON Cat.id = Pc.id_category "
            "GROUP BY Cat.id, Cat.category_name "
            "ORDER BY COUNT(Pc.id_product) DESC "
            "LIMIT 20")
        return ast.literal_eval(rows.export('json'))

    def get_search_products(self, id_category):
        ''' Get the most popular products in
            category passed as parameter with
            bad nutrition grade (e or d)
        '''
        rows = self.db.query(
            "SELECT P.id as Id, "
            "P.product_name as Name, "
            "P.popularity_score as Popularity_score, "
            "P.nutriscore as Nutriscore "
            "FROM Product as P "
            "INNER JOIN Product_Category as Pc ON P.id = Pc.id_product "
            "WHERE Pc.id_category = :id_cat "
            "AND P.nutriscore in ('e', 'd') "
            "ORDER BY P.nutriscore DESC, P.popularity_score DESC "
            "LIMIT 40",
            id_cat=id_category)
        return ast.literal_eval(rows.export('json'))

    def get_substitute_products(self, id_category, id_search_product):
        ''' Get the most accurate healthy substitutes for
            a given search_product and a category.
        '''
        rows = self.db.query(
            "SELECT "
            "    P.id as Id, "
            "    P.product_name as Name, "
            "    P.nutriscore as Nutriscore "
            "FROM Product P "
            "INNER JOIN Product_Category AS PC "
            "    ON P.id = PC.id_product "
            "INNER JOIN Product_Category AS PC2 "
            "    ON P.id = PC2.id_product "
            "INNER JOIN Product_Category AS PC3 "
            "    ON PC2.id_category = PC3.id_category "
            "WHERE P.nutriscore in ('a', 'b') "
            "AND PC.id_category = :cat_id "
            "AND PC3.id_product = :p_id "
            "GROUP BY P.id, P.product_name, P.nutriscore "
            "ORDER BY P.nutriscore ASC, COUNT(PC2.id_category) DESC ",
            cat_id=id_category,
            p_id=id_search_product)
        return ast.literal_eval(rows.export('json'))

    def get_product_details(self, id_product):
        ''' Get detailled informations of one product
            passed as parameter
        '''
        rows = self.db.query(
            "SELECT * "
            "FROM Product "
            "WHERE id = :id_p",
            id_p=id_product
        ).first()
        return ast.literal_eval(rows.export('json'))

    def save_search(self, id_search_product, id_substitute):
        ''' Save the search results in the Search_history table
            of the database (based on search_product and chosen
            substitute passed as parameters)
        '''
        search_product = self.db.query(
            "SELECT product_name "
            "FROM Product "
            "WHERE id = :id_p",
            id_p=id_search_product).first()

        substitute_product = self.db.query(
            "SELECT product_name, "
            "   product_url "
            "FROM Product "
            "WHERE id = :id_p",
            id_p=id_substitute).first()

        self.db.query(
            "INSERT INTO Search_history ( \
                search_date, \
                search_product_name, \
                substitute_name, \
                url_substitute) \
            VALUES( \
                NOW(), \
                :search_product_name, \
                :substitute_name, \
                :url_substitute)",
            search_product_name=search_product['product_name'],
            substitute_name=substitute_product['product_name'],
            url_substitute=substitute_product['product_url'])

    def get_history(self):
        ''' Get the list of all search results saved
            in Search_history
        '''
        rows = self.db.query(
            "SELECT search_date, "
            "   search_product_name, "
            "   substitute_name, "
            "   url_substitute "
            "FROM Search_history "
            "ORDER BY search_date DESC")
        return ast.literal_eval(rows.export('json'))


if __name__ == "__main__":
    # my_model = Model()
    pass
