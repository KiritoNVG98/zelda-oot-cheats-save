#!/usr/bin/env python3
"""completa_tutto.py - completes every main and side quest of The Legend of Zelda:
Ocarina of Time (Switch 2, 0400486024DEC000), except the final battle with Ganon.
/ Completa tutte le missioni principali e secondarie, tranne la battaglia finale con Ganon.

Close the game first. / Chiudi prima il gioco.

    python3 completa_tutto.py [save folder 0400486024DEC000]

Each quest is an Enum named Step_<quest> whose last value is Complete. This script sets 44
of them to Complete (Defeat_Ganon is left as it is, so the save does not jump past the
ending), gives every dungeon its map and compass, and runs chiavi_porte.py's changes (keys,
boss keys, Door of Time). It writes both the save folder and its .work copy, after a backup.
"""
import os, sys, struct, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cambia_eta import mmh3, index, age, find_save
from chiavi_porte import give_keys, DUNGEONS

COMPLETE = mmh3(b'Complete')
QUESTS = [   # Step_<name> Enums ending in Complete; the unnamed ones are mini-games and side events
    0x003694b5,  # AllSage
    0x378913ca,  # DoorOfTime
    0x8c5e9f84,  # GatheringTokenGold
    0x92431c55,  # Get_Epona
    0x1002b466,  # Get_StoneOfFire
    0x7d776b61,  # Get_StoneOfForest
    0x5bca02a6,  # Get_StoneOfWater
    0xdb89c1a9,  # Goto_HyruleCastle
    0x3372689b,  # Meet_DekuTree
    0x682d1169,  # Meet_GreatFairy
    0xa4ed3902,  # MiniGame_Diving
    0xf6e99816,  # MiniGame_Fishing
    0xa3404532,  # MiniGame_HitTarget
    0xeea87aec,  # SageOfFire
    0xa9632cca,  # SageOfForest
    0x7a91dbd5,  # SageOfShadow
    0x19189e9d,  # SageOfSpirit
    0x560a64af,  # SageOfWater
    0xbe19d91a,  # SubEvent_AllBossBattle
    0x93e84ee3,  # SubEvent_FindRichard
    0x110f26e4,  # SubEvent_GetFireArrow
    0xf7176a52,  # SubEvent_GetIceArrow
    0x9472302b,  # SubEvent_GetScarecrow
    0x7a5b9537,  # SubEvent_GetStormSong
    0x26a2e01c,  # SubEvent_GetSwordBigGoron
    0x6e9b2539,  # SubEvent_GhostShop
    0xea010310,  # SubEvent_MaskSalesman
    0xf6eb33a1,  # SubEvent_RunningRace
    0x1193a73e, 0x147138e3, 0x37a4567e, 0x3e7d10c0, 0x44063c4e, 0x4661f050, 0x474f4ca5, 0x4969f026,
    0x4dd52013, 0x55bfddfa, 0x606c3207, 0x78a93b78, 0x7a6d0096, 0x916e55c8, 0xd601ee20, 0xe73daf62,
]

def complete(data):
    d = bytearray(data); pos = index(d); n = 0
    for h in QUESTS:
        o = pos.get(h)
        if o is not None:
            struct.pack_into('<I', d, o + 4, COMPLETE); n += 1
    for dg in DUNGEONS:
        for f in ('IsGetMap', 'IsGetCompass'):
            o = pos.get(mmh3(f'DungeonInfo.{dg}.{f}'.encode()))
            if o is not None:
                struct.pack_into('<I', d, o + 4, 1)
    return bytes(d), n

def main():
    save = find_save().rstrip('/')
    work = save + '.work'
    if not os.path.isdir(save):
        sys.exit(f'Cartella non trovata / folder not found: {save}')
    slots = [(s, os.path.join(save, s, 'progress.sav')) for s in sorted(os.listdir(save))
             if s.startswith('slot_') and os.path.isfile(os.path.join(save, s, 'progress.sav'))
             and age(os.path.join(save, s, 'progress.sav')) is not None]
    if not slots:
        sys.exit('Nessun salvataggio trovato / no saves found.')
    print('\nChiudi il gioco prima di continuare. / Close the game first.\n')
    print('  Slot: ' + ', '.join(str(int(s[5:]) + 1) for s, p in slots))
    choice = input('\nNumero dello slot (oppure T per tutti) / slot number (or A for all): ').strip().lower()
    pick = slots if choice in ('t', 'a', 'tutti', 'all') else [x for x in slots if choice.isdigit() and int(x[0][5:]) + 1 == int(choice)]
    if not pick:
        sys.exit('Slot non valido / invalid slot.')
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    parent = os.path.dirname(os.path.dirname(save))
    for s, p in pick:
        data, _ = give_keys(p)
        data, n = complete(data)
        backup = os.path.join(parent, 'Backup salvataggi Zelda', f'{stamp} prima del 100 {s}')
        k = 2
        while os.path.exists(backup):
            backup = os.path.join(parent, 'Backup salvataggi Zelda', f'{stamp} prima del 100 {s} ({k})'); k += 1
        for src, tag in ((os.path.join(save, s), 'save'), (os.path.join(work, s), 'work')):
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(backup, tag))
        for folder in (save, work):
            dst = os.path.join(folder, s, 'progress.sav')
            if os.path.isdir(os.path.dirname(dst)):
                open(dst, 'wb').write(data)
        print(f'Slot {int(s[5:]) + 1}: {n} missioni completate, mappe, bussole, chiavi e Porta del Tempo. Backup: {backup}')
    print('\nRiapri il gioco e carica lo slot. / Reopen the game and load the slot.')

if __name__ == '__main__':
    main()
