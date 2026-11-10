# The Legend of Zelda: Ocarina of Time — cheats & 100% inventory save

**Title ID** `0400486024DEC000` · **version** `v131072` · **main build ID** `E0F3CCFAF50065AE`

🇮🇹 [Italiano più in basso](#italiano) · 📖 [Step-by-step guide / Guida passo passo](GUIDE.md)

I made these for my own copy of the game, which I play on my Mac with [NX2Apple](https://github.com/LNPANDY/NX2Apple). This repository holds **no game files**: only my cheats, my saves and a small script.

| File | What it is |
|---|---|
| `cheats/E0F3CCFAF50065AE.txt` | Three Atmosphère-format cheats: **rupees at 1000**, **infinite health**, **infinite magic** |
| `save/child/` · `save/adult/` | The same full-inventory save, with Link as a child or as an adult |
| `tools/zelda100.py` | The script I used: gives the full inventory to **your** save |
| `tools/cambia_eta.py` · `tools/Cambia età Zelda.command` | Switches Link between **child and adult** in a save (game closed) |
| [`GUIDE.md`](GUIDE.md) | **Step-by-step install guide for NX2Apple** (English and Italian) |

## Cheats

Both cheats only work with build `E0F3CCFAF50065AE`. I tested them on NX2Apple (Mac, Apple M4 Max), **not** on a console. To turn one off, switch it off and **restart the game**.

**Rupees 1000.** The game keeps its values in a data manager, looked up by name hash (MurmurHash3). I hook the function that reads integer values (`main+0x83714c`). Each time it runs, my code looks up `PlayerStatus.CurrentRupee` in the same hash table and writes 1000 into its cell. The game still caps rupees to your wallet (1000 with the biggest one).

**Infinite health / Infinite magic.** Plain data cheats, no code patch. They follow the game data manager's pointer (`[[main+0x4C7E180]]`, then its Int value array at `+0xD8`) and copy, every frame, `PlayerStatus.MaxLife` into `Life` and `PlayerStatus.MPMax` into `MP`, so they fit any heart count and single or double magic. A value's cell is its index in the `Int` list of `GameDataList.Product.110.byml` × 0x28 + 0x1C (Life 963, MaxLife 964, MP 965, MPMax 967). I confirmed the MP cell with nxnative's write watch (`DM_PROBE_WATCH`): the Lens of Truth lowers it by 2 a second through the game's own setter, so this cell is the live value.

**Why there is no age cheat.** The game only applies the age when it loads a save, and my cheats never got the flag into the save. The age is changed in the save file instead, with the script below.

## Age switch (child ↔ adult)

Close the game, then double-click `tools/Cambia età Zelda.command` (or run `python3 tools/cambia_eta.py`). Drag your `0400486024DEC000` save folder into the window when it asks, type the slot number, and reopen the game. The script changes `Sequence_IsChildhood` and the equipped sword and shield (adult: Master Sword + Hylian Shield, child: Kokiri Sword + Deku Shield) in both the save folder and its `.work` copy, after a backup of the slot. Don't switch age while Link is inside a dungeon that only exists for one age.

## Saves — full inventory

- **Weapons:** Kokiri Sword, Master Sword, Biggoron's Sword, Giant's Knife; Deku, Hylian and Mirror Shields; Fairy Bow, Fairy Slingshot, Megaton Hammer
- **Gear:** Goron and Zora Tunics, Iron and Hover Boots, Goron's Bracelet, Silver and Golden Gauntlets (lift grade set), Silver and Golden Scales (dive depth set)
- **Items:** Hookshot, Longshot, Boomerang, Lens of Truth, both ocarinas (**Ocarina of Time equipped**), Magic Beans, Fishing Rod, Fire, Ice and Light Arrows, Din's Fire, Farore's Wind, Nayru's Love, Stone of Agony, Gerudo's Card
- **All 13 songs**, and a Scarecrow's Song (X, Y, X, A, X)
- **Capacities:** largest wallet (**1000/1000 rupees**), quiver (50), bomb bag (40, also bombchus), bullet bag (50), nuts (40), sticks (30), all full
- **20 hearts**, **full double magic**, **double defence**
- **Story items:** the 3 Spiritual Stones, the 6 Medallions, every mask, every trade item, 100 Gold Skulltula tokens

**What it does not do:** it does **not** complete quests or the story. In this game a quest is a chain of steps whose "completed" flags are computed from those steps, so setting them by hand can leave the game stuck. The bottles are empty and the Gold Skulltulas are still out in the world. The save is early in the story: as an adult you may find places and people that only make sense later.

### What I learned about the save (for other editors)

The maxima are **not** derived from the items you own. They are stored on their own, so if you only set `IsGet.*` the game shows `1000/200` and bombs drop to 0:
- current bag per capacity: `CurrentExpansionActor_<Rupee|Arrow|Bomb|DekuNut|DekuStick|DekuSeed>` (String64 actor name)
- caps: a struct with one Int member per key (hashes `0xe0010a50` Rupee, `0x418db791` Arrow, `0xe753508b` Bomb, `0xae8cc742` DekuSeed, `0x735b00f7` DekuNut, `0x457616b0` DekuStick)
- magic: `PlayerStatus.MPMax` / `PlayerStatus.MP` = **480** for double magic (the Great Fairy parameter says 48; with 48 the meter is tiny and Din's Fire fails)
- `PlayerStatus.IsDefenseUP`, `PlayerStatus.LiftGrade`, `PlayerStatus.DiveDepth`, `PlayerStatus.EquipOcarina`
- Scarecrow's Song: UIntArray `0xcc535536`, 8 notes; A = 11, Y = 13, X = 16, 0 = empty

### Make your own save 100%

```
python3 tools/zelda100.py progress.sav          # writes progress.sav.100, the original is left alone
python3 tools/zelda100.py progress.sav 500      # with a custom rupee count
```

---

## Italiano

Ho fatto questi file per la mia copia del gioco, che uso sul Mac con [NX2Apple](https://github.com/LNPANDY/NX2Apple). Qui **non ci sono file del gioco**: solo i miei cheat, i miei salvataggi e un piccolo script. La guida passo passo è in [GUIDE.md](GUIDE.md#guida-passo-passo-per-nx2apple-mac).

**Cheat «Rupie 1000».** Aggancio la funzione con cui il gioco legge i numeri (`main+0x83714c`) e scrivo 1000 nella cella di `PlayerStatus.CurrentRupee`. Il gioco tiene comunque il tetto del borsello (1000 con il più grande).

**Cheat «Vita infinita» e «Magia infinita».** Tengono sempre piene vita e magia, qualunque sia il massimo (cuori, magia singola o doppia). Sono cheat sui dati, senza modifiche al codice: copiano a ogni fotogramma il massimo nel valore attuale.

**Cambio età (bambino ↔ adulto).** Con un cheat non funziona: quando salvi, il gioco riscrive l'età attuale di Link. Per questo l'età si cambia nel salvataggio: chiudi il gioco, fai doppio clic su `tools/Cambia età Zelda.command`, trascina nella finestra la cartella dei salvataggi `0400486024DEC000`, scrivi il numero dello slot e riapri il gioco. Lo script fa prima un backup dello slot e cambia anche spada e scudo equipaggiati. Non farlo mentre Link è dentro un tempio che esiste per una sola età.

I cheat funzionano solo con la build `E0F3CCFAF50065AE`. Li ho provati su NX2Apple (Mac M4 Max), **non** su console. Per spegnerli li disattivi e **riavvii il gioco**.

**Salvataggi** (`save/child` bambino, `save/adult` adulto): tutte le armi e l'equipaggiamento, tutti gli oggetti con l'Ocarina del Tempo equipaggiata, le 13 canzoni e una melodia dello spaventapasseri (X, Y, X, A, X), borsello e borse più grandi pieni (**1000/1000 rupie**), 20 cuori, **magia doppia piena**, difesa doppia, pietre, medaglioni, maschere, oggetti di scambio e 100 gettoni Skulltula. **Non completano le quest né la storia**: i flag "completata" il gioco li calcola dai passaggi della quest. Le bottiglie sono vuote.

**Il tuo salvataggio al 100%:** `python3 tools/zelda100.py progress.sav` crea `progress.sav.100` e lascia intatto l'originale.
