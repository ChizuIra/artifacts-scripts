from lib.my_lib import *

# char list :
# .char1
# .
# .
# .
# .

farming_zone = y_slime
gathering_zone = cooper_mine


def mob_farming(character,zone):
    move(character,farming_zone)
    while True:
        rest(character)
        response = fight(character)
        try:
            if response["error"]["code"] == 497:
                cuming_inventory_into_bank(character)
                move(character,farming_zone)
        except:
            continue

def ressource_farming(character,zone):
    move(character,gathering_zone)
    while True:
        response = gathering(character)
        try:
            if response["error"]["code"] == 497:
                cuming_inventory_into_bank(character)
                move(character,gathering_zone)
        except:
            continue


ressource_farming("char1",gathering_zone)
