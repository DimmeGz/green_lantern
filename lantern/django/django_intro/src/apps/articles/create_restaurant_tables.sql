CREATE TABLE Country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(56) NOT NULL
    );


CREATE TABLE City (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(85) NOT NULL,
    country_id INT REFERENCES Country(id) ON DELETE RESTRICT
    );

CREATE TABLE Restaurant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address CHAR(50) NOT NULL UNIQUE,
    country_id INT REFERENCES Country(id),
    city_id INT REFERENCES City(id)
    );

CREATE TABLE Employee (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birthday DATE,
    position VARCHAR(20) NOT NULL,
    restaurant_id INT REFERENCES Restaurant(id) ON DELETE CASCADE
    );

CREATE TABLE Season (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(6) NOT NULL
    );

CREATE TABLE Food (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(30) NOT NULL,
    ingredients TEXT,
    vegan BOOL,
    spicy BOOL,
    season INT REFERENCES Season(id)
    );

CREATE TABLE Menu (
    ID SERIAL PRIMARY KEY NOT NULL,
    season_id INT REFERENCES Season(id),
    food_id INT REFERENCES Food(id)
    );
