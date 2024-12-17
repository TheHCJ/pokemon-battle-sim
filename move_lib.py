import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your password!",
    database="pokemon_database"
)

mycursor = mydb.cursor()


# TODO: add secondary effects!

class Move:
    def __init__(self, name, move_type, category, power, accuracy, pp):
        self.name = name
        self.move_type = move_type.lower()
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.pp = pp


def retrieve_move(name):
    mycursor.execute("SELECT name, type, category, power, accuracy, pp FROM pokemon_database.movepool WHERE name = %s",
                     (name,))

    result = mycursor.fetchall()[0]

    created_move = Move(result[0], result[1], result[2], result[3], result[4], result[5])

    return created_move
