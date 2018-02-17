# Use_Datas_OpenFoodFact

Use_Datas_OpenFoodFact is an application whose purpose is to use the data of the Open Food Fact API to provide the user with healthy foods as a substitute for other unhealthy foods. This project is part of a learning path "Python applicaton developper" which you can find on [OpenClassrooms](https://openclassrooms.com/paths/developpeur-se-dapplication-python) web site.

## FEATURES

    - create the database from a script (INI_DB.sql) at localhost
    - retrieve datas from Open Food Fact API : this feature get a set of datas from the API based on our config file,
    then process raw datas to extract what we need to finally insert it in the correct format in our local database.
    It only executes the first time we launch the program and then update at a frequency that we define. We will be
    able to force the update by adding an option at the launch of the starting point of the application.
    - from the main menu the user can start a new search of healthier food : first he is prompted to choose a category
    and then a food (from 2 consecutive lists), then the application offers the user healthier alternatives to the
    chosen product. The user will then be able to pick an alternative and will have the possibility to save the result
    so he can consult it later.
    - from the main menu the user can also choose to consult the history of his saved searches