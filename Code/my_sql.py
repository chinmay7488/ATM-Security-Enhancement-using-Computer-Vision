import sqlite3
import os
from sqlite3 import Error
from datetime import datetime

class my_sql():
    
    def __init__(self):
        if(not os.path.exists("ATMLog.db")):
            try:
                connection = sqlite3.connect("ATMLog.db")
                tableCursor = connection.cursor()
                table = "CREATE TABLE atm_machine(Person_Photo BLOB NOT NULL, Date DATETIME NOT NULL, Entry_Time DATETIME NOT NULL);"
                tableCursor.execute(table)
            except sqlite3.Error as e:
                print(e)
            finally:
                if connection:
                    connection.close()

    def Insert_data(self, filename, entry_time):
        try:
            date=None
            tableCursor=None
            connection = sqlite3.connect("ATMLog.db")
            tableCursor=connection.cursor()
            today=datetime.now()
            date= str(today.year)+"-"+str(today.month)+"-"+str(today.day)

            with open(filename, "rb") as file:
                photo = file.read()
            SqlStatement="INSERT INTO atm_machine VALUES(?, ?, ?)"
            tableCursor.execute(SqlStatement, (photo, date, entry_time))
            connection.commit()
        except Exception as ex:
            print(ex)
        finally:
                if connection:
                    connection.close()
