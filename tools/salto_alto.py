#!/usr/bin/env python3
# High jump mod for Zelda: Ocarina of Time (Switch 2, 0400486024DEC000) on NX2Apple / nxnative.
# Builds a RomFS overlay from YOUR game files (no game file is shipped in this repository) and turns it on in the app.
#
#   python3 salto_alto.py <Zelda .app> <multiplier>    e.g. 35 = Link jumps 35 times higher (0.7 m -> 24.5 m)
#   python3 salto_alto.py <Zelda .app> off             turns the mod off
#
# What it changes, in Pack/Actor/Player_Base/Child/Adult.pack.zs (all three hold the same parameters):
#   Player/PlayerGameParam/Player.game__player__PlayerGameParam.bgyml   JumpHeight x multiplier, LargeLandHeight = multiplier (no heavy landing after your own jump)
#   Phive/CharacterControllerParam/Player.phive__CharacterControllerParam.bgyml   BounceSuppressor.ThresholdVelY 15 -> 200 (it cuts fast take-offs)
# The game also caps the jump at 5 m in code (main+0x93b12c..0x93b140): above x7 you need the cheat "Jump without 5 m cap / Salto senza limite".
# The overlay goes to <the .app's folder>/Salto alto Zelda/romfs, and DM_ROMFS_OVERLAY in the app's Contents/Resources/dm/env.txt points to it.
# Needs: pip3 install zstandard
import struct, sys
from pathlib import Path

try:
    import zstandard as zstd
except ImportError:
    sys.exit('Serve il modulo zstandard: apri il Terminale e scrivi  pip3 install zstandard')

PACKS = ['Pack/Actor/Player_Base.pack.zs', 'Pack/Actor/Player_Child.pack.zs', 'Pack/Actor/Player_Adult.pack.zs']
PARAM = 'Player/PlayerGameParam/Player.game__player__PlayerGameParam.bgyml'
CCT = 'Phive/CharacterControllerParam/Player.phive__CharacterControllerParam.bgyml'


class RomFS:   # the app's romfs.img (DMROMFS1: 32-byte header, data, index of 24-byte entries, name pool) or an extracted RomFS folder
    def __init__(self, res):
        self.img = res / 'romfs.img'; self.dir = res / 'romfs'; self.idx = None
        if self.img.exists():
            with open(self.img, 'rb') as f:
                magic, ioff, isz, n = struct.unpack('<8sQQQ', f.read(32))
                if magic != b'DMROMFS1': sys.exit('romfs.img non riconosciuto')
                f.seek(ioff); raw = f.read(isz)
            ent = [struct.unpack_from('<QQIHBB', raw, k * 24) for k in range(n)]; pool = raw[n * 24:]
            self.idx, todo = {}, [(0, '')]
            while todo:
                k, path = todo.pop(); a, b, no, nl, t, _ = ent[k]
                if t == 0: todo.extend((c, (path + '/' if path else '') + pool[ent[c][2]:ent[c][2] + ent[c][3]].decode()) for c in range(a, a + b))
                else: self.idx[path] = (a, b)
        elif not self.dir.is_dir(): sys.exit('Non trovo i file del gioco dentro l\'app (romfs.img o romfs/)')

    def read(self, p):
        if self.idx is None: return (self.dir / p).read_bytes()
        a, b = self.idx[p]
        with open(self.img, 'rb') as f: f.seek(a); return f.read(b)


def sarc(b):   # {name: (start, end)} of a SARC archive's files
    hl = struct.unpack_from('<H', b, 4)[0]; doff = struct.unpack_from('<I', b, 12)[0]
    n = struct.unpack_from('<H', b, hl + 6)[0]; names = hl + 12 + n * 16 + 8; out = {}
    for i in range(n):
        h, attr, s, e = struct.unpack_from('<IIII', b, hl + 12 + i * 16)
        no = names + (attr & 0xffff) * 4; out[b[no:b.index(b'\0', no)].decode()] = (doff + s, doff + e)
    return out


def byml_floats(b):   # {path: offset of the float} of a BYML's float values (dictionaries and arrays)
    koff, soff, roff = struct.unpack_from('<III', b, 4)
    def table(o):
        n = struct.unpack_from('<I', b, o)[0] >> 8; offs = struct.unpack_from('<%dI' % (n + 1), b, o + 4)
        return [b[o + offs[i]:b.index(b'\0', o + offs[i])].decode() for i in range(n)]
    keys = table(koff); out = {}
    def node(o, path):
        t = b[o]; n = struct.unpack_from('<I', b, o)[0] >> 8
        if t == 0xc1:
            for i in range(n):
                e = o + 4 + i * 8; k = struct.unpack_from('<I', b, e)[0] & 0xffffff; tt = b[e + 3]; v = struct.unpack_from('<I', b, e + 4)[0]
                p = path + '/' + keys[k]
                if tt == 0xd2: out[p] = e + 4
                elif tt in (0xc0, 0xc1): node(v, p)
    node(roff, '')
    return out


def main():
    if len(sys.argv) != 3: sys.exit(__doc__ or 'uso: salto_alto.py <app di Zelda> <moltiplicatore | off>')
    app = Path(sys.argv[1].strip().strip("'\"")).expanduser()
    res = app / 'Contents/Resources'; env = res / 'dm/env.txt'
    if not env.parent.is_dir(): sys.exit('Questa non sembra l\'app di Zelda fatta con NX2Apple: ' + str(app))
    lines = [l for l in (env.read_text().splitlines() if env.exists() else []) if not l.startswith('DM_ROMFS_OVERLAY=')]
    if sys.argv[2].lower() == 'off':
        env.write_text(''.join(l + '\n' for l in lines)); print('Salto alto DISATTIVATO.'); return
    mult = float(sys.argv[2].replace(',', '.'))
    if not 0 < mult <= 1000: sys.exit('Moltiplicatore fuori misura: usa un numero tra 1 e 1000')
    rom = RomFS(res); out = app.parent / 'Salto alto Zelda' / 'romfs'
    raw = zstd.ZstdDecompressor().decompress(rom.read('Pack/ZsDic.pack.zs'), max_output_size=1 << 26); files = sarc(raw)
    dic = zstd.ZstdCompressionDict(raw[slice(*files['pack.zsdic'])])
    for pk in PACKS:
        dec = bytearray(zstd.ZstdDecompressor(dict_data=dic).decompress(rom.read(pk), max_output_size=1 << 28)); f = sarc(bytes(dec))
        s, e = f[PARAM]; fl = byml_floats(bytes(dec[s:e]))
        jh = s + fl['/JumpHeight']; base = struct.unpack_from('<f', dec, jh)[0]
        struct.pack_into('<f', dec, jh, base * mult)
        struct.pack_into('<f', dec, s + fl['/LargeLandHeight'], max(5.0, mult))
        s, e = f[CCT]; struct.pack_into('<f', dec, s + byml_floats(bytes(dec[s:e]))['/UpdateComponentParam/BounceSuppressor/ThresholdVelY'], 200.0)
        dst = out / pk; dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(zstd.ZstdCompressor(level=19, dict_data=dic).compress(bytes(dec)))
        print(f'{pk}: salto {base:.2f} m -> {base * mult:.2f} m')
    env.write_text(''.join(l + '\n' for l in lines + ['DM_ROMFS_OVERLAY=' + str(out.resolve())]))
    print(f'Salto alto x{mult:g} ATTIVO ({out}). Riavvia il gioco.')
    if mult > 7: print('Sopra x7 serve anche il cheat «Jump without 5 m cap / Salto senza limite».')


if __name__ == '__main__':
    main()
