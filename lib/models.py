from collections import defaultdict
import weakref
import sqlite3

DB_FILE = "../data/test.db"

class Model:
    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))
        print("Adding weakref" + str(weakref.ref(self)))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst

    @classmethod
    def get_instance(cls, key, value):
        for inst in cls.get_instances():
            if inst().get_attribute(key) == value:
                return inst

    @classmethod
    def get(cls, key, value):
        print(cls.__name__)
        existing_model_object = cls.get_instance(key, value)
        if existing_model_object:
            print("obj in memeory")
            return existing_model_object
        else:
            print("Getting {0} from db".format(cls.__name__))
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            response = cursor.execute("SELECT * FROM {tablename} WHERE {key} = '{value}';".format(
                                            tablename=cls.__name__, key=key, value=value))
            db_tuple = response.fetchone()
            conn.close()
            if db_tuple:
                return cls(*db_tuple)
            else:
                return None

    def create(self):
        attrs = self.__dict__
        insert_str = "INSERT INTO {class_name} ".format(self.__class__.__name__)
        column_headers_str = "("
        values_str = "VALUES ("
        for key in attrs.keys():
            column_headers_str += key
            column_headers_str += ", "
            values_str += "'"
            values_str += attrs[key]
            values_str += "', "
        create_row_str = insert_str
        create_row_str += column_headers_str
        create_row_str = create_row_str[:-2]
        create_row_str += ") "
        create_row_str += values_str
        create_row_str = create_row_str[:-2]
        create_row_str += ");"




class Accounts(Model):

    def __init__(self, username, level):
        super(Accounts, self).__init__()
        self.username = username
        self.level = level

    @staticmethod
    def create_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS Accounts ("
                       "username TEXT UNIQUE,"
                       "level REAL);")


class Characters(Model):

    def __init__(self, name, owner):
        super(Characters, self).__init__()
        self.name = name
        self.owner = owner
        self.stats = Stats.get("character_name", self.name)

    @staticmethod
    def create_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS characters ("
                       "owner TEXT, "
                       "name TEXT, "
                       "FOREIGN KEY(owner) REFERENCES accounts(username));")

    def __str__(self):
        return self.name


class Stats(Model):

    def __init__(self, maxHealth=1, currenthealth=1, strength=1, dexterity=1, stamina=1, intellect=1,
                       wisdom=1, charisma=1, luck=1):
        super(Stats, self).__init__()
        self.maxHealth = maxHealth
        self.currentHealth = currenthealth
        self.strength = strength
        self.dexterity = stamina
        self.stamina = dexterity
        self.intellect = intellect
        self.wisdom = wisdom
        self.charisma = charisma
        self.luck = luck

    @staticmethod
    def create_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS stats ("
                       "character_name TEXT, "
                       "MaxHealth INT, "
                       "CurrentHealth INT, "
                       "Strength INT, "
                       "Dexterity INT, "
                       "Stamina INT, "
                       "Intelligence INT, "
                       "Wisdom INT, "
                       "Charisma INT, "
                       "Luck INT, "
                       "FOREIGN KEY(character_name) REFERENCES character(name));")


class Ability(Model):

    def __init__(self):
        super(Ability, self).__init__()
        pass

    @staticmethod
    def create_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS ability ("
                       "Name TEXT, "
                       "PowerCost TEXT, "
                       "ManaCost TEXT, "
                       "Damage INT,"
                       "DamageType TEXT,"
                       "Description TEXT);")


if __name__ == "__main__":
    pass






