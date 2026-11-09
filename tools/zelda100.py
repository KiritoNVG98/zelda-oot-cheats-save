#!/usr/bin/env python3
"""
zelda100.py - gives a The Legend of Zelda: Ocarina of Time (Switch 2, 0400486024DEC000) save
the full inventory: every weapon, shield, tunic, boot, item, song, upgrade, medallion, stone,
mask and trade item, 20 hearts, full double magic, double defence, 100 Gold Skulltula tokens,
the largest wallet/quiver/bags with their real caps, Golden Gauntlets and Scale, and the Ocarina of
Time equipped.

Usage:
    python3 zelda100.py progress.sav            -> writes progress.sav.100 next to it
    python3 zelda100.py progress.sav 1000       -> same, with a custom rupee count

It never touches the original file. It only changes values that already exist in the save
(the file keeps its size), so a save from another version is refused key by key, not broken.
Keep a copy of your save folder before you replace anything.
"""
import struct, sys

def mmh3(key: bytes, seed: int = 0) -> int:
    """MurmurHash3 x86 32-bit: the game names its save values with it."""
    n = len(key); h = seed; c1, c2 = 0xcc9e2d51, 0x1b873593; nb = n // 4 * 4
    for i in range(0, nb, 4):
        k = struct.unpack_from('<I', key, i)[0]
        k = (k * c1) & 0xffffffff; k = ((k << 15) | (k >> 17)) & 0xffffffff; k = (k * c2) & 0xffffffff
        h ^= k; h = ((h << 13) | (h >> 19)) & 0xffffffff; h = (h * 5 + 0xe6546b64) & 0xffffffff
    k = 0
    for i, b in enumerate(key[nb:]): k |= b << (8 * i)
    if n & 3:
        k = (k * c1) & 0xffffffff; k = ((k << 15) | (k >> 17)) & 0xffffffff; k = (k * c2) & 0xffffffff; h ^= k
    h ^= n; h ^= h >> 16; h = (h * 0x85ebca6b) & 0xffffffff; h ^= h >> 13; h = (h * 0xc2b2ae35) & 0xffffffff; h ^= h >> 16
    return h

ITEMS = """
Armor_Adult_Default_Head Armor_Adult_Gauntlet_Gold Armor_Adult_Gauntlet_Silver Armor_Adult_Goron Armor_Adult_HeavyBoot
Armor_Adult_HoverBoot Armor_Adult_Normal Armor_Adult_Zora Armor_Child_Default_Head Armor_Child_Gauntlet_Goron
Armor_Child_Mask_Amiibo0 Armor_Child_Mask_Amiibo1 Armor_Child_Mask_Bunny Armor_Child_Mask_Gerudo Armor_Child_Mask_Goron
Armor_Child_Mask_Keaton Armor_Child_Mask_Skull Armor_Child_Mask_Spooky Armor_Child_Mask_Truth Armor_Child_Mask_Zora
Armor_GlassTruth Item_AgonyStone Item_AlarmCucco Item_Arrow_Fire Item_Arrow_Ice Item_Arrow_Light Item_Arrow_Normal
Item_Bomb Item_BombBag_Large Item_BombBag_Medium Item_BombBag_Small Item_Bombchu Item_Boomerang Item_Bottle
Item_BrokenSword Item_BulletBag_Large Item_BulletBag_Medium Item_BulletBag_Small Item_ClaimCheck Item_CojiroCucco
Item_DekuNut Item_DekuSeed Item_DekuStick Item_DinFire Item_EyeDrop Item_EyeballFrog Item_FairyBless_DefenseDouble
Item_FairyBless_MP Item_FairyBless_MPDouble Item_FaroreWind Item_FishingRod Item_Hammer Item_Hookshot Item_Longshot
Item_MagicBean Item_Medal_Fire Item_Medal_Forest Item_Medal_Light Item_Medal_Shadow Item_Medal_Spirit Item_Medal_Water
Item_Melody_EponaSong Item_Melody_FireBolero Item_Melody_ForestMinuet Item_Melody_LightPrelude Item_Melody_SariaSong
Item_Melody_ScarecrowSong Item_Melody_ShadowNocturne Item_Melody_SpiritRequiem Item_Melody_StormSong Item_Melody_SunSong
Item_Melody_TimeSong Item_Melody_WaterSerenade Item_Melody_ZeldaLullaby Item_NayruLove Item_NutBag_Large
Item_NutBag_Medium Item_NutBag_Small Item_Ocarina_Fairy Item_Ocarina_Time Item_OddMushroom Item_OddPowder
Item_PoacherSaw Item_PocketCucco Item_PocketEgg Item_Prescription Item_Quiver_Large Item_Quiver_Medium Item_Quiver_Small
Item_Scale_Gold Item_Scale_Silver Item_StickBag_Large Item_StickBag_Medium Item_StickBag_Small Item_Stone_Fire
Item_Stone_Forest Item_Stone_Water Item_Token_Gerudo Item_Token_Gold Item_Wallet_Large Item_Wallet_Medium
Item_Wallet_Small Item_WeirdEgg Item_ZeldaLetter Weapon_Range_Bow Weapon_Range_SlingShot Weapon_Shield_Deku
Weapon_Shield_Hylian Weapon_Shield_Mirror Weapon_Sword_Biggoron Weapon_Sword_Giant Weapon_Sword_Kokiri Weapon_Sword_Master
""".split()

