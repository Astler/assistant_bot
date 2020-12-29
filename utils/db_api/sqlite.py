import sqlite3


class Database:
    def __init__(self, pathToDB="main.db"):
        self.path_to_db = pathToDB

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = (), fetchone=False, fetchall=False, commit=False):
        connection = self.connection

        connection.set_trace_callback(logger)

        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = ""

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_ideas(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Ideas_Table (
	        id integer,
	        idea_text text NOT NULL,
	        idea_status integer,
	        idea_date integer,
	        idea_author text,
	        idea_author_id integer,
	        PRIMARY KEY("id" AUTOINCREMENT)
            );"""

        self.execute(sql, commit=True)

    def add_idea(self, text: str, author_name: str):
        sql = "INSERT INTO Ideas_Table(idea_text, idea_status, idea_author) VALUES(?, ?, ?)"
        parameters = (text, 0, author_name)
        self.execute(sql, parameters=parameters, commit=True)

    def all_ideas(self):
        sql = "SELECT * FROM Ideas_Table"
        return self.execute(sql, fetchall=True)

    def count_ideas(self):
        return self.execute("SELECT COUNT(*) FROM Ideas_Table;", fetchone=True)


def logger(statement):
    print(f"""
    -------------------------------------
    Exe {statement}
    """)
