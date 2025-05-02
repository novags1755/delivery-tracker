#tibia_v1_tracker

def parse_hunt_data(raw_data):
    players = []
    lines = raw_data.strip().split("\n")
    current_player = None


    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if not line.startswith(('loot:','Supplies:','Balance:','Damage:','Healing:')):
            #hope am doing great am just retyping pretty much!
            current_player = {'name':line}
            players.append(current_player)
        else:
            key, value = line.split(': ')
            key = key.lower()
            value = int(value.replace(',',''))
            current_player[key] = value

    return players

sample_data = """
John Doe
Loot: 50,000 gp
Supplies: 10,000 gp

Jane Smith
Loot: 75,000 gp
Supplies: 25,000 gp
"""


parsed_data = parse_hunt_data(sample_data)#<--- why this one VS is highlighting it yellow
for player in parsed_data:
    print(player)
