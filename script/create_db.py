import os
from lib.models import *


def create_tables(db_file_location):
    conn = sqlite3.connect(db_file_location)
    c = conn.cursor()
    try:
        print("Creating tables...")
        Accounts.create_table(c)
        Stats.create_table(c)
        CharacterModelBase.create_table(c)
        Ability.create_table(c)
        conn.commit()
        conn.close()
        print("DB Created.")
    except sqlite3.OperationalError as e:
        print("Error in creating DB  - {0}, rolling back".format(e))
        conn.close()
        os.remove(db_file_location)


if __name__ == '__main__':
    create_tables("../data/test.db")
