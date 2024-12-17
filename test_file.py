import natures
import pk_types
from pokemon_class import Pokemon

articuno = Pokemon("Articuno", 100, pk_types.ice, pk_types.flying, "Pressure", None,
                   "Snow Cloak", natures.adamant, [0, 0, 0, 0, 0, 0], [31, 31, 31, 31, 31, 31],
                   [90, 85, 100, 95, 125, 85])

ursaring = Pokemon("Ursaring", 100, pk_types.normal, None, "Guts", "Quick feet",
                   "Unnerve", natures.impish, [0, 0, 0, 0, 0, 0], [31, 31, 31, 31, 31, 31],
                   [90, 130, 75, 75, 75, 55])

incineroar = Pokemon("Incineroar", 100, pk_types.fire, pk_types.dark, "Blaze", None,
                     "Intimidate", natures.hardy, [0, 0, 0, 0, 0, 0], [31, 31, 31, 31, 31, 31],
                     [95, 115, 90, 80, 90, 60])

dusknoir = Pokemon("Dusknoir", 100, pk_types.ghost, None, "Pressure", None,
                   "Frisk", natures.hardy, [0, 0, 0, 0, 0, 0], [31, 31, 31, 31, 31, 31],
                   [45, 100, 135, 65, 135, 45])

articuno.add_moves("Ice Beam", "Blizzard", "Agility", "Protect")
ursaring.add_moves("Slash", "Swords Dance", "Tackle", "Throat Chop")
incineroar.add_moves("Flare Blitz", "Darkest Lariat", "U-turn", "Throat Chop")
dusknoir.add_moves("Dark Pulse", "Shadow Ball", "Phantom Force", "Shadow punch")


def italics(text):
    return '\x1B[3m' + text + '\x1B[23m'


def speed_check(mons):
    turn_order = []  # stack implementation
    mons = [mon for mon in mons if mon is not None]  # gets rid of all spare none values
    turn_order = mons.copy()

    for i in range(1, len(turn_order)):  # uses insertion sort to order by speed. data size not large, fastest O(n).
        j = i
        while j > 0 and turn_order[j - 1].speed > turn_order[j].speed:
            turn_order[j], turn_order[j - 1] = turn_order[j - 1], turn_order[j]
            j -= 1

    return turn_order


def select_target(user, mons, user_mons, enemy_mons):
    print("-" * 5, "SELECT TARGET", "-" * 5)
    targets = mons.copy()
    targets = [target for target in targets if target != user]

    print(
        f"{user.name:<15} | {float(user.hp)} HP / {float(user.calculate_hp())} HP ({round(float(user.hp / user.calculate_hp()) * 100, 1)}%) (USER)\n")
    for number, target in enumerate(targets):
        if (target in user_mons and user in user_mons) or (target in enemy_mons and user in enemy_mons):
            print(
                f"{number + 1}) {target.name:<12} | {float(target.hp)} HP / {float(target.calculate_hp())} HP ({round(float(target.hp / target.calculate_hp()) * 100, 1)}%) | Ally")

            continue

        print(
            f"{number + 1}) {target.name:<12} | {float(target.hp)} HP / {float(target.calculate_hp())} HP ({round(float(target.hp / target.calculate_hp()) * 100, 1)}%) | Opponent")

    print("-" * 25)

    target_mon_index = int(input("Please enter the number of the target you wish to attack: "))
    return targets[target_mon_index - 1]


def select_move(user):
    print("-" * 9, "MOVES", "-" * 9)

    for number, move in enumerate(user.moveset):
        print(f"{number + 1}) {move.name}")

    print("-" * 25)

    selected_move_index = int(input("Please enter the number of the move you want to use: "))
    return user.moveset[selected_move_index - 1]


# TODO: conditions left to add: sleep, drowsiness, freeze


def weather_changes(mons, weather):
    match weather:
        case "snow":
            for mon in mons:
                if mon.type1 == "ice" or mon.type2 == "ice":
                    mon.defense *= 1.5
        case "sandstorm":
            for mon in mons:
                if mon.type1 == "rock" or mon.type2 == "rock":
                    mon.special_defense *= 1.5


def sot_damage(mons, weather):
    pass
    # this is where field effects e.g. tailwinds and trick rooms will have their speed calc for all moves etc. calced


def eot_damage(mons, weather):  # eot = end of turn
    for mon in mons:
        types = [mon.type1, mon.type2]

        # sandstorm implementation
        if weather == "sandstorm" and ("rock" not in types or "ground" not in types or "steel" not in types):
            mon.hp -= mon.calculate_hp() / 16

        if mon.status == "poison" or mon.status == "burn":
            mon.hp -= mon.calculate_hp() * 1 / 16
        elif mon.status == "badly poisoned":
            mon.hp -= mon.calculate_hp() * mon.toxic_counter / 16
            mon.toxic_counter += 1


def turn(user_mons, enemy_mons, pre_weather):
    weather = pre_weather
    user_mon1, user_mon2, enemy_mon1, enemy_mon2 = 0, 0, 0, 0

    if len(user_mons) == 2:
        user_mon1, user_mon2 = user_mons
    elif len(user_mons) == 1:
        user_mon1 = user_mons[0]
        user_mon2 = None

    if len(enemy_mons) == 2:
        enemy_mon1, enemy_mon2 = enemy_mons
    elif len(enemy_mons) == 1:
        enemy_mon1 = enemy_mons[0]
        enemy_mon2 = None

    mons = [user_mon1, user_mon2, enemy_mon1, enemy_mon2]

    speed_stack = speed_check(mons)[::-1]  # turn order calculations

    for mon in speed_stack:
        target_mon = select_target(mon, speed_stack, user_mons, enemy_mons)
        selected_move = select_move(mon)

        print("-" * 25)

        result = mon.use_move(selected_move, target_mon, weather)

        print(f"{mon.name} used {italics(selected_move.name)}!\n")
        if result == -2:
            print(f"The move {italics("missed")}!")
        elif result == -3:
            print(f"{target_mon.name} is {italics("immune")} to {selected_move.name}!")
        elif result == -4:
            print(f"{mon.name} couldn't move because it's paralysed!")
        elif result == -5:
            print(f"{mon.name} is fast asleep.")
            mon.sleep_counter += 1
        else:
            print(
                f"{target_mon.name} lost {italics(str(result))} HP! ({target_mon.hp}.00 HP / {target_mon.calculate_hp()}.00 HP)")

        print("-" * 25, "\n")

    eot_damage(mons, weather)


turn([articuno, incineroar], [ursaring, dusknoir], "rain")