AMMO = {'Item_Arrow_Normal': 50, 'Item_Bomb': 40, 'Item_Bombchu': 50, 'Item_DekuNut': 40, 'Item_DekuStick': 30,
        'Item_DekuSeed': 50, 'Item_MagicBean': 10, 'Item_Token_Gold': 100}

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]; rupees = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    d = bytearray(open(src, 'rb').read())
    if d[:4] != b'\x04\x03\x02\x01':
        sys.exit(f'{src} is not a progress.sav of this game')
    pos = {}
    for o in range(0x20, len(d) - 8, 8):           # the save is (name hash, value) pairs
        pos.setdefault(struct.unpack_from('<I', d, o)[0], o)
    changed, missing = 0, []
    def put(name, value, optional=False):
        nonlocal changed
        o = pos.get(mmh3(name.encode()))
        if o is None:
            if not optional: missing.append(name)
            return
        if struct.unpack_from('<i', d, o + 4)[0] != value:
            struct.pack_into('<i', d, o + 4, value); changed += 1
    for it in ITEMS:
        put('IsGet.' + it, 1)
        put(f'PouchData.{it}.StockNum', AMMO.get(it, 1), optional=True)
    put('IsGet.Item_Bottle_Letter', 1)
    put('PlayerStatus.MaxLife', 80)               # 4 per heart: 80 = 20 hearts
    put('PlayerStatus.Life', 80)
    put('PlayerStatus.CurrentRupee', rupees)
    put('PlayerStatus.MPMax', 480)                # double magic, tested in game (the Great Fairy params say 48: the game scales it)
    put('PlayerStatus.MP', 480)
    put('PlayerStatus.IsDefenseUP', 1)            # double defence (white-edged hearts)

    def put_raw(name, raw):
        nonlocal changed
        o = pos.get(mmh3(name.encode()))
        if o is None: missing.append(name); return
        if struct.unpack_from('<I', d, o + 4)[0] != raw:
            struct.pack_into('<I', d, o + 4, raw); changed += 1
    put_raw('PlayerStatus.LiftGrade', 375060617)                          # Golden Gauntlets
    put_raw('PlayerStatus.DiveDepth', struct.unpack('<I', struct.pack('<f', 9.0))[0])  # Golden Scale

    def put_str(name, value):                     # String64 values: the pair holds an offset to a 64-byte field
        nonlocal changed
        o = pos.get(mmh3(name.encode()))
        if o is None: missing.append(name); return
        off = struct.unpack_from('<I', d, o + 4)[0]
        new = value.encode() + b'\0' * (64 - len(value))
        if bytes(d[off:off + 64]) != new:
            d[off:off + 64] = new; changed += 1
    put_str('PlayerStatus.EquipOcarina', 'Item_Ocarina_Time')   # without an equipped ocarina you cannot play or see the songs
    for key, bag in [('Rupee', 'Item_Wallet_Large'), ('Arrow', 'Item_Quiver_Large'), ('Bomb', 'Item_BombBag_Large'),
                     ('DekuNut', 'Item_NutBag_Large'), ('DekuStick', 'Item_StickBag_Large'), ('DekuSeed', 'Item_BulletBag_Large')]:
        put_str('CurrentExpansionActor_' + key, bag)

    # capacity caps: one struct with a member per key (Rupee, Arrow, Bomb, DekuSeed, DekuNut, DekuStick);
    # the values are the MaxNum of the largest bags. Without them the counter shows 1000/200 and bombs drop to 0.
    def put_hash(h, value, label):
        nonlocal changed
        o = pos.get(h)
        if o is None: missing.append(label); return
        if struct.unpack_from('<i', d, o + 4)[0] != value:
            struct.pack_into('<i', d, o + 4, value); changed += 1
    for h, v, label in [(0xe0010a50, 1000, 'cap Rupee'), (0x418db791, 50, 'cap Arrow'), (0xe753508b, 40, 'cap Bomb'),
                        (0xae8cc742, 50, 'cap DekuSeed'), (0x735b00f7, 40, 'cap DekuNut'), (0x457616b0, 30, 'cap DekuStick')]:
        put_hash(h, v, label)
    dst = src + '.100'
    open(dst, 'wb').write(d)
    print(f'{changed} values changed, written to {dst}')
    if missing:
        print('not in this save (left alone):', ', '.join(missing))

if __name__ == '__main__':
    main()
