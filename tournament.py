#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    remove_all_matches = "UPDATE matches SET wins = 0, matches = 0;"

    conn = connect()
    c = conn.cursor()
    c.execute(remove_all_matches)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    delete_matches = "DELETE FROM matches;"
    delete_players = "DELETE FROM players;"

    conn = connect()
    c = conn.cursor()
    c.execute(delete_matches)
    c.execute(delete_players)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    get_player_count = "SELECT count(*) FROM players;"

    conn = connect()
    c = conn.cursor()
    c.execute(get_player_count)

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
    insert_player = "INSERT INTO players (name) values (%s) RETURNING id"
    insert_match = "INSERT INTO matches values (%s, %s, %s)"

    conn = connect()
    c = conn.cursor()

    c.execute(insert_player, (name,))
    player_id = c.fetchone()[0]

    c.execute(insert_match, (player_id, 0, 0))

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
    get_player_standing = 'SELECT * FROM player_match'
    conn = connect()
    c = conn.cursor()
    c.execute(get_player_standing)

    standings = c.fetchall()

    c.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    update_winner = '''
    UPDATE matches
    SET wins = wins + 1, matches = matches + 1
    WHERE id = %s
    '''

    update_loser = '''
    UPDATE matches
    SET matches = matches + 1
    WHERE id = %s
    '''

    conn = connect()
    c = conn.cursor()

    c.execute(update_winner, (winner,))
    c.execute(update_loser, (loser,))

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

    get_max_wins = "SELECT * FROM max_wins"

    c.execute(get_max_wins)
    max_wins = c.fetchone()[0]

    parings = []
    get_players_same_win = "SELECT * FROM player_match WHERE wins = %s"
    for wins in xrange(max_wins, -1, -1):
        c.execute(get_players_same_win, (wins,))
        players = c.fetchall()

        while players:
            a = random.choice(players)
            players.remove(a)
            b = random.choice(players)
            players.remove(b)

            parings.append((a[0], a[1], b[0], b[1]))

    conn.close()
    return parings
