TOKEN = "your token here" 

from time import sleep
import requests


# Target coordinates
chiken_farm = { "x": 0, "y": 1 }
y_slime = { "x": 1,"y":-2 }
cooking = { "x": 1, "y": 1 }
weapon_crafting = { "x": 2, "y": 1 }

# Actions function
def move(character,body):
    # API endpoint for the move action
    url = f"https://api.artifactsmmo.com/my/{character}/action/move"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        if "error" in data:
            raise Exception(data["error"]["message"])

        destination = data["data"]["destination"]
        cooldown = data["data"]["cooldown"]

        print(f"✅ Moved to ({destination['x']}, {destination['y']}) on {destination['name']}")
        print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    except Exception as e:
        print(f"❌ {e}")
    print("---")
    sleep(cooldown['total_seconds'])

def fight(character):
    # API endpoint to start a fight against the monster on the current tile
    url = f"https://api.artifactsmmo.com/my/{character}/action/fight"
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

        fight = data["data"]["fight"]
        fight_stats = fight["characters"][0]
        cooldown = data["data"]["cooldown"]

        print("🏆 Fight won!" if fight["result"] == "win" else "💀 Fight lost!")
        print(f"⚔️  XP gained: {fight_stats['xp']} | HP remaining: {fight_stats['final_hp']}")
        if len(fight_stats["drops"]) > 0:
            drops_str = ", ".join([f"{d['quantity']}x {d['code']}" for d in fight_stats["drops"]])
            print(f"🎁 Loot dropped: {drops_str}")
        print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
    except Exception as e:
        print(f"❌ {e}")
    print("---")
    sleep(cooldown['total_seconds'])

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
    except Exception as e:
        print(f"❌ {e}")
    print("---")
    sleep(cooldown['total_seconds'])


