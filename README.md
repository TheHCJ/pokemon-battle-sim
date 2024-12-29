# UPDATE 1.0: (a very very very) Alpha release
Yayy finally, after a couple of months I am ready to release the code I have written so far 🥳🥳

> [!NOTE]
> I have not been coding that much on this project, and I do have aspirations to pick it up again. You will see more updates in the future.

## Features
- damage calculators (Henceforth IV, EV, stats calculator)
- **ALL** forms (megas, g-max†, regional forms, legendary forms e.g. deoxys)
- complete pokedex as mentioned with the addition above ^^
- complete movepool with z-moves, g-max moves etc.
- weather effects
- status conditions
- basic turn functionality
- speed stacks (I didn't actually use a stack, I was going to but I also needed to swap a lot of values so it would've been ineffective)
- basic double battle availability

## User Experience
This is just going to be a quick guide on how to use the current functions.
first off we have the pokemon class, and the following attributes.
```python3 
class Pokemon:
    def __init__(self, name, level, type1, type2, ability1, ability2, hidden_ability, nature, ev, iv, base_stats,
                 moveset=None, held_item=None, gender="Male")
```
As demonstrated by the code below, this is how you would create a new pokemon:
```python3
articuno = Pokemon("Articuno", 100, pk_types.ice, pk_types.flying, "Pressure", None,
                   "Snow Cloak", natures.adamant, [0, 0, 0, 0, 0, 0], [31, 31, 31, 31, 31, 31],
                   [90, 85, 100, 95, 125, 85])
```
In this scenario, we have created an articuno with these following stats (courtesy to [pokemon database](https://pokemondb.net) for parts of these images):

![image](https://github.com/user-attachments/assets/35c2bdf3-1398-4aed-94d0-66d04bb1175c)

In order to **add moves**, you should use this following function. This adds Ice Beam, Blizzard, Agility and Protect to Articuno's moveset:
```python3
articuno.add_moves("Ice Beam", "Blizzard", "Agility", "Protect")
```

Finally, in order to keep things basic, this is how to use a move:
```python3
result = mon.use_move(selected_move, target_mon, weather)
```
The reason it is stored to a variable and not just called is because it returns 'codes' which mean certain things about the outcome of that move:
### Move outcome results
- -2 = the move missed
- -3 = the target is immune to the move
- -4 = the user is paralyzed
- 0 = the move was successful <br>
(all of these can be found in the use_move() function in `pokemon_class.py`!

## How to set up the database!! (VERY IMPORTANT)
Originally, this project was meant for me to be able to use databases and more importantly mysql in python. However I have not made a 'public database' as I don't want to spend money on this. now, "Why can't you just create a massive list with all the moves and pokemon?", well truthfully, I dont really know. I wanted to get a grip on sql and also a python file with 1000+ lines of pokemon and info is a tedious process to scrape and filter through.
### Creating the database
#### Required libraries
- mysql
- requests
- beautifulsoup

Make sure you have mysql database or something similar installed to create a local database. There are plenty of guides on the internet to connect to the local database via the mysql library. Open the `\setup` folder and then for every file run it **ONCE**, and your database should be created. You can run this on your local mysql workbench to see all the values:
```sql
SELECT *
from pokedex;
```
Feel free to change that depending on the database (it's either that or movepool)

After running the files the databases should be setup and then all the mysql commands, retrievals etc. will work

> [!CAUTION]
> Please make sure to hide your passwords when sharing this code. I have too in order for my own privacy!

## Final notes
This **is not** a good alpha release, this is just what I have done so far. You will find pieces of code that are missing or comments describing my current state. This is not polished yet however it is instead a very robust method to simulate pokemon battling.

# Pokemon Battle Simulator
Hello fellow reader, this is going to be my grand project. Pokemon as a game is rather complex in its calculations, having many complex formulas and confusing processes. Nevertheless over the next year I will begin attempting to create what I would consider an accurate battle simulator for any pokemon. Eventually, I will also begin optimising it for user experience and create an API but we need to start small.
