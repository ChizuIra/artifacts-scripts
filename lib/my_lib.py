TOKEN = "token here" 

from time import sleep
import requests


# Target coordinates
chiken_farm = { "x": 0, "y": 1 }
y_slime = { "x": 1,"y":-2 }
cooking = { "x": 1, "y": 1 }
weapon_crafting = { "x": 2, "y": 1 }
bank = { "x": 4, "y": 1 }



# GET functions
def get_character(character):
    url = f"https://api.artifactsmmo.com/characters/{character}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "error" in data:
            raise Exception(data["error"]["message"])

        print("Successfully fetched character.")
        print(data["data"]["cooldown"]) 
        sleep(data["data"]["cooldown"])
    except Exception as e:
        print(f"❌ {e}")
    print("---")
    return data

# actions
def move(character,destination):
    # API endpoint for the move action
    url = f"https://api.artifactsmmo.com/my/{character}/action/move"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, headers=headers, json=destination)
    data = response.json()

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
    # API endpoint to start a fight against the monster on the current tile
    url = f"https://api.artifactsmmo.com/my/{character}/action/fight"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    
    response = requests.post(url, headers=headers)
    data = response.json()

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
    # API endpoint to make your character rest and recover HP
    url = f"https://api.artifactsmmo.com/my/{character}/action/rest"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        response = requests.post(url, headers=headers)
        data = response.json()

        if "error" in data:
            raise Exception(data["error"]["message"])

        hp_restored = data["data"]["hp_restored"]
        character = data["data"]["character"]
        cooldown = data["data"]["cooldown"]

        print(f"🛏️   Rested and restored {hp_restored} HP.")
        print(f"❤️  Current HP: {character['hp']}/{character['max_hp']}")
        print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
        sleep(cooldown['total_seconds'])
    except Exception as e:
        print(f"❌ {e}")
    print("---")

def deposit_bank(character,code_item,quantity):
    url = f"https://api.artifactsmmo.com/my/{character}/action/bank/deposit/item"
    payload = [
        {
            "code": f"{code_item}",
            "quantity": quantity
        }
    ]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    if "error" in data:
        print(f"❌ {data["error"]["message"]}")
        return data 

    cooldown = data["data"]["cooldown"]
    
    print(f"Deposit x{quantity} {code_item} in bank")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    
    sleep(cooldown['total_seconds'])
    print("---")
    return data


# send the sauce deep into the bank~
def cuming_inventory_into_bank(character):
    data = move(character,bank)
    i = 0
    for x in data["data"]["character"]["inventory"]:
        slot_x = data["data"]["character"]["inventory"][i]
        if slot_x["quantity"] != 0:
            #print(f"deposit x{slot_x["quantity"]} {slot_x["code"]}")
            deposit_bank(character,slot_x["code"],slot_x["quantity"])    
        i = i + 1
            
