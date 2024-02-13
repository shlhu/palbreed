from collections import defaultdict, OrderedDict
import json

from csv import DictReader


COMBI_RANKS = OrderedDict([
    ("Anubis", 570),
    ("Incineram", 590),
    ("Incineram Noct", 580),
    ("Mau", 1480),
    ("Mau Cryst", 1440),
    ("Rushoar", 1130),
    ("Lifmunk", 1430),
    ("Tocotoco", 1340),
    ("Eikthyrdeer", 920),
    ("Eikthyrdeer Terra", 900),
    ("Digtoise", 850),
    ("Galeclaw", 1030),
    ("Grizzbolt", 200),
    ("Teafant", 1490),
    ("Direhowl", 1060),
    ("Gorirat", 1040),
    ("Jolthog", 1370),
    ("Jolthog Cryst", 1360),
    ("Univolt", 680),
    ("Foxparks", 1400),
    ("Bristla", 1320),
    ("Lunaris", 1110),
    ("Pengullet", 1350),
    ("Dazzi", 1210),
    ("Gobfin", 1090),
    ("Gobfin Ignis", 1100),
    ("Lamball", 1470),
    ("Jormuntide", 310),
    ("Jormuntide Ignis", 315),
    ("Loupmoon", 950),
    ("Hangyu", 1420),
    ("Hangyu Cryst", 1422),
    ("Suzaku", 50),
    ("Suzaku Aqua", 30),
    ("Pyrin", 360),
    ("Pyrin Noct", 240),
    ("Elphidran", 540),
    ("Elphidran Aqua", 530),
    ("Woolipop", 1190),
    ("Cryolinx", 130),
    ("Melpaca", 890),
    ("Surfent", 560),
    ("Surfent Terra", 550),
    ("Cawgnito", 1080),
    ("Azurobe", 500),
    ("Cattiva", 1460),
    ("Depresso", 1380),
    ("Fenglope", 980),
    ("Reptyro", 320),
    ("Ice Reptyro", 230),
    ("Maraith", 1150),
    ("Robinquill", 1020),
    ("Robinquill Terra", 1000),
    ("Relaxaurus", 280),
    ("Relaxaurus Lux", 270),
    ("Kitsun", 830),
    ("Leezpunk", 1120),
    ("Leezpunk Ignis", 1140),
    ("Fuack", 1330),
    ("Vanwyrm", 660),
    ("Vanwyrm Cryst", 620),
    ("Chikipi", 1500),
    ("Dinossom", 820),
    ("Dinossom Lux", 810),
    ("Sparkit", 1410),
    ("Frostallion", 120),
    ("Frostallion Noct", 100),
    ("Mammorest", 300),
    ("Mammorest Cryst", 290),
    ("Felbat", 1010),
    ("Broncherry", 860),
    ("Broncherry Aqua", 840),
    ("Faleris", 370),
    ("Blazamut", 10),
    ("Caprity", 930),
    ("Reindrix", 880),
    ("Shadowbeak", 60),
    ("Sibelyx", 450),
    ("Vixy", 1450),
    ("Wixen", 1160),
    ("Lovander", 940),
    ("Hoocrates", 1390),
    ("Kelpsea", 1260),
    ("Kelpsea Ignis", 1270),
    ("Killamari", 1290),
    ("Mozzarina", 910),
    ("Wumpo", 460),
    ("Wumpo Botan", 480),
    ("Vaelet", 1050),
    ("Nitewing", 420),
    ("Flopie", 1280),
    ("Lyleen", 250),
    ("Lyleen Noct", 210),
    ("Elizabee", 330),
    ("Beegarde", 1070),
    ("Tombat", 750),
    ("Mossanda", 430),
    ("Mossanda Lux", 390),
    ("Arsox", 790),
    ("Rayhound", 740),
    ("Fuddler", 1220),
    ("Astegon", 150),
    ("Verdash", 990),
    ("Foxcicle", 760),
    ("Jetragon", 90),
    ("Daedream", 1230),
    ("Tanzee", 1250),
    ("Blazehowl", 710),
    ("Blazehowl Noct", 670),
    ("Kingpaca", 470),
    ("Ice Kingpaca", 440),
    ("Gumoss", 1240),
    ("Swee", 1300),
    ("Sweepa", 410),
    ("Katress", 700),
    ("Ribbuny", 1310),
    ("Beakon", 220),
    ("Warsect", 340),
    ("Paladius", 80),
    ("Nox", 1180),
    ("Penking", 520),
    ("Chillet", 800),
    ("Quivern", 350),
    ("Helzephyr", 190),
    ("Ragnahawk", 380),
    ("Bushi", 640),
    ("Celaray", 870),
    ("Necromus", 70),
    ("Petallia", 780),
    ("Grintale", 510),
    ("Cinnamoth", 490),
    ("Menasting", 260),
    ("Orserk", 140),
    ("Cremis", 1455),
    ("Dumud", 895),
    ("Flambelle", 1405),
    ("Rooby", 1155),
])

