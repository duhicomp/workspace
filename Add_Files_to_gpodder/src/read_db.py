'''
Created on Apr 26, 2015

@author: Duhi
'''
import sqlite3
import ConfigParser 

#TODO: add logging functionality, global through the solution?
class GPODDER_SQLLITE_INTERFACE:
    def __init__(self, db_config_file='../resources/db.cfg',section='Default'):
        self.db_config=ConfigParser.ConfigParser()
        self.db_config.read(db_config_file)
        self.db_file= self.db_config.get(section, 'db_path', 0)
        print("The DB file is:" + self.db_file)
        self.db_connection = sqlite3.connect(self.db_file)
        
    def get_max_eposide_id(self):
        db_cursor = self.db_connection.cursor()
        try:
            print("in the get_max_eposide_id try")
            db_cursor.execute('''SELECT max(id) FROM episode ''')
            data = db_cursor.fetchone()
            self.db_connection.commit()
        except:
            print("couldn't execute the SQL Statement: '''SELECT max(id) FROM episode''' on the database file: "  + db_file)
        finally:
            db_cursor.close()
        return data
    
    def insert_in_db(self):
        db_cursor = self.db_connection.cursor()
        try:
            print("in the insert_in_db try")
            db_cursor.execute('''INSERT INTO episode VALUES (title)''',['Test Title'])
#             db_cursor.execute('''INSERT INTO episode VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',['2','Test Title','Test Description','http://test.url.com','1430756549','http://test.guid.org/story/sex-ducks-and-founding-feud/','http://feeds.wnyc.org/~r/radiolab/~3/Fh9qN_9QWME/', '-1', 'audio/mpeg', '1','1','0','test_filename.mp3','0','0','0','0',''])
            self.db_connection.commit()             
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column 0')
        except sqlite3.InterfaceError:
            print('ERROR: Interface Error')
        except sqlite3.DatabaseError:
            print('ERROR: Database Error')
        except sqlite3.DataError:
            print('ERROR: Data Error')
        except sqlite3.InternalError:
            print('ERROR: Internal Error')
        except sqlite3.NotSupportedError:
            print('ERROR: NotSupported Error')
        finally:
            db_cursor.close()
if __name__ == '__main__':
    try:
        print("In the main try")
        gpodder_db = GPODDER_SQLLITE_INTERFACE('../resources/db.cfg','mysection')
        print("Max eposide ID:" + str(gpodder_db.get_max_eposide_id()))
        gpodder_db.insert_in_db()
    except:
        print("Some Error occured? find out what")