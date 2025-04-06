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

-- INDEX 


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


-- PROCEDURES
-- Prends un jeu random et retourne l'id et le nom du jeu 
drop procedure if exists get_random_game;
DELIMITER //
CREATE PROCEDURE get_random_game()
BEGIN
    SELECT game_id,name FROM Game ORDER BY RAND() LIMIT 1;
END;
//
DELIMITER ;

call get_random_game;

-- 
drop procedure if exists game;
DELIMITER //
create procedure Game(jeu_id int)
begin
    select * from GameDetails where game_id = jeu_id;
end
//
DELIMITER ;

call Game(3);

-- 
drop procedure if exists Description
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
drop procedure if exists search_game
DELIMITER //
create procedure search_game(game varchar(500))
begin
	select * from GameDetails where Nom_Jeu = game;
end
// 
DELIMITER ;

call search_game('catan') 
	