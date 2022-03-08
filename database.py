import sqlite3

con = sqlite3.connect("bot.db", check_same_thread=False)
c = con.cursor()

def create_table():
    query = '''CREATE TABLE IF NOT EXISTS Members
                (Name TEXT,
                Last_name TEXT,
                User_name TEXT,
                Chat_id TEXT,
                User_id TEXT,
                Time_joined TEXT);'''

    c.execute(query)

    query2 = '''CREATE TABLE IF NOT EXISTS Blocked
            (Chat_id INTEGER);'''
    
    c.execute(query2)

    query3 = '''CREATE TABLE IF NOT EXISTS Prefix
                (Prefix TEXT,
                Type TEXT,
                File_id TEXT,
                Caption TEXT);'''

    c.execute(query3)

    con.commit()
    con.close()

if 4 == 4:
    create_table()