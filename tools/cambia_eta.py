#!/usr/bin/env python3
"""cambia_eta.py - switches Link between child and adult in a The Legend of Zelda:
Ocarina of Time (Switch 2, 0400486024DEC000) save. / Cambia Link da bambino ad adulto
e viceversa in un salvataggio.

Close the game first. / Chiudi prima il gioco.

    python3 cambia_eta.py [save folder 0400486024DEC000]

It changes Sequence_IsChildhood and the equipped sword and shield
(adult: Master Sword + Hylian Shield, child: Kokiri Sword + Deku Shield),
in both the save folder and its .work copy, after a backup of the slot.
"""
import os, sys, struct, shutil, datetime

TITLE = '0400486024DEC000'

def mmh3(key: bytes, seed: int = 0) -> int:
    c1, c2 = 0xcc9e2d51, 0x1b873593
    h = seed; n = len(key) & ~3
    for i in range(0, n, 4):
        k = int.from_bytes(key[i:i + 4], 'little')
        k = (k * c1) & 0xffffffff; k = ((k << 15) | (k >> 17)) & 0xffffffff; k = (k * c2) & 0xffffffff
        h ^= k; h = ((h << 13) | (h >> 19)) & 0xffffffff; h = (h * 5 + 0xe6546b64) & 0xffffffff
    t = key[n:]; k = 0
    if len(t) == 3: k ^= t[2] << 16
    if len(t) >= 2: k ^= t[1] << 8
    if len(t) >= 1:
        k ^= t[0]; k = (k * c1) & 0xffffffff; k = ((k << 15) | (k >> 17)) & 0xffffffff; k = (k * c2) & 0xffffffff; h ^= k
    h ^= len(key); h ^= h >> 16; h = (h * 0x85ebca6b) & 0xffffffff; h ^= h >> 13; h = (h * 0xc2b2ae35) & 0xffffffff
    return h ^ (h >> 16)

CHILD = mmh3(b'Sequence_IsChildhood')
WEAPON = mmh3(b'PlayerStatus.EquipWeapon')
SHIELD = mmh3(b'PlayerStatus.EquipShield')
GEAR = {0: ('Weapon_Sword_Master', 'Weapon_Shield_Hylian'),   # adult
        1: ('Weapon_Sword_Kokiri', 'Weapon_Shield_Deku')}     # child

def index(d):
    pos = {}
    for o in range(0x20, len(d) - 8, 8):
        pos.setdefault(struct.unpack_from('<I', d, o)[0], o)
    return pos

def age(path):
    d = open(path, 'rb').read()
    if d[:4] != b'\x04\x03\x02\x01':
        return None
    o = index(d).get(CHILD)
    return None if o is None else struct.unpack_from('<I', d, o + 4)[0]

def set_age(path, child):
    d = bytearray(open(path, 'rb').read())
    pos = index(d)
    struct.pack_into('<I', d, pos[CHILD] + 4, child)
    for h, name in zip((WEAPON, SHIELD), GEAR[child]):
        o = pos.get(h)
        if o is None:
            continue
        off = struct.unpack_from('<I', d, o + 4)[0]
        d[off:off + 64] = name.encode() + b'\0' * (64 - len(name))
    return bytes(d)

def find_save():
    if len(sys.argv) > 1:
        return os.path.expanduser(sys.argv[1].strip().strip('\'"'))
    here = os.path.dirname(os.path.abspath(__file__))
    for up in ('..', '../..', '../../..'):
        p = os.path.normpath(os.path.join(here, up, 'save', TITLE))
        if os.path.isdir(p):
            return p
    p = input(f'Trascina qui la cartella {TITLE} dei salvataggi e premi Invio / '
              f'Drag the {TITLE} save folder here and press Enter:\n> ')
    return os.path.expanduser(p.strip().strip('\'"').replace('\\ ', ' '))

def main():
    save = find_save().rstrip('/')
    work = save + '.work'
    if not os.path.isdir(save):
        sys.exit(f'Cartella non trovata / folder not found: {save}')
    slots = []
    for s in sorted(os.listdir(save)):
        p = os.path.join(save, s, 'progress.sav')
        if s.startswith('slot_') and os.path.isfile(p):
            a = age(p)
            if a is not None:
                slots.append((s, p, a))
    if not slots:
        sys.exit('Nessun salvataggio trovato / no saves found.')
    print('\nChiudi il gioco prima di continuare. / Close the game first.\n')
    for s, p, a in slots:
        n = int(s[5:]) + 1
        print(f'  Slot {n}: Link {"bambino / child" if a else "adulto / adult"}')
    choice = input('\nNumero dello slot da cambiare / slot number to switch: ').strip()
    match = [x for x in slots if choice.isdigit() and int(x[0][5:]) + 1 == int(choice)]
    if not match:
        sys.exit('Slot non valido / invalid slot.')
    s, p, a = match[0]
    new = 0 if a else 1
    data = set_age(p, new)

    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    parent = os.path.dirname(os.path.dirname(save))
    backup = os.path.join(parent, 'Backup salvataggi Zelda', f'{stamp} prima del cambio eta {s}')
    k = 2
    while os.path.exists(backup):
        backup = os.path.join(parent, 'Backup salvataggi Zelda', f'{stamp} prima del cambio eta {s} ({k})'); k += 1
    for src, tag in ((os.path.join(save, s), 'save'), (os.path.join(work, s), 'work')):
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(backup, tag))
    for folder in (save, work):
        dst = os.path.join(folder, s, 'progress.sav')
        if os.path.isdir(os.path.dirname(dst)):
            open(dst, 'wb').write(data)
    print(f'\nFatto: slot {int(s[5:]) + 1} ora e\' Link {"bambino" if new else "adulto"}. / '
          f'Done: Link is now {"a child" if new else "an adult"}.')
    print(f'Backup: {backup}')
    print('Riapri il gioco e carica lo slot. / Reopen the game and load the slot.')

if __name__ == '__main__':
    main()
