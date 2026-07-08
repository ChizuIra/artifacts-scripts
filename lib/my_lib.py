import os
from dotenv import load_dotenv
from time import sleep
import requests

load_dotenv() 
TOKEN = os.environ.get("TOKEN")

# tiles coordinates

TILE_LIST={
    "ZERO": { "x": 0, "y": 0 }, 
    "MINING": { "x": 0, "y": 0 },
    "CHIKEN":  { "x": 0, "y": 1 },
    "YELLOW_SLIM":  { "x": 1,"y":-2 },
    "COOKING":  { "x": 1, "y": 1 },
    "WEAPON_CRAFTING":  { "x": 2, "y": 1 },
    "BANK":  { "x": 4, "y": 1 },
    "COPPER":  { "x": 2,"y": 0 },
    "IRON":  { "x": 1, "y": 7 }, 
    "COAL":  { "x": 1, "y": 6 },
    "MINING":  { "x": 1, "y": 5 },
}



def arg_to_TILE(arg):
    match arg: 
        case "ZERO":
            return ZERO
        case "CHIKEN":
            return CHIKEN 
        case "YELLOW_SLIME":
            return YELLOW_SLIME
        case "COOKING":
            return COOKING
        case "WEAPON_CRAFTING":
            return WEAPON_CRAFTING
        case "BANK":
            return BANK
        case "COPPER":
            return COPPER
        case "IRON":
            return IRON
        case "COAL":
            return COAL
        case "MINING":
            return MINING
# the goat
def request_builder(character,action,info):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    if info != "":
        url = f"https://api.artifactsmmo.com/my/{character}/action/{action}"
        response = requests.post(url, headers=headers, json=info)
    else:
        url = f"https://api.artifactsmmo.com/my/{character}/action/{action}"
        response = requests.post(url, headers=headers)
        
    return response.json()


# actions
def gathering(character):
    info = "" 
    data = request_builder(character,"gathering",info)

    if "error" in data:
        print(f"❌ {data["error"]["message"]}")
        return data 

    cooldown = data["data"]["cooldown"]
    xp = data["data"]["details"]["xp"]

    print(f"{data["data"]["details"]["items"]} for {xp}xp")
    #print(f"✅ Gathering {quantity} {item} and gain {xp}xp")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")

    sleep(cooldown['total_seconds'])
    print("---")
    return data



def move(character,destination):
    info = destination
    print(f"destination : {destination}")
    data = request_builder(character,"move",info)

    if "error" in data:
        print(f"❌ {data["error"]["message"]}")
        return data 

    destination = data["data"]["destination"]
    cooldown = data["data"]["cooldown"]

    print(f"✅ Moved to ({destination['x']}, {destination['y']}) on {destination['name']}")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    sleep(cooldown['total_seconds'])
    print("---")
    return data

def fight(character):
    info = ""
    data = request_builder(character,"fight",info)

    if "error" in data:
        print(f"❌ {data["error"]["message"]}")
        return data 

    fight = data["data"]["fight"]
    fight_stats = fight["characters"][0]
    cooldown = data["data"]["cooldown"]

    print("🏆 Fight won!" if fight["result"] == "win" else "💀 Fight lost!")
    print(f"⚔️  XP gained: {fight_stats['xp']} | HP remaining: {fight_stats['final_hp']}")
    if len(fight_stats["drops"]) > 0:
        drops_str = ", ".join([f"{d['quantity']}x {d['code']}" for d in fight_stats["drops"]])
        print(f"🎁 Loot dropped: {drops_str}")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    sleep(cooldown['total_seconds'])
    print("---")
    return data

def rest(character):
    info = ""
    data = request_builder(character,"rest",info)

    if "error" in data:
        print(f"❌ {data["error"]["message"]}")
        return data 

    hp_restored = data["data"]["hp_restored"]
    character = data["data"]["character"]
    cooldown = data["data"]["cooldown"]

    print(f"🛏️   Rested and restored {hp_restored} HP.")
    print(f"❤️  Current HP: {character['hp']}/{character['max_hp']}")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    sleep(cooldown['total_seconds'])

def deposit_bank(character,code_item,quantity):
    info = [
        {
            "code": f"{code_item}",
            "quantity": quantity
        }
    ] 
    data = request_builder(character,"/bank/deposit/item",info)

    if "error" in data:
        print(f"❌ {data["error"]["message"]}")
        return data 

    cooldown = data["data"]["cooldown"]
    
    print(f"Deposit x{quantity} {code_item} in bank")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    
    sleep(cooldown['total_seconds'])
    print("---")
    return data


# pre build order    

# send the sauce deep into the bank~
def cuming_inventory_into_bank(character):
    data = move(character,BANK)
    i = 0
    for x in data["data"]["character"]["inventory"]:
        slot_x = data["data"]["character"]["inventory"][i]
        if slot_x["quantity"] != 0:
            #print(f"deposit x{slot_x["quantity"]} {slot_x["code"]}")
            deposit_bank(character,slot_x["code"],slot_x["quantity"])    
        i = i + 1
            
