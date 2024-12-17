import random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR password!",
    database="pokemon_database"
)

mycursor = mydb.cursor()


class Pokemon:
    def __init__(self, name, level, type1, type2, ability1, ability2, hidden_ability, nature, ev, iv, base_stats,
                 moveset=None, held_item=None, gender="Male"):

        if moveset is None:
            moveset = []

        self.name = name
        self.gender = gender
        self.level = level

        self.type1 = type1
        self.type2 = type2
        self.ability1 = ability1
        self.ability2 = ability2
        self.hidden_ability = hidden_ability

        self.nature = nature
        self.held_item = held_item

        self.status = "healthy"
        self.toxic_counter = 1
        self.sleep_counter = 0

        self.ev = ev
        self.iv = iv
        self.base_stats = base_stats

        self.hp = self.calculate_hp()
        self.attack = self.calculate_stat("attack")
        self.defense = self.calculate_stat("defense")
        self.special_attack = self.calculate_stat("spatk")
        self.special_defense = self.calculate_stat("spdef")
        self.speed = self.calculate_stat("speed")

        self.pseudo_stats = [1 / 1, 1 / 1, 0]  # accuracy, evasion, crit chance !!
        # Increase denom. = DIVIDE by multiplier

        self.moveset = moveset


        # TODO: status conditions

    def calculate_hp(self):
        return int((((2 * self.base_stats[0] + self.iv[0] + (self.ev[0] / 4)) * self.level) / 100) + self.level + 10)

    def calculate_stat(self, stat):
        # match statement to figure out which stat is being modified
        index_val = 0

        match stat:
            case "attack":
                index_val = 1
            case "defense":
                index_val = 2
            case "spatk":
                index_val = 3
            case "spdef":
                index_val = 4
            case "speed":
                index_val = 5

        # checks the nature boost/reductions
        nature_modifier = 1

        if self.nature.boosted_stat == self.nature.reduced_stat:
            nature_modifier = 1
        elif self.nature.boosted_stat == stat:
            nature_modifier = 1.1
        elif self.nature.reduced_stat == stat:
            nature_modifier = 0.9

        result = ((((2 * self.base_stats[index_val] + self.iv[index_val] + (self.ev[index_val] / 4))
                    * self.level) / 100) + 5) * nature_modifier

        return int(result)

    def reset_stats(self):
        self.hp = self.calculate_hp()
        self.attack = self.calculate_stat("attack")
        self.defense = self.calculate_stat("defense")
        self.special_attack = self.calculate_stat("spatk")
        self.special_defense = self.calculate_stat("spdef")
        self.speed = self.calculate_stat("speed")

    def add_moves(self, *moves):

        for move in moves:
            if len(self.moveset) >= 4:
                return

            self.moveset.append(move_lib.retrieve_move(move))

    def calculate_crit(self):
        match self.pseudo_stats[2]:
            case 0:
                max_val = 24
            case 1:
                max_val = 8
            case 2:
                max_val = 2
            case _:
                max_val = 1

        if max_val == 1:
            return 1.5

        roll = random.randint(1, max_val)
        if roll == 1:
            return 1.5

        return 1

    def check_stab(self, move):
        typings = [self.type1, self.type2]

        for typing in typings:
            if typing is None:
                continue
            if typing.name == move.move_type:
                return 1.5
        return 1

    @staticmethod
    def type_matchups(move, enemy, weather):

        type_modifier = 1
        if move.move_type in enemy.type1.immune or (enemy.type2 is not None and move.move_type in enemy.type2.immune):
            return 0

        typings = [enemy.type1, enemy.type2]

        for typing in typings:
            if typing is None:
                continue

            if move.move_type in typing.weak:
                type_modifier *= 2
            elif move.move_type in typing.resist:
                type_modifier *= 0.5

            if (move.move_type == "electric" or move.move_type == "rock" or move.move_type == "ice") and weather == "strong winds":
                type_modifier *= 0.5

        return type_modifier

    @staticmethod
    def weather_calculator(move, weather):
        match weather:
            case "harsh sunlight":
                if move.move_type == "fire":
                    return 1.5
                elif move.move_type == "water":
                    return 0.5

                return 1
            case "rain":
                if move.move_type == "water":
                    return 1.5
                elif move.move_type == "fire":
                    return 0.5

                return 1
            case _:
                return 1

    def is_burned(self, move):
        if self.status == "burn" and move.category == "physical":
            return 0.5

        return 1

    def damage_calculator(self, move, enemy, weather):
        A = self.attack
        D = enemy.defense

        if move.category == "special":
            A = self.special_attack
            D = enemy.special_defense

        base_damage = math.floor(math.floor(math.floor(2 * self.level / 5 + 2) * move.power * A / D) // 50 + 2)

        # TODO: Double battles, glaive rush (secondary effect), burns, z-moves, terrastalisation
        type_matchups = self.type_matchups(move, enemy, weather)

        if type_matchups == 0:
            return -3

        damage = math.floor(base_damage * self.weather_calculator(move, weather))
        damage = math.floor(damage * self.calculate_crit())
        damage = math.floor(damage * (random.randint(85, 100) / 100))
        damage = math.floor(damage * self.check_stab(move))
        damage = math.floor(damage * type_matchups)
        damage = math.floor(damage * self.is_burned(move))

        return damage

    def take_damage(self, amount):
        resultant_hp = self.hp - amount
        if resultant_hp > 0:
            self.hp -= amount
        else:
            self.hp = 0

    def use_move(self, move, enemy, weather):
        # makes sure that the move actually hits
        # TODO: add accuracy formula
        # CURRENT: Adding sleep
        if self.status == "sleep":
            # TODO: add percentage of waking up by sleep (after 1 turn: 1/3, 2 turns: 1/2, 3 turns: guaranteed)
            return -5
        elif self.status == "paralysis":
            turn_lost = random.randint(1, 4)
            if turn_lost == 1:
                return -4

        is_hit = random.randint(1, 100)

        if is_hit > move.accuracy:  # code result for misses
            return -2

        move_damage = self.damage_calculator(move, enemy, weather)

        if move_damage == -3:  # code result for immunities
            return -3

        enemy.take_damage(move_damage)
        return move_damage
