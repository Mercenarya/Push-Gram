import sqlite3
import os



current = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current,"telegram-trans.db")
DB = sqlite3.connect("telegram-trans.db",check_same_thread=False)
cursor = DB.cursor()

print(db_path)


def Note():
    setNote = '''
        CREATE TABLE note (
            title VARCHAR(900) PRIMARY KEY,
            textiled TEXT
        )
    '''
    return setNote

def Languages():
    setLangs = '''
        CREATE TABLE langs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lans VARCHAR(700)
        )
    '''
    return setLangs
def Word():
    Setword = '''
        CREATE TABLE word (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            trans TEXT
        )
    '''
    return Setword
try:
    if sqlite3.Connection:
        
        language = [0," "," "]


        print("Connection set up")
        cursor.execute('''
            INSERT INTO word (id,items,trans) VALUES (?,?,?)
        ''',language)
        # cursor.execute(Word())
        # cursor.execute("DROP TABLE Word")
        # for obj in cursor.fetchall():
        #     print(obj[0],"-",obj[1])
        DB.commit()
    elif sqlite3.Error:
        print("DB Error")
except sqlite3.Error as error:
    print(error)