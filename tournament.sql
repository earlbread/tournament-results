-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players(id),
    loser INTEGER REFERENCES players(id)
);

CREATE VIEW player_wins as (
    SELECT players.id as player, count(matches.winner) as wins
    FROM players LEFT JOIN matches
    ON players.id = matches.winner
    GROUP BY players.id
    ORDER BY players.id
);

CREATE VIEW player_matches as (
    SELECT players.id as player, count(matches) as matches
    FROM players LEFT JOIN matches
    ON players.id = matches.winner or players.id = matches.loser
    GROUP BY players.id
    ORDER BY players.id
);

CREATE VIEW player_standings as (
    SELECT players.id, players.name, wins, matches
    FROM players, player_wins, player_matches
    WHERE players.id = player_wins.player and players.id = player_matches.player
);
