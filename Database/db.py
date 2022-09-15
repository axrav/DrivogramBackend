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

    async def create_file_table(self, table_name):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name}(
            Index Serial PRIMARY KEY,
            filename VARCHAR(200) NOT NULL,
            FileSize VARCHAR(300) NOT NULL,
            MessageID INT UNIQUE NOT NULL,
            FileKey VARCHAR(20) UNIQUE NOT NULL,
            UserID VARCHAR(50) NOT NULL,
            Content VARCHAR(50),
            TIME TIMESTAMP NOT NULL);
            """
        )
        self.conn.commit()

    async def create_user_table(self, table_name):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name}(
            Index Serial PRIMARY KEY,
            UserName VARCHAR(300) NOT NULL,
            UserID VARCHAR(50) UNIQUE NOT NULL);"""
        )
        self.conn.commit()

    async def insert_file_data(
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
            """INSERT INTO FileData(filename, FileSize, MessageID, FileKey, UserID, CONTENT,TIME)
                            Values (%s, %s, %s, %s, %s, %s, %s);""",
            insert,
        )
        self.conn.commit()

    async def display_table_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")

    async def add_user(self, name):
        key = data_key("DRIVO-", 10)
        data = (name, key)
        self.cursor.execute(
            """INSERT INTO UserData(UserName, UserID)
                            Values (%s, %s)""",
            data,
        )
        self.conn.commit()
        return key

    async def login_check(self, key):
        self.cursor.execute(
            """SELECT Username from Userdata WHERE USERID = %s;""",
            (key,),
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    async def get_uploads(self, key):
        self.cursor.execute(
            """SELECT filename, content, Filesize, FileKey FROM filedata WHERE USERID = %s;""",
            (key,),
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

    async def deleteFile(self, file_key, User_id):
        self.cursor.execute(
            """SELECT Filename FROM FileData WHERE Filekey = %s and UserID = %s""",
            (
                file_key,
                User_id,
            ),
        )
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute(
                """DELETE FROM FileData WHERE Filekey = %s and UserID = %s""",
                (
                    file_key,
                    User_id,
                ),
            )
            self.conn.commit()
            return row[0]

    async def getFile(self, file_key, User_id):
        self.cursor.execute(
            """SELECT MessageID FROM FileData WHERE USERID = %s and Filekey = %s;""",
            (User_id, file_key),
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    async def create_share_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS sharedata(
            Index Serial PRIMARY KEY,
            Token VARCHAR(50000) UNIQUE NOT NULL,
            Shorten VARCHAR(500) UNIQUE NOT NULL,
            userid VARCHAR(500) NOT NULL,
            time INT NOT NULL);
            """
        )

    async def share_data_add(self, short, token, userid, time):
        insert = (token, short, userid, time)
        self.cursor.execute(
            """INSERT INTO sharedata(token,shorten,userid,time)
        Values(%s,%s,%s,%s)""",
            insert,
        )
        self.conn.commit()

    async def share_data_search(self, shorten):
        self.cursor.execute(
            """SELECT token,time FROM sharedata WHERE Shorten = %s;""",
            (shorten,),
        )
        row = self.cursor.fetchone()
        return row[0], row[1] if row else None
