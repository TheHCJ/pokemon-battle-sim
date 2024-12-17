import requests
from bs4 import BeautifulSoup

MOVEPOOL_URL = "https://pokemondb.net/move/all"

movepool_page = requests.get(MOVEPOOL_URL)

soup = BeautifulSoup(movepool_page.content, "html.parser")

move_table = soup.find(id="moves")

moves = soup.find_all("tr")[1:]
movedex = []

for move in moves:
    name = move.find(class_="cell-name").text
    icons = move.find_all(class_="cell-icon")
    move_type = icons[0].text
    category = icons[1]["data-filter-value"]
    nums = move.find_all(class_="cell-num")
    power, accuracy, pp, probability = tuple([i.text for i in nums])
    effect = move.find(class_="cell-long-text").text

    # database validation
    if effect == "":
        effect = "No effect."   # done
    if accuracy == "∞":     # done
        accuracy = 2048
    elif accuracy == "—":   # done
        accuracy = -1
    if power == "—":    # done
        power = 0
    if category == "":
        category = "Gimmick"  # done
    if probability == "—":  # done
        probability = 0
    if pp == "—":
        pp = -1

    movedex.append((name, move_type, category, power, accuracy, pp, effect, probability))
