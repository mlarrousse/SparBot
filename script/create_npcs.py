import sqlite3
import os
from lib.models import Stats
from lib import db


def create_game_master(db_file_location):
    conn = sqlite3.connect(db_file_location)
    c = conn.cursor()
    try:
        print("game_master account.")
        c.execute("INSERT INTO Accounts VALUES ('game_master', '1');")
        conn.commit()
        conn.close()
        print("game_master Created.")
    except sqlite3.OperationalError as e:
        print("Error in creating game_master  - {0}, rolling back".format(e))
        conn.close()
        os.remove(db_file_location)


def create_npcs(db_file_location):
    stats = Stats()
    db.create_npc("scarecrow", stats)


if __name__ == "__main__":
    #create_game_master("../data/test.db")
    create_npcs("../data/test.db")