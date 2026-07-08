from lib.my_lib import *
import sys

# my char list memo :
# .char1
# .char2
# .
# .
# .

#missions
def mob_farming(character,zone):
    move(character,zone)
    while True:
        rest(character)
        response = fight(character)
        try:
            if response["error"]["code"] == 497:
                cuming_inventory_into_bank(character)
                move(character,zone)
        except:
            continue

def ressource_farming(character,zone):
    move(character,zone)
    while True:
        response = gathering(character)
        try:
            if response["error"]["code"] == 497:
                cuming_inventory_into_bank(character)
                move(character,zone)
        except:
            continue

#script start here
character = sys.argv[1]
mission = sys.argv[2]
zone = sys.argv[3]

if zone in TILE_LIST: 
    match mission:
        case "mob":
            mob_farming(character,TILE_LIST[zone])
        case "ressource":
            ressource_farming(character,TILE_LIST[zone])
        case _:
            print(f"'{mission}' n'est pas une mission valide")
else:
    print(f"'{zone}' n'est pas une zone connu")
    print(f"zone connu : {TILE_LIST}")
