import zlib

from collections import defaultdict
from csv import DictWriter


from lib.gvas import GvasFile
from lib.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS
from lib.PalInfo import PalEntity

MAGIC_BYTES = b"PlZ"


def decompress_sav_to_gvas(data: bytes) -> tuple[bytes, int]:
    uncompressed_len = int.from_bytes(data[0:4], byteorder="little")
    compressed_len = int.from_bytes(data[4:8], byteorder="little")
    magic_bytes = data[8:11]
    save_type = data[11]
    # Check for magic bytes
    if magic_bytes != MAGIC_BYTES:
        if (
            magic_bytes == b"\x00\x00\x00"
            and uncompressed_len == 0
            and compressed_len == 0
        ):
            raise Exception(
                f"not a compressed Palworld save, found too many null bytes, this is likely corrupted"
            )
        raise Exception(
            f"not a compressed Palworld save, found {magic_bytes} instead of {MAGIC_BYTES}"
        )
    # Valid save types
    if save_type not in [0x30, 0x31, 0x32]:
        raise Exception(f"unknown save type: {save_type}")
    # We only have 0x31 (single zlib) and 0x32 (double zlib) saves
    if save_type not in [0x31, 0x32]:
        raise Exception(f"unhandled compression type: {save_type}")
    if save_type == 0x31:
        # Check if the compressed length is correct
        if compressed_len != len(data) - 12:
            raise Exception(f"incorrect compressed length: {compressed_len}")
    # Decompress file
    uncompressed_data = zlib.decompress(data[12:])
    if save_type == 0x32:
        # Check if the compressed length is correct
        if compressed_len != len(uncompressed_data):
            raise Exception(f"incorrect compressed length: {compressed_len}")
        # Decompress file
        uncompressed_data = zlib.decompress(uncompressed_data)
    # Check if the uncompressed length is correct
    if uncompressed_len != len(uncompressed_data):
        raise Exception(f"incorrect uncompressed length: {uncompressed_len}")

    return uncompressed_data, save_type


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
            "hp", "melee", "ranged", "def", "total_100", "slot"]
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in paldata:
            writer.writerow(row)


def main():
    data = get_paldata("Level.sav")
    export_csv(data, "paldata.csv")


if __name__ == "__main__":
    main()
