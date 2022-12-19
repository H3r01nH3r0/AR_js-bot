import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_category(self):
        with self.connection:
            result = self.cursor.execute("SELECT name FROM `category`").fetchall()
            return set(result)

    def get_ctg(self):
        with self.connection:
            result = self.cursor.execute("SELECT link FROM `category`").fetchall()
            result = [i[0] for i in result]
            return result

    def get_link(self, name):
        with self.connection:
            result = self.cursor.execute("SELECT link FROM `category` WHERE name = ?", (name,)).fetchone()
            return result[0]

    #user configurations

    def check_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `user_cfg` WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `user_cfg` (user_id) VALUES (?)", (user_id,))

    def add_ctg(self, user_id, ctg):
        with self.connection:
            return self.cursor.execute("UPDATE `user_cfg` SET ctg = ? WHERE user_id = ?", (ctg, user_id,))

    def add_pos(self, user_id, poss):
        with self.connection:
            return self.cursor.execute("UPDATE `user_cfg` SET poss = ? WHERE user_id = ?", (poss, user_id))

    def get_user_ctg(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT ctg FROM `user_cfg` WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]

    #text

    def check_user_text(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `text` WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user_text(self, user_id, content):
        with self.connection:
            return self.cursor.execute("INSERT INTO `text` (user_id, content) VALUES (?, ?)", (user_id, content))

    def change_user_text(self, user_id, content):
        with self.connection:
            return self.cursor.execute("UPDATE `text` SET content = ? WHERE user_id = ?", (content, user_id,))

    def get_user_text(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT content FROM `text` WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]

    #picture

    def check_user_pict(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `picture` WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user_pict(self, user_id, content):
        with self.connection:
            return self.cursor.execute("INSERT INTO `picture` (user_id, content) VALUES (?, ?)", (user_id, content))

    def change_user_pict(self, user_id, content):
        with self.connection:
            return self.cursor.execute("UPDATE `picture` SET content = ? WHERE user_id = ?", (content, user_id,))

    def get_user_pict(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT content FROM `picture` WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]

    #object

    def get_user_poss(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT poss FROM `user_cfg` WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]

    def get_object(self,category, poss):
        with self.connection:
            result = self.cursor.execute("SELECT link FROM objects WHERE category = ? AND possition = ?", (category, poss,)).fetchone()
            return result[0]

