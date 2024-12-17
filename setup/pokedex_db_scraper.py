import requests
from bs4 import BeautifulSoup


URL_STATS = "https://pokemondb.net/pokedex/all"
URL_BIOMETRICS = "https://pokemondb.net/pokedex/stats/height-weight"
URL_ABILITIES = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Ability"


stat_page = requests.get(URL_STATS)
stat_soup = BeautifulSoup(stat_page.content, "html.parser")
stat_dex = stat_soup.find(id="pokedex")


biometrics_page = requests.get(URL_BIOMETRICS)
soup = BeautifulSoup(biometrics_page.content, "html.parser")
biometric_dex = soup.find(class_="data-table")

abilities_page = requests.get(URL_ABILITIES)
abilities_soup = BeautifulSoup(abilities_page.content, "html.parser")
abilities_dex = abilities_soup.find_all(class_="sortable")

dex_entries = stat_dex.find_all("tr")[1:]
biometric_entries = biometric_dex.find_all("tr")[1:]
# abilities_entries = abilities_dex.find_all("tr")[1:]

# print(len(abilities_dex))




pokedex = []

names = stat_dex.find_all("td", class_="cell-name")

bio_names = biometric_dex.find_all("td", class_="cell-name")

# for i in range(len(bio_names)):
#     if names[i].text == bio_names[i].text:
#         continue
#     print(bio_names[i].text, names[i].text)
#     print(bio_names[i - 1].text, names[i - 1].text)
#     print(bio_names[i - 2].text, names[i - 2].text)
#     print(bio_names[i - 3].text, names[i - 3].text)
#     break

for entry in dex_entries:
    name = entry.find("td", class_="cell-name")
    if name.text == "Eternatus Eternamax":  # unusable and no data for height and weight...
        continue
    # gets the name of the Pokémon (includes all forms, megas etc.)
    stats = entry.find_all("td", class_="cell-num")[2:]
    types = entry.find_all("a", class_="type-icon")
    type2 = None

    if len(types) == 2:
        type2 = types[1].text
    type1 = types[0].text

    hp = int(stats[0].text)
    atk = int(stats[1].text)
    defense = int(stats[2].text)
    spa = int(stats[3].text)
    spd = int(stats[4].text)
    speed = int(stats[5].text)

    bst = hp + atk + defense + spa + spd + speed
    pokedex.append((name.text, type1, type2, bst, hp, atk, defense, spa, spd, speed))

for i, entry in enumerate(biometric_entries):
    stats = entry.find_all("td", class_="cell-num")
    pokedex[i] += (float(stats[2].text), float(stats[4].text), None, None, None)
