DROP DATABASE IF EXISTS gamedle;
CREATE DATABASE gamedle;

USE gamedle;

CREATE TABLE Publisher(
   publisher_id INT,
   name VARCHAR(500) NOT NULL,
   PRIMARY KEY(publisher_id)
);

CREATE TABLE Contribution(
   sector VARCHAR(500),
   PRIMARY KEY(sector)
);

CREATE TABLE Category(
   category_name VARCHAR(500),
   PRIMARY KEY(category_name)
);

CREATE TABLE Mechanic(
   mechanic_type VARCHAR(500),
   PRIMARY KEY(mechanic_type)
);

CREATE TABLE Game(
   game_id INT,
   minAge INT NOT NULL,
   minPlayer INT NOT NULL,
   ranking INT NOT NULL,
   maxPlayer INT NOT NULL,
   yearPublished DATE,
   name VARCHAR(500) NOT NULL,
   description TEXT,
   playingTime TIME NOT NULL,
   publisher_id INT,
   PRIMARY KEY(game_id),
   FOREIGN KEY(publisher_id) REFERENCES Publisher(publisher_id),
   CHECK (minPlayer <= maxPlayer)
);

CREATE TABLE Creator(
   creator_id INT,
   firstname VARCHAR(500) NOT NULL,
   surname VARCHAR(500) NOT NULL,
   sector VARCHAR(500) NOT NULL,
   PRIMARY KEY(creator_id),
   FOREIGN KEY(sector) REFERENCES Contribution(sector)
);

CREATE TABLE created(
   game_id INT,
   creator_id INT,
   PRIMARY KEY(game_id, creator_id),
   FOREIGN KEY(game_id) REFERENCES Game(game_id),
   FOREIGN KEY(creator_id) REFERENCES Creator(creator_id)
);

CREATE TABLE is_categorised_as(
   game_id INT,
   category_name VARCHAR(500),
   PRIMARY KEY(game_id, category_name),
   FOREIGN KEY(game_id) REFERENCES Game(game_id),
   FOREIGN KEY(category_name) REFERENCES Category(category_name)
);

CREATE TABLE has_mechanics(
   game_id INT,
   mechanic_type VARCHAR(500),
   PRIMARY KEY(game_id, mechanic_type),
   FOREIGN KEY(game_id) REFERENCES Game(game_id),
   FOREIGN KEY(mechanic_type) REFERENCES Mechanic(mechanic_type)
);
