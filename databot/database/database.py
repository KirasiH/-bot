import sqlite3 as sql


class DataBase:

    def __init__(self):
        self.db = sql.connect("databot/database.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INT PRIMARY KEY,
            user_name TEXT,
            name TEXT,
            phone_number TEXT,
            status_admin TINYINT(1),
            status_block TINYINT(1)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS groups(
            group_id INT PRIMARY KEY,
            name text
        )""")
        self.db.commit()

    def check_user(self, user_id):
        if self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchall() == []:
            return False
        return True

    def add_user(self, user_id, name, phone_number, status_admin, status_block):
        self.cursor.execute("INSERT INTO users(user_id, name, phone_number, status_admin, status_block) VALUES (?, ?, ?, ?, ?)", (user_id, name, phone_number, status_admin, status_block))
        self.db.commit()

    def delete_user(self, user_id):
        self.cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        self.db.commit()

    def user_new_name(self, user_id, name):
        self.cursor.execute(f"UPDATE users SET name = '{name}' WHERE user_id = {user_id}")
        self.db.commit()

    def user_new_phone(self, user_id, phone):
        self.cursor.execute(f"UPDATE users SET phone_number = '{phone}' WHERE user_id = {user_id}")
        self.db.commit()

    def user_name(self, user_id):
        return str(self.cursor.execute(f"SELECT name FROM users WHERE user_id = {user_id}").fetchall()[0][0])


    def user_phone(self, user_id):
        return str(self.cursor.execute(f"SELECT phone_number FROM users WHERE user_id = {user_id}").fetchall()[0][0])

    def groups(self):
        data = self.cursor.execute(f"SELECT group_id, name FROM groups").fetchall()
        return data

    def delete_group(self, group_id):
        self.cursor.execute(f"DELETE FROM groups WHERE group_id = {group_id}")
        self.db.commit()

    def add_group(self, group_id, name):
        self.cursor.execute("INSERT INTO groups(group_id, name) VALUES (?, ?)", (group_id, name))
        self.db.commit()

    def user_new_status_block(self, user_id, status):
        self.cursor.execute(f"UPDATE users SET status_block = {status} WHERE user_id = {user_id}")
        self.db.commit()

    def list_users(self, ban=False):
        if ban:
            data = self.cursor.execute("SELECT user_id FROM users WHERE status_block = 1").fetchall()
        else:
            data = self.cursor.execute("SELECT user_id FROM users WHERE status_block = 0").fetchall()

        for i in data:
            print(i[0])
            yield i[0]

    def list_admin(self):
        data = self.cursor.execute(f"SELECT user_id FROM users WHERE status_admin = 1").fetchall()
        return data

    def user_info(self, user_id):
        data = self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchall()
        if data == []:
            return None
        else:
            return data[0]


database = DataBase()
#
# class DataBase:
#
#     async def connection(self, loop):
#         conn = await aiomysql.connect(port=3306,
#                                       host="127.0.0.1",
#                                       db="Bot001",
#                                       user="root",
#                                       password="123456789-zalik",
#                                       loop=loop
#         )
#
#         return conn
#
#     async def create_database(self):
#
#         loop = asyncio.get_event_loop()
#
#         self.conn = await self.connection(loop)
#
#         async with self.conn.cursor() as cur:
#             cur.execute("""CREATE TABLE IF NOT EXISTS users(
#                 user_id INT PRIMARY KEY,
#                 user_name TEXT,
#                 name TEXT,
#                 phone_number TEXT,
#                 status_admin TINYINT(1),
#                 status_block TINYINT(1)
#             )""")
#
#             cur.execute("""CREATE TABLE IF NOT EXISTS groups(
#                 group_id INT PRIMARY KEY,
#                 name ENUM('request', 'suggestion', 'admin')
#             )""")
#
#
#     async def check_user(self, user_id):
#
#         async with self.conn.cursor() as cur:
#             if cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchall() == []:
#                 return False
#
#             return True
#
#     async def add_user(self, user_id, name, phone_number, status_admin, status_block):
#
#         async with self.conn.cursor() as cur:
#             cur.execute("INSERT INTO users(user_id, name, phone_number, status_admin, status_block) VALUES (?, ?, ?, ?, ?)", (user_id, name, phone_number, status_admin, status_block))
#
#     async def delete_user(self, user_id):
#
#         async with self.conn.cursor() as cur:
#             cur.execute(f"DELETE FROM users WHERE user_id = {user_id}")
#
#     async def user_new_name(self, user_id, name):
#
#         async with self.conn.cursor() as cur:
#             cur.execute(f"UPDATE users SET name = '{name}' WHERE user_id = {user_id}")
#
#     async def user_new_phone(self, user_id, phone):
#
#         async with self.conn.cursor() as cur:
#             cur.execute(f"UPDATE users SET phone_number = '{phone}' WHERE user_id = {user_id}")
#
#     async def user_name(self, user_id):
#
#         async with self.conn.cursor() as cur:
#             return str(cur.execute(f"SELECT name FROM users WHERE user_id = {user_id}").fetchall()[0][0])
#
#     async def user_phone(self, user_id):
#
#         async with self.conn.cursor() as cur:
#             return str(cur.execute(f"SELECT phone_number FROM users WHERE user_id = {user_id}").fetchall()[0][0])
#
#     async def groups(self):
#
#         async with self.conn.cursor() as cur:
#             data = cur.execute(f"SELECT group_id, name FROM groups").fetchall()
#             return data
#
#     async def delete_group(self, group_id):
#
#         async with self.conn.cursor() as cur:
#             cur.execute(f"DELETE FROM groups WHERE group_id = {group_id}")
#
#     async def add_group(self, group_id, name):
#
#         async with self.conn.cursor() as cur:
#             cur.execute("INSERT INTO groups(group_id, name) VALUES (?, ?)", (group_id, name))
#
#     async def user_new_status_block(self, user_id, status):
#
#         async with self.conn.cursor() as cur:
#             cur.execute(f"UPDATE users SET status_block = {status} WHERE user_id = {user_id}")
#
#     async def list_users(self, ban=False):
#
#         async with self.conn.cursor() as cur:
#             if ban:
#                 data = await cur.execute("SELECT user_id FROM users WHERE status_block = 1")
#
#             else:
#                 data = await cur.execute("SELECT user_id FROM users WHERE status_block = 0")
#             print(data)
#
#             ban_list = []
#             for i in data:
#                 ban_list.append(i[0])
#
#             return ban_list
#
#     async def list_admin(self):
#
#         async with self.conn.cursor() as cur:
#             data = cur.execute(f"SELECT user_id FROM users WHERE status_admin = 1").fetchall()
#             return data
#
#     async def user_info(self, user_id):
#
#         async with self.conn.cursor() as cur:
#             data = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchall()
#
#             if data == []:
#                 return None
#
#             else:
#                 return data[0]
#
# database = DataBase()
#
#

