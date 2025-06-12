import json

class SQLGenerator:
    def __init__(self, json_file, output_file="output.sql", db_name="WebshopDB"):
        self.json_file = json_file
        self.output_file = output_file
        self.db_name = db_name
        self.data = []
        self.created_tables = set()

    def load_json(self):
        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def generate_sql_field(self, field):
        line = f"{field['name']} {field['datatype']}"
        # Voor PK met auto_increment toevoegen
        if field.get("type") == "PK" and field.get("auto_increment", False):
            line += " AUTO_INCREMENT"
        if field.get("not_null"):
            line += " NOT NULL"
        if field.get("unique") and field.get("type") != "PK":
            line += " UNIQUE"
        return line

    def convert_table_to_sql(self, table):
        lines = []
        constraints = []

        for field in table["fields"]:
            if field["type"] == "PK":
                lines.append(self.generate_sql_field(field))
                constraints.append(f"PRIMARY KEY ({field['name']})")
            elif field["type"] == "FK":
                lines.append(self.generate_sql_field(field))
                ref = field.get("references", {})
                ref_table = ref.get("table")
                ref_field = ref.get("field")
                if ref_table in self.created_tables:
                    constraints.append(f"FOREIGN KEY ({field['name']}) REFERENCES {ref_table}({ref_field})")
                else:
                    return None  # FK refereert naar niet-bestaande table
            else:
                lines.append(self.generate_sql_field(field))

        full_definition = lines + constraints
        return f"CREATE TABLE {table['title']} (\n  " + ",\n  ".join(full_definition) + "\n);"

    def generate_full_sql(self):
        sql_lines = [
            f"DROP DATABASE IF EXISTS {self.db_name};",
            f"CREATE DATABASE {self.db_name};",
            f"USE {self.db_name};\n"
        ]

        remaining_tables = self.data[:]
        max_attempts = len(remaining_tables)

        while remaining_tables and max_attempts > 0:
            progress = False
            for table in remaining_tables[:]:
                sql = self.convert_table_to_sql(table)
                if sql:
                    sql_lines.append(sql)
                    sql_lines.append("")
                    self.created_tables.add(table['title'])
                    remaining_tables.remove(table)
                    progress = True
            if not progress:
                break
            max_attempts -= 1

        if remaining_tables:
            sql_lines.append("-- Tabellen die niet konden worden aangemaakt vanwege ongeldige FK-verwijzingen:")
            for table in remaining_tables:
                sql_lines.append(f"-- {table['title']}")

        return "\n".join(sql_lines)

    def save_sql_to_file(self, sql_code):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(sql_code)
        print(f"✅ SQL-script succesvol opgeslagen als: {self.output_file}")

    def run(self):
        try:
            self.load_json()
            sql_script = self.generate_full_sql()
            self.save_sql_to_file(sql_script)
        except FileNotFoundError:
            print(f"⚠ Bestand '{self.json_file}' niet gevonden.")
        except json.JSONDecodeError as e:
            print(f"⚠ JSON fout: {e}")