UNIQUE_COMBI = {
    ("Relaxaurus", "Sparkit"): "Relaxaurus Lux",
    ("Incineram", "Maraith"): "Incineram Noct",
    ("Mau", "Pengullet"): "Mau Cryst",
    ("Vanwyrm", "Foxcicle"): "Vanwyrm Cryst",
    ("Eikthyrdeer", "Hangyu"): "Eikthyrdeer Terra",
    ("Elphidran", "Surfent"): "Elphidran Aqua",
    ("Pyrin", "Katress"): "Pyrin Noct",
    ("Mammorest", "Wumpo"): "Mammorest Cryst",
    ("Mossanda", "Grizzbolt"): "Mossanda Lux",
    ("Dinossom", "Rayhound"): "Dinossom Lux",
    ("Jolthog", "Pengullet"): "Jolthog Cryst",
    ("Frostallion", "Helzephyr"): "Frostallion Noct",
    ("Kingpaca", "Reindrix"): "Ice Kingpaca",
    ("Lyleen", "Menasting"): "Lyleen Noct",
    ("Leezpunk", "Flambelle"): "Leezpunk Ignis",
    ("Blazehowl", "Felbat"): "Blazehowl Noct",
    ("Robinquill", "Fuddler"): "Robinquill Terra",
    ("Broncherry", "Fuack"): "Broncherry Aqua",
    ("Surfent", "Dumud"): "Surfent Terra",
    ("Gobfin", "Rooby"): "Gobfin Ignis",
    ("Suzaku", "Jormuntide"): "Suzaku Aqua",
    ("Reptyro", "Foxcicle"): "Ice Reptyro",
    ("Hangyu", "Swee"): "Hangyu Cryst",
    ("Frostallion", "Frostallion"): "Frostallion",
    ("Jetragon", "Jetragon"): "Jetragon",
    ("Paladius", "Paladius"): "Paladius",
    ("Necromus", "Necromus"): "Necromus",
    ("Mossanda", "Petallia"): "Lyleen",
    ("Vanwyrm", "Anubis"): "Faleris",
    ("Mossanda", "Rayhound"): "Grizzbolt",
    ("Grizzbolt", "Relaxaurus"): "Orserk",
    ("Kitsun", "Astegon"): "Shadowbeak",
    ("Lyleen", "Lyleen"): "Lyleen",
    ("Faleris", "Faleris"): "Faleris",
    ("Grizzbolt", "Grizzbolt"): "Grizzbolt",
    ("Orserk", "Orserk"): "Orserk",
    ("Shadowbeak", "Shadowbeak"): "Shadowbeak",
    ("Jormuntide Ignis", "Jormuntide Ignis"): "Jormuntide Ignis",
    ("Relaxaurus Lux", "Relaxaurus Lux"): "Relaxaurus Lux",
    ("Incineram Noct", "Incineram Noct"): "Incineram Noct",
    ("Mau Cryst", "Mau Cryst"): "Mau Cryst",
    ("Vanwyrm Cryst", "Vanwyrm Cryst"): "Vanwyrm Cryst",
    ("Eikthyrdeer Terra", "Eikthyrdeer Terra"): "Eikthyrdeer Terra",
    ("Elphidran Aqua", "Elphidran Aqua"): "Elphidran Aqua",
    ("Pyrin Noct", "Pyrin Noct"): "Pyrin Noct",
    ("Mammorest Cryst", "Mammorest Cryst"): "Mammorest Cryst",
    ("Mossanda Lux", "Mossanda Lux"): "Mossanda Lux",
    ("Dinossom Lux", "Dinossom Lux"): "Dinossom Lux",
    ("Jolthog Cryst", "Jolthog Cryst"): "Jolthog Cryst",
    ("Frostallion Noct", "Frostallion Noct"): "Frostallion Noct",
    ("Ice Kingpaca", "Ice Kingpaca"): "Ice Kingpaca",
    ("Lyleen Noct", "Lyleen Noct"): "Lyleen Noct",
    ("Leezpunk Ignis", "Leezpunk Ignis"): "Leezpunk Ignis",
    ("Blazehowl Noct", "Blazehowl Noct"): "Blazehowl Noct",
    ("Robinquill Terra", "Robinquill Terra"): "Robinquill Terra",
    ("Broncherry Aqua", "Broncherry Aqua"): "Broncherry Aqua",
    ("Surfent Terra", "Surfent Terra"): "Surfent Terra",
    ("Gobfin Ignis", "Gobfin Ignis"): "Gobfin Ignis",
    ("Suzaku Aqua", "Suzaku Aqua"): "Suzaku Aqua",
    ("Ice Reptyro", "Ice Reptyro"): "Ice Reptyro",
    ("Hangyu Cryst", "Hangyu Cryst"): "Hangyu Cryst",
}

