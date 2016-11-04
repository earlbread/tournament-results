#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    QUERY = "UPDATE matches SET wins = 0, matches = 0;"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DELETE_MATCHES = "DELETE FROM matches;"
    DELETE_PLAYERS = "DELETE FROM players;"

    conn = connect()
    c = conn.cursor()
    c.execute(DELETE_MATCHES)
    c.execute(DELETE_PLAYERS)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    QUERY = "SELECT count(*) FROM players;"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)

    cnt = c.fetchone()[0]
    conn.close()

    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    INSERT_PLAYER = "INSERT INTO players (name) values (%s) RETURNING id"
    INSERT_MATCH = "INSERT INTO matches values (%s, %s, %s)"

    conn = connect()
    c = conn.cursor()

    c.execute(INSERT_PLAYER, (name,))
    player_id = c.fetchone()[0]

    c.execute(INSERT_MATCH, (player_id, 0, 0))
    
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    QUERY = '''
    SELECT players.id, players.name, matches.wins, matches.matches
    FROM players, matches
    WHERE players.id = matches.id
    '''
    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)

    standings = c.fetchall()

    c.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    WINNER = '''
    UPDATE matches 
    SET wins = wins + 1, matches = matches + 1
    WHERE id = %s
    '''

    LOSER = '''
    UPDATE matches 
    SET matches = matches + 1
    WHERE id = %s
    '''

    conn = connect()
    c = conn.cursor()

    c.execute(WINNER, (winner,))
    c.execute(LOSER, (loser,))

    conn.commit()
    conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM max_wins")
    max_wins = c.fetchone()[0]

    parings = []
    for wins in xrange(max_wins, -1, -1):
        c.execute("SELECT * FROM player_match WHERE wins = %s", (wins,))
        players = c.fetchall()
        
        while players:
            a = random.choice(players)
            players.remove(a)
            b = random.choice(players)
            players.remove(b)

            parings.append((a[0], a[1], b[0], b[1]))
        
    conn.close();
    return parings





