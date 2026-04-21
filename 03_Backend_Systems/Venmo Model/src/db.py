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
        self.create_user_table()
        self.create_interactions_table()

    def create_user_table(self):
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
    
####------------Transactions --------------####

    def create_interactions_table(self):
        """
        Using SQL, create a transactions table that 
        also references the user table
        """
        try:
            self.conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS interactions(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        sender_id INTEGER NOT NULL,
                        receiver_id INTEGER NOT NULL, 
                        amount INTEGER NOT NULL,
                        message TEXT,
                        accepted INTEGER,
                        FOREIGN KEY (sender_id) REFERENCES user(id),
                        FOREIGN KEY (receiver_id) REFERENCES user(id)
                    )
                """

            )
        except Exception as e:
            print(e)

    def delete_interactions_table(self):
        """
        Using SQL, delete the interactions table
        """

        self.conn.execute("DROP TABLE IF EXISTS interactions")


    def insert_interaction(self, timestamp, sender_id, receiver_id, amount, message, accepted):
        """
        Using SQL, add a new interaction into the interactions table 
        """

        cursor = self.conn.execute("INSERT INTO interactions (timestamp, sender_id, receiver_id, amount, message, accepted) VALUES (?, ?, ?, ?, ?, ?);",
        (timestamp, sender_id, receiver_id, amount, message, accepted))
        self.conn.commit()
        return cursor.lastrowid

    def get_interactions_of_user(self, user_id):
        """
        Using SQL, get all the interactions for given a user id
        """
        cursor = self.conn.execute("SELECT * FROM interactions WHERE sender_id = ? OR receiver_id=?", (user_id,user_id))
        interactions = []
        for row in cursor:
            if row[6] == None:
                interactions.append({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "message": row[5], "accepted": None})
            else:
                interactions.append({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "message": row[5], "accepted": bool(row[6])})
        return interactions

    
    def get_all_interactions(self):
        """
        Using SQL, get all interactions

        """
        cursor = self.conn.execute("SELECT * FROM interactions")
        interactions = []
        for row in cursor:
            if row[6] == None:
                interactions.append({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "message": row[5], "accepted": None})
            else:
                interactions.append({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "message": row[5], "accepted": bool(row[6])})
        return interactions

    def get_interaction_by_id(self, id):
        """
        Using SQL, get the interactions for given id
        """
        cursor = self.conn.execute("SELECT * FROM interactions WHERE id = ?;", (id,))
        
        for row in cursor:
            if row[6] == None:
                return ({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "message": row[5], "accepted": None})
            else:
                return ({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "message": row[5], "accepted": bool(row[6])})
        return None

    def update_interaction(self,timestamp, id, accepted): 
        """
        Using SQL, updates interaction's accepted field from interactions table 
        """
        self.conn.execute("""
        UPDATE interactions SET timestamp=?, accepted =? WHERE id=?;
        """, (timestamp, accepted, id))
        self.conn.commit()

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
