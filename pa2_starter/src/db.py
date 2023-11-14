import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the User app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """Secure a connection with the database and stores it into the instance 'conn'
        """

        self.conn = sqlite3.connect("venmo.db", check_same_thread=False) 
        self.create_task_table()

    def create_task_table(self):
        """
        Using SQL, create user table with 4 fields: id, name, username, and balance! 
        """
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INT NOT NULL
        );
        """)
        

    def delete_user_table(self):
        """
        Using SQL, delete the user table
        """
        self.conn.execute("DROP TABLE IF EXISTS user;")

    def get_all_users(self):
        """
        Using SQL, return all the users in the user table.
        """
        cursor = self.conn.execute("SELECT * FROM user;") 
        users = []
        for row in cursor :
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users


    def get_user_by_id(self, id):
        """
        Using SQL, gets a user by its id
        """

        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?;", (id,)) 
        for row in cursor :
            return ({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})

    def insert_user_table(self, name, username, balance = 0):
        """
        Using SQL, inserts a user into the task table. The default value for a user's balance, 
        if it's not provided, is 0! 
        """
        cursor = self.conn.execute("INSERT INTO user(name, username, balance) VALUES (?,?,?);", (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid
    

    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a user from a table
        """
        self.conn.execute("DELETE FROM user WHERE id = ?;", (id,))
        self.conn.commit()

    def update_user(self, user_id, balance):
        """
        Using SQL, updates user's balance field from a table 
        """
        self.conn.execute("""
        UPDATE user SET balance =? WHERE id=?;
        """, (balance, user_id))
        self.conn.commit()
    
        


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
