-- Create the database
CREATE DATABASE hall_of_famers;

-- Use the newly created database
USE hall_of_famers;
GO

-- Create the Players table
CREATE TABLE players (
    player_id INT PRIMARY KEY,
    team_id INT,
    stat_id INT,
    accolade_id INT,
    player_firstname VARCHAR(50),
    player_lastname VARCHAR(50),
    player_dob DATE,
    player_position VARCHAR(50),
    player_height FLOAT,
    player_weight FLOAT,
    player_nationality VARCHAR(100)
);
GO

-- Create the Teams table
CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(50),
    team_city VARCHAR(50),
    team_state VARCHAR(50)
);
GO

-- Create the Seasons table
CREATE TABLE seasons (
    season_id INT PRIMARY KEY,
    season_year INT,
    season_description VARCHAR(255),
    season_made_playoffs BIT
);
GO

-- Create the Accolades table
CREATE TABLE accolades (
    accolade_id INT PRIMARY KEY,
    player_id INT,
    accolade_mvp_status BIT,
    accolade_rookie_of_year SMALLINT,
    accolade_finals_mvp SMALLINT,
    accolade_scoring_title SMALLINT,
    accolade_defensive_poy SMALLINT,
    accolade_championships SMALLINT,
    accolade_olympic_medals VARCHAR(255)
);
GO

-- Create the Stats table
CREATE TABLE statis (
    stat_id INT PRIMARY KEY,
    player_id INT,
    season_id INT,
    stat_points INT,
    stat_assists INT,
    stat_rebounds INT,
    stat_steals INT,
    stat_blocks INT,
    stat_turnovers INT,
    stat_minutes_played INT,
    stat_seasons_played INT
);
GO

-- Create foreign key relationships
ALTER TABLE players 
DROP CONSTRAINT IF EXISTS FK_players_teams;
GO
ALTER TABLE players
ADD CONSTRAINT FK_players_teams FOREIGN KEY (team_id) REFERENCES teams(team_id);

ALTER TABLE players 
DROP CONSTRAINT IF EXISTS FK_players_statis;
GO
ALTER TABLE players
ADD CONSTRAINT FK_players_statis FOREIGN KEY (stat_id) REFERENCES statis(stat_id);

ALTER TABLE players
DROP CONSTRAINT IF EXISTS FK_players_accolades;
GO
ALTER TABLE players
ADD CONSTRAINT FK_players_accolades FOREIGN KEY (accolade_id) REFERENCES accolades(accolade_id);

ALTER TABLE accolades
DROP CONSTRAINT IF EXISTS FK_accolades_players;
GO
ALTER TABLE accolades
ADD CONSTRAINT FK_accolades_players FOREIGN KEY (player_id) REFERENCES players(player_id);


ALTER TABLE statis 
DROP CONSTRAINT IF EXISTS FK_statis_players;
GO
ALTER TABLE statis
ADD CONSTRAINT FK_statis_players FOREIGN KEY (player_id) REFERENCES players(player_id);

ALTER TABLE statis 
DROP CONSTRAINT IF EXISTS FK_statis_seasons;
GO
ALTER TABLE statis
ADD CONSTRAINT FK_statis_seasons FOREIGN KEY (season_id) REFERENCES seasons(season_id);


-- Insert data into the Teams table
INSERT INTO teams (team_id, team_name, team_city, team_state) VALUES
(1, 'Lakers', 'Los Angeles', 'California'),
(2, 'Bulls', 'Chicago', 'Illinois'),
(3, 'Celtics', 'Boston', 'Massachusetts'),
(4, 'Warriors', 'San Francisco', 'California'),
(5, 'Heat', 'Miami', 'Florida');
GO

-- Insert data into the Seasons table
INSERT INTO seasons (season_id, season_year, season_description, season_made_playoffs) VALUES
(5, 2021, '2020-2021 NBA Season', 1),
(4, 2020, '2019-2020 NBA Season', 1),
(3, 2019, '2018-2019 NBA Season', 1),
(2, 2018, '2017-2018 NBA Season', 1),
(1, 2017, '2016-2017 NBA Season', 1);
GO

-- Insert data into the Accolades table
INSERT INTO accolades (accolade_id, player_id, accolade_mvp_status, accolade_rookie_of_year, accolade_finals_mvp, accolade_scoring_title, accolade_defensive_poy, accolade_championships, accolade_olympic_medals) VALUES
(1, 1, 1, 0, 1, 0, 1, 3, 2),
(2, 2, 0, 1, 0, 1, 0, 1, 1),
(3, 3, 1, 0, 1, 0, 0, 2, 1),
(4, 4, 0, 0, 0, 0, 1, 4, 3),
(5, 5, 1, 0, 1, 1, 1, 2, 0);
GO

-- Insert data into the Stats table
INSERT INTO statis (stat_id, player_id, season_id, stat_points, stat_assists, stat_rebounds, stat_steals, stat_blocks, stat_turnovers, stat_minutes_played, stat_seasons_played) VALUES
(1, 1, 1, 2500, 800, 600, 200, 100, 300, 2400, 10),
(2, 2, 2, 2300, 700, 500, 150, 90, 250, 2300, 9),
(3, 3, 3, 2200, 600, 550, 180, 95, 200, 2200, 8),
(4, 4, 4, 2400, 750, 620, 210, 110, 280, 2500, 11),
(5, 5, 5, 2600, 850, 700, 220, 120, 320, 2600, 12);
GO

-- Insert data into the Players table
INSERT INTO Players (player_id, team_id, stat_id, accolade_id, player_firstname, player_lastname, player_dob, player_position, player_height, player_weight, player_nationality) VALUES
(1, 1, 1, 1, 'John', 'Doe', '1990-01-15', 'Guard', 6.3, 190, 'USA'),
(2, 2, 2, 2, 'Mike', 'Smith', '1989-03-22', 'Forward', 6.7, 210, 'USA'),
(3, 3, 3, 3, 'James', 'Johnson', '1991-07-18', 'Center', 6.10, 240, 'USA'),
(4, 4, 4, 4, 'Robert', 'Brown', '1992-09-30', 'Forward', 6.8, 220, 'USA'),
(5, 5, 5, 5, 'David', 'Miller', '1988-12-05', 'Guard', 6.2, 185, 'USA');
GO


SELECT * FROM players

SELECT * FROM accolades 
WHERE player_id = 1; 
GO 

SELECT p.player_id, p.player_firstname + ' ' + p.player_lastname AS player_name, a.accolade_mvp_status, a.accolade_scoring_title, a.accolade_rookie_of_year 
FROM accolades a
JOIN 
players p ON a.player_id = p.player_id
WHERE 
p.player_id= 1