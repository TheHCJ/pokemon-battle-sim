import mysql.connector
from move_pool_info_scraper import movedex

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR PASSWORD!!!",
    database="pokemon_database"
)

mycursor = mydb.cursor()

# STEP 1: RUN THIS CODE UNCOMMENTED FIRST TO CREATE THE TABLE, THEN COMMENT IT AFTER RUNNING IT ONCE!
mycursor.execute("""CREATE TABLE movepool (
name VARCHAR(50),
type VARCHAR(20),
category VARCHAR(50),
power INT,
accuracy INT,
pp INT,
effect VARCHAR(255),
probability INT)""")

# STEP 2: UNCOMMENT THE NEXT 3 LINES OF CODE AFTER DOING STEP 1 AND RUN THE FILE AGAIN
# sql = "INSERT movepool (name, type, category, power, accuracy, pp, effect, probability) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# 
# mycursor.executemany(sql, movedex)

mydb.commit()
