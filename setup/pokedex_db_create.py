import mysql.connector
from pokemon_database_scraper import pokedex, abilities_dex
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR PASSWORD!",
    database="pokemon_database"
)

mycursor = mydb.cursor()


def step_1():
    mycursor.execute("""
    CREATE TABLE pokedex (
        num INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        type1 VARCHAR(10),
        type2 VARCHAR(10),
        bst INT,
        hp INT,
        atk INT,
        def INT,
        spa INT,
        spd INT,
        speed INT,
        height DOUBLE,
        weight DOUBLE,
        ability1 VARCHAR(50),
        ability2 VARCHAR(50),
        hiddenAbility VARCHAR(50)
    )
    """)


def step_2():
    sql = "INSERT pokedex (name, type1, type2, bst, hp, atk, def, spa, spd, speed, height, weight, ability1, ability2, hiddenAbility) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    mycursor.executemany(sql, pokedex)
    
    mydb.commit()


step_1()
step_2()

for generation in abilities_dex:
    dex = generation.find_all("tr")[1:]
    for mon in dex:
        tds = mon.find_all("td")
        name = tds[2].find("a").text
        smaller_name = "" if tds[2].find("small").text == " " else tds[2].find("small").text
        spacer = "" if tds[2].find("small").text == "" else " "
        full_name = name + spacer + smaller_name
        ability_1 = tds[3].find("a").text
        ability_2 = None if tds[4].find("a") is None else tds[4].find(
            "a").text  # None if type(tds[4].find("a")) is None else tds[4].find("a").text
        ability_3 = None if tds[5].find("a") is None else tds[5].find(
            "a").text  # None if type(tds[5].find("a")) is None else tds[4].find("a").text

        mycursor.execute("UPDATE pokedex SET ability1 = %s, ability2 = %s, hiddenAbility = %s WHERE name = %s",
                         (ability_1, ability_2, ability_3, full_name))

        mydb.commit()
