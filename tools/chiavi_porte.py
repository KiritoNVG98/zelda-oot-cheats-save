#!/usr/bin/env python3
"""chiavi_porte.py - opens every locked door of The Legend of Zelda: Ocarina of Time
(Switch 2, 0400486024DEC000): small keys and the boss key in every dungeon.
/ Apre tutte le porte chiuse a chiave: chiavi piccole e chiave del boss in ogni dungeon.

Close the game first. / Chiudi prima il gioco.

    python3 chiavi_porte.py [save folder 0400486024DEC000]

For each dungeon it sets DungeonInfo.<dungeon>.SmallKeyNum to 30 and
DungeonInfo.<dungeon>.IsGetBossKey to true, in both the save folder and its .work
copy, after a backup of the slot. Doors you already opened stay open.
It also opens the Door of Time in the Temple of Time: the quest "DoorOfTime" (Enum 0x378913ca)
goes to Complete, plus Market_Child_TimeTempleDoor_Opened and DoorOfTime_GetStoneCount = 3.
"""
import os, sys, struct, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cambia_eta import mmh3, index, age, find_save

KEYS = 30
DUNGEONS = ['InsideTheDekuTree', 'DodongoCavern', 'InsideJabuJabuBelly', 'ForestTemple', 'FireTemple',
            'WaterTemple', 'ShadowTemple', 'SpiritTemple', 'BottomOfTheWell', 'IceCavern',
            'GerudoTrainingGround', 'GerudoFortress', 'InsideGanonCastle', 'FinalBattleField']

def give_keys(path):
    d = bytearray(open(path, 'rb').read())
    pos = index(d); done = 0
    for n in DUNGEONS:
        for name, val in ((f'DungeonInfo.{n}.SmallKeyNum', KEYS), (f'DungeonInfo.{n}.IsGetBossKey', 1)):
            o = pos.get(mmh3(name.encode()))
            if o is not None:
                struct.pack_into('<I', d, o + 4, val); done += 1
    for h, val in ((mmh3(b'Market_Child_TimeTempleDoor_Opened'), 1), (mmh3(b'DoorOfTime_GetStoneCount'), 3),
                   (0x378913ca, 0x4c0a63f4)):   # quest DoorOfTime -> Complete
        o = pos.get(h)
        if o is not None:
            struct.pack_into('<I', d, o + 4, val)
    return bytes(d), done

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
        data, done = give_keys(p)
        backup = os.path.join(parent, 'Backup salvataggi Zelda', f'{stamp} prima delle chiavi {s}')
        k = 2
        while os.path.exists(backup):
            backup = os.path.join(parent, 'Backup salvataggi Zelda', f'{stamp} prima delle chiavi {s} ({k})'); k += 1
        for src, tag in ((os.path.join(save, s), 'save'), (os.path.join(work, s), 'work')):
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(backup, tag))
        for folder in (save, work):
            dst = os.path.join(folder, s, 'progress.sav')
            if os.path.isdir(os.path.dirname(dst)):
                open(dst, 'wb').write(data)
        print(f'Slot {int(s[5:]) + 1}: {KEYS} chiavi piccole e chiave del boss in {done // 2} dungeon, Porta del Tempo aperta. Backup: {backup}')
    print('\nRiapri il gioco e carica lo slot. / Reopen the game and load the slot.')

if __name__ == '__main__':
    main()
