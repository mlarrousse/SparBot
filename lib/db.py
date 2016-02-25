import sqlite3
from script import create_db
import os

DB_FILE = 'data/test.db'
DB_FILE = '../data/test.db'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()


def tuple_to_stats(tuple):
    stats = {
        "Strength" : tuple[0],
        "Dexterity": tuple[1],
        "Stamina"  : tuple[2],
        "Intelligence"  : tuple[3],
        "Wisdom"  : tuple[4],
        "Charisma"  : tuple[5],
        "Luck"  : tuple[6],
    }
    return stats


def register_user(username, character_name):
    if not user_is_registered(username):
        print("Registering {0}".format(username))
        c.execute("INSERT INTO Accounts VALUES ('{username}', '1');".format(username=username))
        response = c.execute("INSERT INTO stats (Strength, Dexterity, Stamina, Intelligence, Wisdom, Charisma, Luck)"
                             " VALUES ('1', '1', '1', '1', '1', '1', '1');")
        stats_id = response.fetchone()
        print(stats_id)
        c.execute("INSERT INTO characters VALUES ('{username}', '{character_name}');".
                  format(username=username, character_name=character_name))
        conn.commit()


def user_is_registered(username):
    print("Checking {0}".format(username))
    print("SELECT * FROM Accounts WHERE username = '{username}';".format(username=username))
    response = c.execute("SELECT * FROM Accounts WHERE username = '{username}';".format(username=username)).fetchone()
    if response:
        print("Found registration {0}".format(response))
        return True
    else:
        print("User not found. Response: {response}".format(response=response))
        return False


def create_npc(name, stats):
    print("Creating npc {0}...".format(name))
    c.execute("INSERT INTO characters VALUES ('game_master', '{name}');".
              format(name=name))
    c.execute("INSERT INTO stats (character_name, MaxHealth, CurrentHealth, Strength, Dexterity, Stamina, Intelligence, Wisdom, Charisma, Luck)"
               " VALUES ('game_master', '{MaxHealth}', '{CurrentHealth}', '{Strength}', '{Dexterity}', '{Stamina}', '{Intelligence}', '{Wisdom}', '{Charisma}', '{Luck}');".format(
                MaxHealth=stats.maxHealth, CurrentHealth=stats.currentHealth, Strength=stats.strength, Dexterity=stats.dexterity, Stamina=stats.stamina, Intelligence=stats.intellect, Wisdom=stats.wisdom, Charisma=stats.charisma, Luck=stats.luck))
    conn.commit()
    print("NPC {0} created.".format(name))


def close_connection():
    conn.close()

if __name__ == '__main__':
    DB_FILE = "../data/test.db"

    if not os.path.isfile(DB_FILE):
        print("Creating DB: {0}".format(DB_FILE))
        create_db.create_tables(DB_FILE)
    register_user("mary", "mary")
    print(get_character_stats("mary"))
    close_connection()
