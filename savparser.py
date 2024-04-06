from csv import DictWriter


from palworld_save_tools.gvas import GvasFile
from palworld_save_tools.palsav import decompress_sav_to_gvas
from palworld_save_tools.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS
from lib.PalInfo import PalEntity

import pdb


def parse_sav(filename):
    print(f"Decompressing sav file")
    with open(filename, "rb") as f:
        data = f.read()
        raw_gvas, _ = decompress_sav_to_gvas(data)
    print(f"Loading GVAS file")
    gvas_file = GvasFile.read(
        raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
    return gvas_file.dump()


COMBAT_SKILLS = {
    "Legend": 8,
    "Ferocious": 4,
    "Musclehead": 2,
    "Lucky": 1,
    "Swift": 1,
    "Divine Dragon": 1,
    "Spirit Emperor": 1,
    "Lord of the Sea": 1,
    "Lord of Lightning": 4,
    "Lord of the Underworld": 1,
    "Ice Emperor": 1,
    "Flame Emperor": 1,
    "Celestial Emperor": 1,
}

WORK_SKILLS = {
    "Artisan": 8,
    "Work Slave": 4,
    "Serious": 2,
    "Lucky": 1,
}

MOUNT_SKILLS = {
    "Legend": 8,
    "Swift": 4,
    "Runner": 2,
    "Nimble": 1,
}

OWNERS = {
    "b1b": "Axle",
    "548": "Shlhu",
    "3b5": "MeltUp"
}


def extra_col(entity):
    # Currently just check for dark whisp
    if entity.GetLearntMoves().count("EPalWazaID::DarkLegion"):
        return True
    return False


def convert_to_short_dict(entity):
    data = {
        "owner": OWNERS[str(entity.GetOwner())[:3]],
        "level": entity.GetLevel(),
        "pal": entity.GetName(),
        "skills": entity.GetReadableSkills(),
        "gender": entity.GetGender()[0],
        "mount_score": 0,
        "not_mount_score": 0,
        "work_score": 0,
        "not_work_score": 0,
        "combat_score": 0,
        "not_combat_score": 0,
        "hp": entity.GetTalentHP(),
        "melee": entity.GetAttackMelee(),
        "ranged": entity.GetAttackRanged(),
        "def": entity.GetDefence(),
        "total_100": 0,
        "extra_col": extra_col(entity),
        "slot": entity.storageSlot
    }
    for stat in ("hp", "ranged", "def"):
        if data[stat] == 100:
            data["total_100"] += 1

    for skill in data["skills"]:
        if skill in COMBAT_SKILLS:
            data["combat_score"] += COMBAT_SKILLS[skill]
        else:
            data["not_combat_score"] += 1
        if skill in WORK_SKILLS:
            data["work_score"] += WORK_SKILLS[skill]
        else:
            data["not_work_score"] += 1
        if skill in MOUNT_SKILLS:
            data["mount_score"] += MOUNT_SKILLS[skill]
        else:
            data["not_mount_score"] += 1
    return data


def get_paldata(infile):
    data = parse_sav(infile)
    pals = []
    for paldata in data['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value']:
        try:
            p = convert_to_short_dict(PalEntity(paldata))
            pals.append(p)
        except Exception as e:
            print(e)
    return pals


def export_csv(paldata, outfile):
    with open(outfile, "w", newline="") as f:
        fieldnames = [
            "owner", "level", "pal", "skills", "gender", "combat_score", "not_combat_score",
            "mount_score", "not_mount_score", "work_score", "not_work_score",
            "hp", "melee", "ranged", "def", "total_100", "extra_col", "slot"]
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in paldata:
            writer.writerow(row)


def main():
    data = get_paldata("Level.sav")
    export_csv(data, "paldata.csv")


if __name__ == "__main__":
    main()
