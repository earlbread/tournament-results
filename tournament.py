#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.

    Returns a database connection and database cursor
    """
    try:
        conn = psycopg2.connect('dbname=tournament')
        cursor = conn.cursor()
        return conn, cursor
    except:
        print 'DB Connection error occurred'


def deleteMatches():
    """Remove all the match records from the database."""
    remove_all_matches = 'DELETE FROM matches;'

    conn, cursor = connect()
    cursor.execute(remove_all_matches)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    delete_matches = 'DELETE FROM matches;'
    delete_players = 'DELETE FROM players;'

    conn, cursor = connect()
    cursor.execute(delete_matches)
    cursor.execute(delete_players)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    get_player_count = 'SELECT count(*) FROM players;'

    conn, cursor = connect()
    cursor.execute(get_player_count)

    cnt = cursor.fetchone()[0]
    conn.close()

    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    insert_player = 'INSERT INTO players (name) values (%s) RETURNING id'

    conn, cursor = connect()

    cursor.execute(insert_player, (name,))

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
    get_player_standings = 'SELECT * FROM player_standings'

    conn, cursor = connect()
    cursor.execute(get_player_standings)

    standings = cursor.fetchall()

    conn.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    report_match = 'INSERT INTO matches (winner, loser) VALUES (%s, %s)'

    conn, cursor = connect()

    cursor.execute(report_match, (winner, loser))

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
    conn, cursor = connect()

    get_player_standings = 'SELECT id, name from player_standings order by wins'

    cursor.execute(get_player_standings)
    standings = cursor.fetchall()

    parings = []
    while standings:
        id1, name1 = standings.pop()
        id2, name2 = standings.pop()

        parings.append((id1, name1, id2, name2))

    conn.close()
    return parings
