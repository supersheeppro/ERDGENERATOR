import sqlite3

class CRUDExecutor:
    def __init__(self, db_type=None, **kwargs):
        """
        db_type: 'sqlite' (default), 'mysql', or 'postgresql'
        kwargs: connection parameters depending on db_type

        For SQLite (default):
            - db_name (optional, default 'default.db')

        For MySQL:
            - host, user, password, database

        For PostgreSQL:
            - host, user, password, database, port (optional)
        """
        self.db_type = db_type or 'sqlite'

        if self.db_type == 'sqlite':
            db_name = kwargs.get('db_name', 'default.db')
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.placeholder = "?"
        elif self.db_type == 'mysql':
            import mysql.connector
            self.conn = mysql.connector.connect(
                host=kwargs.get('host', 'localhost'),
                user=kwargs['user'],
                password=kwargs['password'],
                database=kwargs['database']
            )
            self.cursor = self.conn.cursor()
            self.placeholder = "%s"
        elif self.db_type == 'postgresql':
            import psycopg2
            self.conn = psycopg2.connect(
                host=kwargs.get('host', 'localhost'),
                user=kwargs['user'],
                password=kwargs['password'],
                dbname=kwargs['database'],
                port=kwargs.get('port', 5432)
            )
            self.cursor = self.conn.cursor()
            self.placeholder = "%s"
        else:
            raise ValueError(f"Unsupported db_type '{self.db_type}'")

    def execute(self, query, params=(), fetch=False):
        """
        Execute a single query with optional parameters.
        """
        try:
            self.cursor.execute(query, params)
            if fetch:
                return self.cursor.fetchall()
            else:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error executing query: {e}")
            raise e

    def close(self):
        self.cursor.close()
        self.conn.close()

    def format_query(self, query_template):
        """
        Optional helper to replace all %s with the correct placeholder for SQLite.
        Use this if queries are defined with %s but target SQLite.
        """
        if self.db_type == 'sqlite':
            return query_template.replace("%s", "?")
        return query_template

if __name__ == "__main__":
    executor = CRUDExecutor(
        db_type='mysql',
        host='localhost',
        user='root',
        password='D@vi7596',
        database='minecraft'
    )

    # READ example
    read_query = "SELECT * FROM Speler WHERE SpelerID = %s;"
    result = executor.execute(read_query, (1,), fetch=True)
    print("READ result:", result)

    read_all_query = "SELECT * FROM Speler;"
    result = executor.execute(read_all_query, fetch=True)
    print("Alle spelers:", result)


    # INSERT example
    insert_query = """
    INSERT INTO Speler (Gebruikersnaam, UUID, EersteLogin, LaatsteLogin, IsBanned, Ervaring, Level, Health, Mana)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    insert_values = ("Nieu3ddweSqwweprgeler", "uuid-123wee3545434", "2025-06-12 10:00:00", None, False, 0, 1, 100.0, 100.0)
    executor.execute(insert_query, insert_values)

    # UPDATE example
    #update_query = """
    #UPDATE Speler
    #SET Gebruikersnaam = %s,
    #    UUID = %s,
    #    EersteLogin = %s,
    #    LaatsteLogin = %s,
    #    IsBanned = %s,
    #    Ervaring = %s,
    #    Level = %s,
    #    Health = %s,
    #    Mana = %s
    #WHERE SpelerID = %s;
    #"""
    #update_values = ("GewijzigdeNaam", "uuid-5678", "2025-06-11 09:00:00", None, False, 100, 2, 90.0, 80.0, 1)
    #executor.execute(update_query, update_values)

    # DELETE example
    #delete_query = "DELETE FROM Speler WHERE SpelerID = %s;"
    #executor.execute(delete_query, (1,))

    executor.close()

