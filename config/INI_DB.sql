CREATE DATABASE UDOFF CHARACTER SET 'utf8mb4';
USE UDOFF;

-- CREATE TABLES

    -- TABLE : Product
    CREATE TABLE Product (
        id INT UNSIGNED AUTO_INCREMENT,
        product_name VARCHAR(200) NOT NULL,
        ingredients TEXT,
        stores TEXT,
        product_url VARCHAR(2100),
        nutriscore CHAR(1),
        PRIMARY KEY(id)
    )ENGINE=INNODB;

    -- TABLE : Category
    CREATE TABLE Category (
        id INT UNSIGNED AUTO_INCREMENT,
        category_name VARCHAR(150) NOT NULL UNIQUE,
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
        search_date DATETIME NOT NULL,
        id_product_start INT UNSIGNED,
        id_substitute INT UNSIGNED,
        PRIMARY KEY(id_product_start, id_substitute)
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

    -- foreign key Record : id_product_start
    ALTER TABLE Record
    ADD CONSTRAINT fk_Record_id_product_start FOREIGN KEY (id_product_start) REFERENCES Product(id);

    -- foreign key Record : id_substitute
    ALTER TABLE Record
    ADD CONSTRAINT fk_Record_id_substitute FOREIGN KEY (id_substitute) REFERENCES Product(id);