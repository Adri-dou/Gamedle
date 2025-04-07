Use gamedle;
-- ADVANCED FUNCTIONALITIES
-- VIEW 

CREATE VIEW GameDetails AS
SELECT 
    g.game_id,
    g.name AS Nom_Jeu,
    GROUP_CONCAT(DISTINCT c.category_name ORDER BY c.category_name SEPARATOR ', ') AS Catégories,
    g.minPlayer AS Min_Joueurs,
    g.maxPlayer AS Max_Joueurs,
    YEAR(g.yearPublished) AS Annee_Publication,
    p.name AS Editeur,
    g.ranking AS Classement
FROM Game g
LEFT JOIN is_categorised_as ic ON g.game_id = ic.game_id
LEFT JOIN Category c ON ic.category_name = c.category_name
LEFT JOIN Publisher p ON g.publisher_id = p.publisher_id
GROUP BY g.game_id, g.name, g.minPlayer, g.maxPlayer, g.yearPublished, p.name, g.ranking;

SELECT * FROM GameDetails;
--
create view Game_Description as
select 
	g.game_id,
    g.name,
    g.description
from game g
group by g.game_id, g.name, g.description;

select * from Game_Description;
--
CREATE VIEW View_GameOfTheDay AS
SELECT
    g.game_id,
    g.name,
    go.date
FROM GameOfTheDay go
JOIN Game g ON g.game_id = go.game_id;

select * from View_GameOfTheDay;

-- INDEX 
-- pour accélérer la recherche par nom de jeu
drop index idx_game on game;
create index idx_game on Game(name);
show index from game;
-- pour faciliter la recherche des jeux par catégorie
create index idx_game_category on is_categorised_as(category_name);
show index from game;
-- Index pour accélérer la recherche des jeux par année de publication
create index idx_game_year on Game(yearPublished);
show index from game;
--


-- TRIGGERS 
-- Ajoute une catégorie si elle n'existe pas lors de l'ajout d'un jeu
drop trigger insert_category
DELIMITER //
create trigger insert_category before insert on is_categorised_as
for each row
begin
    if not exists (select 1 from category where category_name = new.category_name) then
        insert into category(category_name) values (new.category_name);
    end if;
end;
//
DELIMITER ;
--
DELIMITER //
CREATE TRIGGER validate_player_number
BEFORE INSERT ON Game
FOR EACH ROW
BEGIN
    IF NEW.minPlayer > NEW.maxPlayer THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le minimum de joueur ne peut être supérieur au nombre max de joueur.';
    END IF;
END//
DELIMITER ;
--
DELIMITER //
CREATE TRIGGER validate_publication_year
BEFORE INSERT ON Game
FOR EACH ROW
BEGIN
    IF NEW.yearPublished > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La date ne doit pas etre dans le futur !';
    END IF;
END//
DELIMITER ;
--
DELIMITER //
CREATE TRIGGER set_random_game_for_date
BEFORE INSERT ON GameOfTheDay
FOR EACH ROW
BEGIN
    DECLARE random_game_id INT;

    IF NEW.game_id IS NULL THEN
        SELECT game_id INTO random_game_id FROM Game ORDER BY RAND() LIMIT 1;
        SET NEW.game_id = random_game_id;
    END IF;
END;
//
DELIMITER ;
INSERT INTO GameOfTheDay (date) VALUES (DATE(NOW()));
-- PROCEDURES
-- Prends un jeu random et retourne l'id et le nom du jeu 
drop procedure get_random_game;
DELIMITER //
CREATE PROCEDURE get_random_game()
BEGIN
    SELECT game_id,name FROM Game ORDER BY RAND() LIMIT 1;
END;
//
DELIMITER ;

call get_random_game;

-- 
drop procedure game;
DELIMITER //
create procedure get_game(jeu_id int)
begin
    select * from GameDetails where game_id = jeu_id;
end
//
DELIMITER ;

call get_game(3);

-- 
drop procedure Description
DELIMITER //
create procedure Description(jeu_id int)
begin
    select description from Game_Description where game_id = jeu_id;
end
//
DELIMITER ;
call Description(3);
-- 
-- Pour chercher un jeu 
drop procedure search_game
DELIMITER //
create procedure search_game(game varchar(500))
begin
	select * from GameDetails where Nom_Jeu = game;
end
// 
DELIMITER ;

call search_game('catan') 
	