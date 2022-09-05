import random
import string

import psycopg2
from Config.config import config
from Functions.functions import data_key


class database:
    conn = psycopg2.connect(
        database=config.db_name,
        host=config.db_host,
        user=config.db_user,
        password=config.db_password,
        port=config.db_port,
    )
    cursor = conn.cursor()

    def create_file_table(self, table_name):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name}(
            Index Serial PRIMARY KEY,
            filename VARCHAR(200) NOT NULL,
            FileSize VARCHAR(20000) NOT NULL,
            MessageID INT UNIQUE NOT NULL,
            FileKey VARCHAR(20) UNIQUE NOT NULL,
            UserID VARCHAR(50) NOT NULL,
            Content VARCHAR(50),
            TIME TIMESTAMP NOT NULL);
            """
        )
        self.conn.commit()

    def create_user_table(self, table_name):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name}(
            Index Serial PRIMARY KEY,
            UserName VARCHAR(300) NOT NULL,
            UserID VARCHAR(50) UNIQUE NOT NULL);"""
        )
        self.conn.commit()

    def insert_file_data(
        self,
        filename,
        fileSize,
        MessageID,
        FileKey,
        UserID,
        Content,
        Time,
    ):
        insert = (
            filename,
            fileSize,
            MessageID,
            FileKey,
            UserID,
            Content,
            Time,
        )
        self.cursor.execute(
            f"""INSERT INTO FileData(filename, FileSize, MessageID, FileKey, UserID, CONTENT,TIME)
                            Values (%s, %s, %s, %s, %s, %s, %s);""",
            insert,
        )
        self.conn.commit()

    def display_table_data(self, table_name):
        self.cursor.execute(f"Select * from {table_name}")

    def add_user(self, name):
        key = data_key("DRIVO-", 10)
        data = (name, key)
        self.cursor.execute(
            f"SELECT UserID FROM USERDATA WHERE Username = '{str(name)}';"
        )
        row = self.cursor.fetchone()
        if row:
            return row[0]
        self.cursor.execute(
            f"""INSERT INTO UserData(UserName, UserID)
                            Values (%s, %s)""",
            data,
        )
        return key

    def login_check(self, key):
        self.cursor.execute(
            f"SELECT Username from USERDATA WHERE USERID = '{str(key)}';"
        )
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_uploads(self, key):
        self.cursor.execute(
            f"SELECT FILENAME, CONTENT, Filesize, FileKey from FILEDATA where USERID = '{str(key)}';"
        )
        rows = self.cursor.fetchall()
        final_data = []
        if rows:
            for row in rows:
                data = {
                    "file_name": row[0],
                    "content": row[1],
                    "file_size": row[2],
                    "file_key": row[3],
                }
                final_data.append(data)
            return final_data
        else:
            return []

    def deleteFile(self, file_key, User_id):
        self.cursor.execute(
            f"DELETE from FileData where Filekey = '{str(file_key)}' and UserID = '{str(User_id)}'"
        )
        self.conn.commit()

    def getFile(self, file_key, User_id):
        self.cursor.execute(
            f"SELECT MessageID from FileData where USERID = '{str(User_id)}' and Filekey = '{str(file_key)}'"
        )
        row = self.cursor.fetchone()
        return row[0] if row else None
