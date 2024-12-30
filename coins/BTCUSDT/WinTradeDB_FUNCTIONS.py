import sqlite3


def CerateTable():
    try:
        sqliteConnection = sqlite3.connect('WinTrade.db')
        sqlite_create_table_query = '''CREATE TABLE TradeHistory (
                                    id INTEGER PRIMARY KEY,
                                    lasttradestat REAL NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")    
        
      
        
            
def InsertTable():
    try:
        sqliteConnection = sqlite3.connect('WinTrade.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO TradeHistory
                              (id, lasttradestat) 
                               VALUES 
                              (1, 9500)"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into TradeHistory table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
   
        
        
import sqlite3

def ReadLastTradeMove():
    
    
    global lasttradestat
    try:
        sqliteConnection = sqlite3.connect('WinTrade.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from TradeHistory"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("lasttradestat: ", row[1])
            print("\n")
        lasttradestat = (row[1])

   

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            
import sqlite3


def UpdateLastTradeMove(lasttradestat, id):
    try:
        sqliteConnection = sqlite3.connect('WinTrade.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_update_query = """Update TradeHistory set lasttradestat = ?, id = ?"""
        columnValues = (lasttradestat, id)
        cursor.execute(sqlite_update_query, columnValues)
        sqliteConnection.commit()
        print("Multiple columns updated successfully")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update multiple columns of sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")




            
   
        
