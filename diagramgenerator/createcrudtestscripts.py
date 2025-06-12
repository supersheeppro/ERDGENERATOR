import json

class CRUDGenerator:
    def __init__(self, json_path):
        self.json_path = json_path
        self.tables = self._load_tables()
        self.crud_statements = {}

    def _load_tables(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_crud(self):
        for table in self.tables:
            table_name = table["title"]
            fields = table["fields"]

            columns = [f for f in fields if f["type"] != "PK"]
            pk = next((f for f in fields if f["type"] == "PK"), None)

            if not pk:
                print(f"⚠️  Geen primaire sleutel gevonden voor tabel '{table_name}', overslaan...")
                continue

            col_names = [f['name'] for f in columns]
            insert_placeholders = ["%s"] * len(col_names)
            update_assignments = [f"{col} = %s" for col in col_names]

            self.crud_statements[table_name] = {
                "READ": f"SELECT * FROM {table_name} WHERE {pk['name']} = %s;",
                "INSERT": f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({', '.join(insert_placeholders)});",
                "UPDATE": f"UPDATE {table_name} SET {', '.join(update_assignments)} WHERE {pk['name']} = %s;",
                "DELETE": f"DELETE FROM {table_name} WHERE {pk['name']} = %s;"
            }

    def print_crud(self):
        for table, statements in self.crud_statements.items():
            print(f"\n-- {table} CRUD SQL")
            for action, sql in statements.items():
                print(f"-- {action}\n{sql}\n")

    def save_to_file(self, filename="crudtestscripts.sql"):
        with open(filename, "w", encoding="utf-8") as f:
            for table, statements in self.crud_statements.items():
                f.write(f"-- {table} CRUD SQL\n")
                for action, sql in statements.items():
                    f.write(f"-- {action}\n{sql}\n\n")
        print(f"✅ CRUD-scripts opgeslagen in '{filename}'.")

    def get_crud(self):
        return self.crud_statements
