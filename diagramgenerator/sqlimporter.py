import sqlite3
import os


class SQLImporter:
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
        elif self.db_type == 'mysql':
            import mysql.connector
            self.conn = mysql.connector.connect(
                host=kwargs.get('host', 'localhost'),
                user=kwargs['user'],
                password=kwargs['password']
            )
            self.cursor = self.conn.cursor()
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
        else:
            raise ValueError(f"Unsupported db_type '{self.db_type}'")

    def import_sql_file(self, filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"SQL file '{filepath}' not found.")

        with open(filepath, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Split statements on ';' - let op, dit is simpel en werkt niet als ; in strings voorkomt
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

        try:
            for stmt in statements:
                # Filter SQLite incompatible statements
                if self.db_type == 'sqlite':
                    stmt_upper = stmt.upper()
                    if (stmt_upper.startswith('DROP DATABASE') or
                        stmt_upper.startswith('CREATE DATABASE') or
                        stmt_upper.startswith('USE ')):
                        print(f"Skipping incompatible statement for SQLite: {stmt[:40]}...")
                        continue

                self.cursor.execute(stmt)
            self.conn.commit()
            print(f"Successfully imported '{filepath}' into {self.db_type} database.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error executing SQL script: {e}")
            raise e

    def close(self):
        self.cursor.close()
        self.conn.close()
