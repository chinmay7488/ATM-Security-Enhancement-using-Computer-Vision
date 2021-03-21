import mysql.connector as mysql
from datetime import datetime

class my_sql():
    
    def __init__(self, filename, entry_time):
        date=None
        mycursor=None
        # Connecting Mysql server 
        mydb = mysql.connect(
                host="localhost",
                user="root",
                password="1234",
                database="minor_project"
                )
        if(mydb):
            print("Connection Successfull")
        else:
            print("Connection Failed")
        # accessing MySQL Cursor
        mycursor=mydb.cursor()
        # Fetching current date and time
        today=datetime.now()
        # converting date to date from date and time
        date= str(today.year)+"-"+str(today.month)+"-"+str(today.day)

        # opening image as binary and reading it
        with open(filename, "rb") as file:
             photo = file.read()
        # Mysql command to insert value and executing it
        SqlStatement="INSERT INTO atm_machine(photo, date, entry_time) VALUES (%s,%s,%s)"
        mycursor.execute(SqlStatement, (photo, date, entry_time))
        # Commiting changes
        mydb.commit()

