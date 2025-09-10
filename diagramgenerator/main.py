from createsql import SQLGenerator
from compiler import DrawioERDGenerator
from sqlimporter import SQLImporter
from createcrudtestscripts import CRUDGenerator

if __name__ == "__main__":
    sqlgenerator = SQLGenerator(json_file="data/tables.json", output_file="output.sql", db_name="minecraft")
    sqlgenerator.run()
    erdgenerator = DrawioERDGenerator(json_file="data/tables.json", output_file="output.drawio")
    erdgenerator.run()
    generator = CRUDGenerator(json_path="data/tables.json")
    generator.generate_crud()
    generator.save_to_file()
    #importer = SQLImporter()  # Maakt 'default.db' aan in de huidige map
    #importer.import_sql_file('output.sql')
    #importer.close()
    #mysql:
    importer = SQLImporter(
        db_type='mysql',
        host='localhost',
        user='root',
        password='D@vi7596',
    )
    importer.import_sql_file('output.sql')
    importer.close()
    #postgres:
    #importer = SQLImporter(
    #    db_type='postgresql',
    #    host='localhost',
    #    user='postgres',
    #    password='wachtwoord',
    #    database='WebshopDB'
    #)
    #importer.import_sql_file('output.sql')
    #importer.close()