UNIQUE_CHILDREN = set(UNIQUE_COMBI.values())


def FindChildCharacterId(parent_a: str, parent_b: str) -> str:
    if (parent_a, parent_b) in UNIQUE_COMBI:
        return UNIQUE_COMBI[(parent_a, parent_b)]
    elif (parent_b, parent_a) in UNIQUE_COMBI:
        return UNIQUE_COMBI[(parent_b, parent_a)]
    else:
        return FindNearestCombiRank(
            (COMBI_RANKS[parent_a] + COMBI_RANKS[parent_b] + 1) // 2)


def FindNearestCombiRank(combi_rank: int) -> str:
    return min(
        (x for x in COMBI_RANKS.items() if x[0] not in UNIQUE_CHILDREN),
        key=lambda x: abs(x[1] - combi_rank))[0]


def import_csv(outfile):
    data = []
    with open(outfile, "r") as f:
        reader = DictReader(f)
        for row in reader:
            row["skills"] = json.loads(row["skills"].replace("'", '"'))
            data.append(row)
    return data


ATTRS = ("mount", "work")


def build_seeds(data):
    blank = {}
    for attr in ATTRS:
        blank[(attr, "M")] = None
        blank[(attr, "F")] = None
    seeds = {}
    for pal in data:
        if pal["pal"] not in seeds:
            seeds["pal"] = dict(blank)
        for attr in ATTRS:
            iscore = attr + "_score"
            if not pal["not_" + iscore]:
                best = seeds[pal["pal"]][(attr, pal["gender"])] or 0
                best = max(best, pal[iscore])
                seeds[pal["pal"]][(attr, pal["gender"])] = best
    return seeds


def main():
    data = import_csv("paldata.csv")
    seeds = build_seeds(data)


if __name__ == "__main__":
    main()
