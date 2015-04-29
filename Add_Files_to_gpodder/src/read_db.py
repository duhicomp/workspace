'''
Created on Apr 26, 2015

@author: Duhi
'''
import sqlite3
import ConfigParser 



if __name__ == '__main__':
    db_config_file='../resources/db.cfg'
    db_config=ConfigParser.ConfigParser()
    db_config.read(db_config_file)
    
    print db_config.get('mysection', 'db_path', 0)
    try:
        db_file= db_config.get('mysection', 'db_path', 0)
    except:
        db_file = db_config.get('Default', 'db_path', 0)
    
    db_connection = sqlite3.connect(db_file)
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute('''SELECT id FROM episode ''')
        db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = db_cursor.fetchall()
        print("List of tables in:' "  + db_file + "' : "+ str(data))
        db_cursor.execute('''SELECT max(id) FROM episode ''')
        data = db_cursor.fetchone()
        print("max_id in eposide table is :%s "  %data)
    except:
        print("couldn't execute the SQL Statement: '''SELECT max(id) FROM episode''' on the database file: "  + db_file)
    finally:
        db_cursor.close
    