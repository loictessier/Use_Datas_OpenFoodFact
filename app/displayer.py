#!/usr/bin/env python3
# coding: utf-8

""" Handle the display of informations and the interaction
    with the user
"""


class Displayer:
    """ This class contains all methods to presents
        the informations based on what we get from
        our Model module
    """

    @staticmethod
    def _get_input():
        try:
            response = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            response = 99
        return response

    @classmethod
    def main_menu(cls):
        """ Starting menu of the application
        """
        print("############################################################")
        print("###               Use Datas Open Food Fact               ###")
        print("############################################################")
        print("### 1. Quel aliment souhaitez-vous remplacer ?           ###")
        print("### 2. Retrouver mes aliments substitués.                ###")
        print("### 3. Quitter l'application.                            ###")
        print("############################################################")
        return cls._get_input()

    @classmethod
    def category_choice(cls, categories):
        """ Search workflow : choice of category
        """
        print("############################################################")
        print("###    Recherche de substitut : choix de la catégorie    ###")
        print("############################################################")
        for i, cat in enumerate(categories, 1):
            print(str(i) + ".", cat['Name'])
        print("0. Retour au menu principal")
        print("############################################################")
        return cls._get_input()

    @classmethod
    def search_product_choice(cls, search_products):
        """ Search workflow : choice of product to
            replace
        """
        print("############################################################")
        print("###      Recherche de substitut : choix du produit       ###")
        print("############################################################")
        for i, product in enumerate(search_products, 1):
            print(str(i) + ".", product['Name'])
        print("0. Retour au menu principal")
        print("############################################################")
        return cls._get_input()

    @classmethod
    def substitute_choice(cls, substitutes_products):
        """ Search workflow : choice of substitute
        """
        print("############################################################")
        print("###     Recherche de substitut : choix du substitut      ###")
        print("############################################################")
        for i, substitute in enumerate(substitutes_products, 1):
            print(
                str(i) + ".",
                substitute['Name'],
                "(" + substitute['Nutriscore'].upper() + ")"
            )
        print("0. Retour au menu principal")
        print("############################################################")
        return cls._get_input()

    @classmethod
    def search_results(cls, search_p, substitute_p):
        """ Search workflow : display of detailed results
            and choice of saving
        """
        print("############################################################")
        print("###     Recherche de substitut : Résultats détaillés     ###")
        print("############################################################")
        print("###                  Produit de départ                   ###")
        print("############################################################")
        print("###", "Name :", search_p[0]['product_name'])
        print("###", "Ingredients :", search_p[0]['ingredients'])
        print("###", "Magasins :", search_p[0]['stores'])
        print("###", "Nutriscore :", search_p[0]['nutriscore'].upper())
        print("###", "Lien OpenFoodFact :", search_p[0]['product_url'])
        print("############################################################")
        print("###                Substitut selectionné                 ###")
        print("############################################################")
        print("###", "Name :", substitute_p[0]['product_name'])
        print("###", "Ingredients :", substitute_p[0]['ingredients'])
        print("###", "Magasins :", substitute_p[0]['stores'])
        print("###", "Nutriscore :", substitute_p[0]['nutriscore'].upper())
        print("###", "Lien OpenFoodFact :", substitute_p[0]['product_url'])
        print("############################################################")
        print("### 1. Souhaitez-vous sauvegarder la recherche ?         ###")
        print("### 2. Retourner au menu principal sans sauvegarder      ###")
        print("############################################################")
        return cls._get_input()

    @classmethod
    def history(cls, search_history):
        """ History workflow : display of previous saved
            search list
        """
        print("############################################################")
        print("###              Historique des recherches               ###")
        print("############################################################")
        if search_history:
            for search in search_history:
                print("###", search['search_date'])
                print(
                    "###",
                    " "*3,
                    "Produit de départ :",
                    search['search_product_name'])
                print(
                    "###",
                    " "*3,
                    "Produit de substitution :",
                    search['substitute_name'])
                print(
                    "###",
                    " "*3,
                    "Lien du produit de substitution :",
                    search['url_substitute'])
                print("#"*60)
        else:
            print("Aucune recherche sauvegardée.")
            print("#"*60)
        print("### 1. Retourner au menu principal                       ###")
        print("############################################################")
        return cls._get_input()

    @staticmethod
    def quit_display():
        """ Display a message before leaving application
        """
        print("############################################################")
        print("################ Fermeture de l'application ################")
        print("############################################################")
        return True

if __name__ == "__main__":
    pass
