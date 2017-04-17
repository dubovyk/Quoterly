import sqlite3
import time


class sqliteConnector:
    def __init__(self, dbpath):
        self.__dbpath = dbpath
        self.__connection = sqlite3.connect(self.__dbpath)  # initialize 'connection' (actually, open file)
        self.__cursor = self.__connection.cursor()

    def add_user(self, username, usermail, userpass):
        self.__cursor.execute("INSERT INTO User (username, email, regdate, pass_hash) VALUES (\"{}\", \"{}\", \"{}\", \"{}\");".format(username, usermail, time.ctime(), userpass))
        self.__connection.commit()  # should be done to finish operation

    def is_available_user(self, username, usermail):
        self.__cursor.execute(("SELECT * FROM User WHERE username=\"{}\" OR email=\"{}\";").format(username, usermail))
        data = self.__cursor.fetchall()
        return len(data) == 0

    def get_user(self, username):
        self.__cursor.execute(("SELECT * FROM User WHERE username=\"{}\" OR email=\"{}\";").format(username, username))
        data = self.__cursor.fetchone()
        return data

    def drop(self):
        self.__cursor.execute("DROP TABLE IF EXISTS User;")
        self.__cursor.execute("DROP TABLE IF EXISTS Quote;")
        self.__connection.commit()

    def create(self):
        self.__cursor.execute("CREATE TABLE User (username varchar,email varchar,regdate datetime,pass_hash varchar,is_admin boolean default false)")
        self.__cursor.execute("CREATE TABLE Quote (id integer PRIMARY KEY AUTOINCREMENT,"
                              "quote_text text,author text,username varchar,publication_date datetime);")
        self.__connection.commit()

    def match_password(self, username, password):
        self.__cursor.execute(("SELECT * FROM User WHERE username=\"{}\" AND pass_hash=\"{}\";").format(username, password))
        data = self.__cursor.fetchall()
        return len(data) != 0

    def is_admin(self, username):
        self.__cursor.execute("SELECT is_admin FROM User WHERE username=\"{}\";".format(username))
        data = self.__cursor.fetchall()
        if len(data) == 0:
            return False
        return data[0][0] == 'true'

    def update_user(self, username, fieldname, fieldvalue):
        self.__cursor.execute("UPDATE User SET {}=\"{}\" WHERE username=\"{}\";".format(fieldname, fieldvalue, username))
        self.__connection.commit()

    def delete_user(self, username):
        self.__cursor.execute("DELETE FROM User WHERE username=\"{}\";".format(username))
        self.__connection.commit()

    def add_quote(self, text, author, username):
        self.__cursor.execute("INSERT INTO Quote (quote_text, author, username, publication_date) VALUES (\"{}\", \"{}\", \"{}\", \"{}\");".format(text, author, username, time.ctime()))
        self.__connection.commit()
        self.__cursor.execute("SELECT * FROM Quote WHERE quote_text=\"{}\" AND author=\"{}\";".format(text, author))
        data = self.__cursor.fetchall()
        return data[-1]

    def get_random_quote(self):
        self.__cursor.execute("SELECT * FROM Quote ORDER BY RANDOM() LIMIT 1;")
        data = self.__cursor.fetchone()
        if not data:
            return None
        return data

    def get_quote_by_id(self, id):
        self.__cursor.execute("SELECT * FROM Quote WHERE id=\"{}\";".format(id))
        data = self.__cursor.fetchone()
        if not data:
            return None
        return data

    def get_quotes_by_user(self, username):
        self.__cursor.execute("SELECT * FROM Quote WHERE username=\"{}\";".format(username))
        data = self.__cursor.fetchall()
        if len(data) == 0:
            return None
        return data

    def update_quote_field(self, quote_id, field, value):
        self.__cursor.execute("UPDATE Quote SET {}=\"{}\" WHERE id=\"{}\";".format(field, value, quote_id))
        self.__connection.commit()

    def delete_quote(self, quote_id):
        self.__cursor.execute("DELETE FROM Quote WHERE id=\"{}\";".format(quote_id))
        self.__connection.commit()

    def get_user_by_quote(self, quote_id):
        query = "SELECT username FROM Quote WHERE id=\"{}\";".format(quote_id)
        self.__cursor.execute(query)
        data = self.__cursor.fetchone()
        if not data:
            return None
        return data[0]

    def reset(self):
        self.drop()
        self.create()
