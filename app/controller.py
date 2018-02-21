#!/usr/bin/env python3
# coding: utf-8

""" This module implements the logic of the differents
    user-case, it makes the calls to the model and the
    displayer.
"""

import logging as log
from . import displayer as di
from . import model as mo

# log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.CRITICAL)


class Controller:
    """ This class contains the core of the logic
        of the application, it is directly implemented
        by the starting point of the application
    """

    def __init__(self):
        self.my_displayer = di.Displayer()
        self.my_model = mo.Model()

    def start(self):
        """ Launch the main menu of the application,
            starting point of the differents scenarios
        """
        while True:
            response = self.my_displayer.main_menu()
            if response == 1:
                self.search_worflow()
            elif response == 2:
                self.history_workflow()
            elif response == 3:
                self.my_displayer.quit_display()
                return True

    def search_worflow(self):
        """ start the workflow of searching a substitute :
                1) Select a category
                2) Select a product to remplace
                3) Select a substitute
                4) Display of the detailed results, user
                can save the search
        """
        # category choice
        categories = self.my_model.get_categories()
        while True:
            i = self.my_displayer.category_choice(categories)
            if i == 0:
                return True
            elif i in range(1, len(categories)+1):
                id_cat = categories[i-1]['Id']
                break
        # search product choice
        search_products = self.my_model.get_search_products(id_cat)
        while True:
            i = self.my_displayer.search_product_choice(search_products)
            if i == 0:
                return True
            elif i in range(1, len(search_products)+1):
                id_sp = search_products[i-1]['Id']
                break
        # substitute choice
        substitutes = self.my_model.get_substitute_products(id_cat, id_sp)
        while True:
            i = self.my_displayer.substitute_choice(substitutes)
            if i == 0:
                return True
            elif i in range(1, len(substitutes)+1):
                id_sub = substitutes[i-1]['Id']
                break
        # results of the search
        search_product_details = self.my_model.get_product_details(id_sp)
        substitute_details = self.my_model.get_product_details(id_sub)
        while True:
            i = self.my_displayer.search_results(
                search_product_details,
                substitute_details)
            if i == 1:
                self.my_model.save_search(id_sp, id_sub)
                print('Recherche sauvegardée.')
                return True
            elif i == 2:
                return True

    def history_workflow(self):
        """ Start the workflow of consulting the history:
                1) Display the history of saved searches
        """
        history = self.my_model.get_history()
        while True:
            i = self.my_displayer.history(history)
            if i == 1:
                return True
