# Use_Datas_OpenFoodFact

Use_Datas_OpenFoodFact is an application whose purpose is to use the data of the Open Food Fact API to provide the user with healthy foods as a substitute for other unhealthy foods. This project is part of a learning path "Python application developper" which you can find on [OpenClassrooms](https://openclassrooms.com/paths/developpeur-se-dapplication-python) web site.

## FEATURES

    - create the database from a script at localhost
    - retrieve datas from Open Food Fact API : this feature get a set of datas from the API based on our config file,
    then process raw datas to extract what we need to finally insert it in the correct format in our local database.
    It only executes the first time we launch the program and then update at a frequency that we define. We will be
    able to force the update by adding an option at the launch of the starting point of the application.
    - from the main menu the user can start a new search of healthier food : first he is prompted to choose a category
    and then a food (from 2 consecutive lists), then the application offers the user healthier alternatives to the
    chosen product. The user will then be able to pick an alternative and will have the possibility to save the result
    so he can consult it later.
    - from the main menu the user can also choose to consult the history of his saved searches

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

First you need to have Python 3 installed on your system. 

For this project I used Pipenv to create a virtual env that can be easily recreated on your environment. First you need to install Pipenv if you don't already have it :

```
pip install pipenv
```

Then you will have to download the source code of the project, unload it inside a folder and from this folder use the command :

```
pipenv install
```

which will automatically create a virtual environment with all the packages used for this project.

Before you start the application you will need to set a local MySQL database environment for this application. The name of the database, the username and password must match those filled in the config/config.json file.

Finally to launch the game in the context of its virtual environment use the command :

```
pipenv run python udoff.py
```

## Packages used

* [requests](https://github.com/requests/requests) - HTTP for Humans : Non-GMO HTTP library for Python, safe for human consumption.
* [records](https://github.com/kennethreitz/records) - SQL for Humans : Records is a very simple, but powerful, library for making raw SQL queries to most relational databases.
* [pymysql](https://github.com/PyMySQL/PyMySQL) - Pure-Python MySQL client library : the goal of PyMySQL is to be a drop-in replacement for MySQLdb and work on CPython, PyPy and IronPython.

