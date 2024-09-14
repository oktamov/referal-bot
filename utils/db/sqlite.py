import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
   CREATE TABLE IF NOT EXISTS Users (
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
"""
        self.execute(sql, commit=True)

    def create_table_users_invite_count(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS UserInviteCount (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            current_count INTEGER,
            history_count INTEGER,
            FOREIGN KEY (user_id) REFERENCES Users (id))
        '''
        self.execute(sql, commit=True)

    def create_table_user_invite_members(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS UserInviteMember (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            inveted_user_id INTEGER
            )
'''
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, full_name: str, username: str, telegram_id: int):

        sql = """
        INSERT INTO Users(full_name, username, telegram_id) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(full_name, username, telegram_id), commit=True)

    def add_user_invite_count(self, user_id: int, current_count: int, history_count: int):
        sql = """
            INSERT INTO UserInviteCount(user_id, current_count, history_count) VALUES (?,?,?)
        """
        self.execute(sql, parameters=(user_id, current_count, history_count), commit=True)

    def add_user_invite_member(self, user_id: int, invited_user_id: int):
        sql = """
            INSERT INTO UserInviteMember(user_id, inveted_user_id) VALUES (?,?)
        """
        self.execute(sql, parameters=(user_id, invited_user_id), commit=True)

    def select_invited_members(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM UserInviteMember WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def get_user_invited_count(self, user_id: int):
        sql = f"""
            SELECT current_count FROM UserInviteCount WHERE user_id={user_id}
        """
        return self.execute(sql, fetchone=True)

    def update_invite_current_history_count_plus_1(self, user_id: int):
        sql = f"""
            UPDATE UserInviteCount
            SET current_count = current_count + 1, history_count = history_count + 1
            WHERE user_id = {user_id}
        """
        return self.execute(sql, commit=True)

    def update_invite_current_count_set_0(self, user_id: int):
        sql = f"""
                    UPDATE UserInviteCount
                    SET current_count = 0
                    WHERE user_id = {user_id}
                """
        return self.execute(sql, commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
