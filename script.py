from lib.my_lib import *

character = "char1"
farming_zone = chiken_farm

# script start here
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


