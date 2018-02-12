CREATE DATABASE UDOFF CHARACTER SET 'utf8mb4';
USE UDOFF;

-- CREATE TABLES

    -- TABLE : Product
    CREATE TABLE Product (
        id INT UNSIGNED AUTO_INCREMENT,
        product_name VARCHAR(200) NOT NULL UNIQUE,
        ingredients TEXT,
        stores TEXT,
        product_url VARCHAR(2100),
        nutriscore CHAR(1),
        popularity_score INT UNSIGNED,
        PRIMARY KEY(id)
    )ENGINE=INNODB;

    -- TABLE : Category
    CREATE TABLE Category (
        id INT UNSIGNED AUTO_INCREMENT,
        category_name VARCHAR(150) NOT NULL,
        category_id_off VARCHAR(150) NOT NULL,
        UNIQUE(category_name, category_id_off),
        PRIMARY KEY(id)
    )ENGINE=INNODB;

    -- TABLE : Product_Category
    CREATE TABLE Product_Category (
        id_product INT UNSIGNED,
        id_category INT UNSIGNED,
        PRIMARY KEY(id_product, id_category)
    )ENGINE=INNODB;

    -- TABLE : Record
    CREATE TABLE Record (
        id INT UNSIGNED AUTO_INCREMENT,
        search_date DATETIME NOT NULL,
        product_start_name INT UNSIGNED,
        substitute_name INT UNSIGNED,
        url_substitute VARCHAR(2100),
        PRIMARY KEY(id)
    )ENGINE=INNODB;

-- CREATE ADDITIONNALS INDEXES

    -- index Record : search_date
    ALTER TABLE Record
    ADD INDEX ind_record_search_date (search_date);

    -- index Category : category_name
    ALTER TABLE Category
    ADD INDEX ind_cat_name (category_name);

    -- index Product : nutriscore, product_name
    ALTER TABLE Product
    ADD INDEX ind_product_nutriscore_name (nutriscore, product_name);

-- CREATE FOREIGN KEY

    -- foreign key Product_Category : id_product
    ALTER TABLE Product_Category
    ADD CONSTRAINT fk_prod_cat_id_product FOREIGN KEY (id_product) REFERENCES Product(id);

    -- foreign key Product_Category : id_category
    ALTER TABLE Product_Category
    ADD CONSTRAINT fk_prod_cat_id_category FOREIGN KEY (id_category) REFERENCES Category(id);