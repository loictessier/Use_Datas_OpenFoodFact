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

    def __init__(self):
        pass

    def main_menu(self):
        """ Starting menu of the application
        """
        print("############################################################")
        print("###               Use Datas Open Food Fact               ###")
        print("############################################################")
        print("### 1. Quel aliment souhaitez-vous remplacer ?           ###")
        print("### 2. Retrouver mes aliments substitués.                ###")
        print("### 3. Quitter l'application.                            ###")
        print("############################################################")
        try:
            r = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            r = 99
        return r

    def category_choice(self, categories):
        """ Search workflow : choice of category
        """
        print("############################################################")
        print("###    Recherche de substitut : choix de la catégorie    ###")
        print("############################################################")
        for i in range(0, len(categories)):
            print(str(i+1) + ".", categories[i]['Name'])
        print("0. Retour au menu principal")
        print("############################################################")
        try:
            r = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            r = 99
        return r

    def search_product_choice(self, search_products):
        """ Search workflow : choice of product to
            replace
        """
        print("############################################################")
        print("###      Recherche de substitut : choix du produit       ###")
        print("############################################################")
        for i in range(0, len(search_products)):
            print(str(i+1) + ".", search_products[i]['Name'])
        print("0. Retour au menu principal")
        print("############################################################")
        try:
            r = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            r = 99
        return r

    def substitute_choice(self, substitutes_products):
        """ Search workflow : choice of substitute
        """
        print("############################################################")
        print("###     Recherche de substitut : choix du substitut      ###")
        print("############################################################")
        for i in range(0, len(substitutes_products)):
            print(
                str(i+1) + ".",
                substitutes_products[i]['Name'],
                "(" + substitutes_products[i]['Nutriscore'].upper() + ")"
            )
        print("0. Retour au menu principal")
        print("############################################################")
        try:
            r = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            r = 99
        return r

    def search_results(self, search_p, substitute_p):
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
        try:
            r = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            r = 99
        return r

    def history(self, search_history):
        """ History workflow : display of previous saved
            search list
        """
        print("############################################################")
        print("###              Historique des recherches               ###")
        print("############################################################")
        if search_history:
            for d in search_history:
                print("###", d['search_date'])
                print(
                    "###",
                    " "*3,
                    "Produit de départ :",
                    d['search_product_name'])
                print(
                    "###",
                    " "*3,
                    "Produit de substitution :",
                    d['substitute_name'])
                print(
                    "###",
                    " "*3,
                    "Lien du produit de substitution :",
                    d['url_substitute'])
                print("#"*60)
        else:
            print("Aucune recherche sauvegardée.")
            print("#"*60)
        print("### 1. Retourner au menu principal                       ###")
        print("############################################################")
        try:
            r = int(input('Sélectionnez une option du menu : '))
        except ValueError:
            r = 99
        return r

    def quit_display(self):
        """ Display a message before leaving application
        """
        print("############################################################")
        print("################ Fermeture de l'application ################")
        print("############################################################")
        return True

if __name__ == "__main__":
    pass
