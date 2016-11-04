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
    id SERIAL REFERENCES players,
    wins INTEGER,
    matches INTEGER
);

CREATE VIEW player_match as (
    SELECT players.id, players.name, matches.wins, matches.matches
    FROM players, matches
    WHERE players.id = matches.id
);

CREATE VIEW max_wins as (
    SELECT max(wins)
    FROM player_match
);
