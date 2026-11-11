# The Legend of Zelda: Ocarina of Time — cheats & 100% inventory save

**Title ID** `0400486024DEC000` · **version** `v131072` · **main build ID** `E0F3CCFAF50065AE`

🇮🇹 [Italiano più in basso](#italiano) · 📖 [Step-by-step guide / Guida passo passo](GUIDE.md)

I made these for my own copy of the game, which I play on my Mac with [NX2Apple](https://github.com/LNPANDY/NX2Apple). This repository holds **no game files**: only my cheats, my saves and a small script.

| File | What it is |
|---|---|
| `cheats/E0F3CCFAF50065AE.txt` | Four Atmosphère-format cheats: **rupees at 1000**, **infinite health**, **infinite magic**, **jump without the 5 m cap** |
| `save/child/` · `save/adult/` | The same full-inventory save, with Link as a child or as an adult |
| `tools/zelda100.py` | The script I used: gives the full inventory to **your** save |
| `tools/cambia_eta.py` · `tools/Cambia età Zelda.command` | Switches Link between **child and adult** in a save (game closed) |
| `tools/salto_alto.py` · `tools/Salto alto Zelda.command` | **High jump** mod: builds it from your own game files and turns it on (game closed) |
| [`GUIDE.md`](GUIDE.md) | **Step-by-step install guide for NX2Apple** (English and Italian) |

## Cheats

The cheats only work with build `E0F3CCFAF50065AE`. I tested them on NX2Apple (Mac, Apple M4 Max), **not** on a console. To turn one off, switch it off and **restart the game**.

**Rupees 1000.** The game keeps its values in a data manager, looked up by name hash (MurmurHash3). I hook the function that reads integer values (`main+0x83714c`). Each time it runs, my code looks up `PlayerStatus.CurrentRupee` in the same hash table and writes 1000 into its cell. The game still caps rupees to your wallet (1000 with the biggest one).

**Infinite health / Infinite magic.** Plain data cheats, no code patch. They follow the game data manager's pointer (`[[main+0x4C7E180]]`, then its Int value array at `+0xD8`) and copy, every frame, `PlayerStatus.MaxLife` into `Life` and `PlayerStatus.MPMax` into `MP`, so they fit any heart count and single or double magic. A value's cell is its index in the `Int` list of `GameDataList.Product.110.byml` × 0x28 + 0x1C (Life 963, MaxLife 964, MP 965, MPMax 967). I confirmed the MP cell with nxnative's write watch (`DM_PROBE_WATCH`): the Lens of Truth lowers it by 2 a second through the game's own setter, so this cell is the live value.

**Why there is no age cheat.** The game only applies the age when it loads a save, and my cheats never got the flag into the save. The age is changed in the save file instead, with the script below.

**Jump without 5 m cap.** The jump code (`main+0x93b100`) reads `JumpHeight` from the player parameters and clamps it to 5 m (`fmov s0, #5.0` · `fcmp` · `fcsel` at `main+0x93b12c..0x93b140`). The cheat replaces the `fcsel` with `fmov s0, s8`, so the height is used as it is. On its own it changes nothing: the normal jump is 0.7 m. It is meant for the high jump mod below. Turning it off in the menu does not put the cap back until you restart the game.

## High jump (mod)

`tools/salto_alto.py` makes Link jump N times higher. It reads **your** game files from the NX2Apple app (`Contents/Resources/romfs.img`), so this repository ships none. In `Pack/Actor/Player_Base`, `Player_Child` and `Player_Adult.pack.zs` it changes:

- `PlayerGameParam`: `JumpHeight` (0.7 m) × N, and `LargeLandHeight` (5 m) = N, so landing from your own jump is not a heavy landing;
- `CharacterControllerParam`: `BounceSuppressor.ThresholdVelY` 15 → 200 m/s, because the physics cuts any take-off faster than 15 m/s (about 20 m of jump).

The changed packs go to a `Salto alto Zelda/romfs` folder next to the app, and the script points nxnative's `DM_ROMFS_OVERLAY` to it (in the app's `Contents/Resources/dm/env.txt`). Above ×7 you also need the **Jump without 5 m cap** cheat. I play with ×35 (24.5 m). Run it again with another number to change it, or with `off` to turn it off. Needs `pip3 install zstandard` (the `.command` installs it).

## Age switch (child ↔ adult)

Close the game, then double-click `tools/Cambia età Zelda.command` (or run `python3 tools/cambia_eta.py`). Drag your `0400486024DEC000` save folder into the window when it asks, type the slot number, and reopen the game. The script changes `Sequence_IsChildhood` and the equipped sword and shield (adult: Master Sword + Hylian Shield, child: Kokiri Sword + Deku Shield) in both the save folder and its `.work` copy, after a backup of the slot. Don't switch age while Link is inside a dungeon that only exists for one age.

## Saves — full inventory

- **Weapons:** Kokiri Sword, Master Sword, Biggoron's Sword, Giant's Knife; Deku, Hylian and Mirror Shields; Fairy Bow, Fairy Slingshot, Megaton Hammer
- **Gear:** Goron and Zora Tunics, Iron and Hover Boots, Goron's Bracelet, Silver and Golden Gauntlets (lift grade set), Silver and Golden Scales (dive depth set)
- **Items:** Hookshot, Longshot, Boomerang, Lens of Truth, both ocarinas (**Ocarina of Time equipped**), Magic Beans, Fishing Rod, Fire, Ice and Light Arrows, Din's Fire, Farore's Wind, Nayru's Love, Stone of Agony, Gerudo's Card
- **All 13 songs**, and a Scarecrow's Song (X, Y, X, A, X)
- **Capacities:** largest wallet (**1000/1000 rupees**), quiver (50), bomb bag (40, also bombchus), bullet bag (50), nuts (40), sticks (30), all full
- **20 hearts**, **full double magic**, **double defence**
- **Story items:** the 3 Spiritual Stones, the 6 Medallions, every mask (the two amiibo masks too), every trade item, 100 Gold Skulltula tokens

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

## amiibo masks — what they do (from the game files)

Nintendo has only said that the Young Link and Young Zelda amiibo (out in 2027) unlock "retro" masks. I looked inside the game's own files (version 1.0.2, build `E0F3CCFAF50065AE`), and this is what they do. Things may change with an update.

- **Two masks, already in the game:** `Armor_Child_Mask_Amiibo0` — **Fairy-Kid Mask** in the English text, *Maschera coraggiosa* in Italian (Young Link) — and `Armor_Child_Mask_Amiibo1` — **Princess Mask**, *Maschera regale* (Young Zelda). They are the 1998 Nintendo 64 faces. My saves and `zelda100.py` include both, because they give every item the game lists.
- **No gameplay effect.** Their parameters only place the mask on the face (UV, hand position): no bonus, no doors, no hidden items.
- **People react.** About 150 of the game's event flows have a branch for these masks: Kokiri, Gorons, Zoras, Hylians and Castle Town guards, Malon, Talon, Ingo, Dampé, King Zora, Ruto, Saria, Mido, Skull Kid, Kaepora Gaebora, the Sages, Princess Zelda herself, even the Poes. When you get a mask the game tells you to talk to people while wearing it.
- **Scanning** (`AmiiboSetting` in the RomFS): the two new figures drop only their mask, with no daily limit. Older Zelda amiibo drop 3 to 5 random items (hearts are the most likely, then magic jars, then bombs, seeds, arrows, sticks, nuts and bombchus), once a day. Any other amiibo is "not supported". amiibo work after the Great Deku Tree, and can be turned off in the options.

---

## Italiano

Ho fatto questi file per la mia copia del gioco, che uso sul Mac con [NX2Apple](https://github.com/LNPANDY/NX2Apple). Qui **non ci sono file del gioco**: solo i miei cheat, i miei salvataggi e un piccolo script. La guida passo passo è in [GUIDE.md](GUIDE.md#guida-passo-passo-per-nx2apple-mac).

**Cheat «Rupie 1000».** Aggancio la funzione con cui il gioco legge i numeri (`main+0x83714c`) e scrivo 1000 nella cella di `PlayerStatus.CurrentRupee`. Il gioco tiene comunque il tetto del borsello (1000 con il più grande).

**Cheat «Vita infinita» e «Magia infinita».** Tengono sempre piene vita e magia, qualunque sia il massimo (cuori, magia singola o doppia). Sono cheat sui dati, senza modifiche al codice: copiano a ogni fotogramma il massimo nel valore attuale.

**Cheat «Salto senza limite» e mod «Salto alto».** Il gioco blocca il salto a 5 metri nel codice: il cheat toglie il blocco. La mod (`tools/Salto alto Zelda.command`) fa saltare Link N volte più in alto (io uso ×35, circa 24,5 m): la crea dai file del **tuo** gioco, dentro l'app di NX2Apple, e la accende. Chiudi il gioco, fai doppio clic, trascina l'app di Zelda nella finestra e scrivi il numero (oppure `off` per spegnerla). Sopra ×7 serve anche il cheat acceso.

**Cambio età (bambino ↔ adulto).** Con un cheat non funziona: quando salvi, il gioco riscrive l'età attuale di Link. Per questo l'età si cambia nel salvataggio: chiudi il gioco, fai doppio clic su `tools/Cambia età Zelda.command`, trascina nella finestra la cartella dei salvataggi `0400486024DEC000`, scrivi il numero dello slot e riapri il gioco. Lo script fa prima un backup dello slot e cambia anche spada e scudo equipaggiati. Non farlo mentre Link è dentro un tempio che esiste per una sola età.

I cheat funzionano solo con la build `E0F3CCFAF50065AE`. Li ho provati su NX2Apple (Mac M4 Max), **non** su console. Per spegnerli li disattivi e **riavvii il gioco**.

**Salvataggi** (`save/child` bambino, `save/adult` adulto): tutte le armi e l'equipaggiamento, tutti gli oggetti con l'Ocarina del Tempo equipaggiata, le 13 canzoni e una melodia dello spaventapasseri (X, Y, X, A, X), borsello e borse più grandi pieni (**1000/1000 rupie**), 20 cuori, **magia doppia piena**, difesa doppia, pietre, medaglioni, maschere, oggetti di scambio e 100 gettoni Skulltula. **Non completano le quest né la storia**: i flag "completata" il gioco li calcola dai passaggi della quest. Le bottiglie sono vuote.

**Il tuo salvataggio al 100%:** `python3 tools/zelda100.py progress.sav` crea `progress.sav.100` e lascia intatto l'originale.

**Le maschere degli amiibo (dai file del gioco).** Nintendo ha detto solo che gli amiibo di Link e Zelda bambini (in uscita nel 2027) sbloccano due maschere «retrò». Ho guardato nei file del gioco (versione 1.0.2): le maschere sono già dentro e si chiamano **Maschera coraggiosa** (Link) e **Maschera regale** (Zelda), con i volti del Nintendo 64. I miei salvataggi e `zelda100.py` le includono. **Non hanno effetti sul gioco**: niente bonus né porte. Però **i personaggi reagiscono**: circa 150 dialoghi hanno una variante per queste maschere (Kokiri, Goron, Zora, abitanti e guardie del castello, Malon, Talon, Ingo, Dampé, Re Zora, Ruto, Saria, Mido, Skull Kid, Kaepora, i Saggi, Zelda stessa e perfino i Poe). Gli amiibo nuovi fanno cadere solo la loro maschera, senza limite giornaliero; quelli di Zelda già usciti fanno cadere 3-5 oggetti a caso una volta al giorno (soprattutto cuori, poi ampolle di magia, bombe, semi, frecce, bastoni, noci e bombchu); gli altri amiibo non sono supportati.
