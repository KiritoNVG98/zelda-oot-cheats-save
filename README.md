# The Legend of Zelda: Ocarina of Time — cheats & 100% inventory save

**Title ID** `0400486024DEC000` · **version** `v131072` · **main build ID** `E0F3CCFAF50065AE`

🇮🇹 [Italiano più in basso](#italiano)

I made these for my own copy of the game, which I play on my Mac with [NX2Apple](https://github.com/LNPANDY/NX2Apple). This repository holds **no game files**: only my cheat, my save and a small script.

| File | What it is |
|---|---|
| `cheats/E0F3CCFAF50065AE.txt` | Atmosphère-format cheat: rupees always at 1000 |
| `save/slot_02/progress.sav` + `caption.sav` | A save with the full inventory (see below) |
| `tools/zelda100.py` | The script I used: gives the full inventory to **your** save |
| [`GUIDE.md`](GUIDE.md) | **Step-by-step install guide for NX2Apple** (English and Italian) |

## Cheat — Rupees 1000

The game keeps its values in a data manager, looked up by name hash (MurmurHash3). I hook the function that reads integer values (`main+0x83714c`). Every time it runs, my code looks up `PlayerStatus.CurrentRupee` in the same hash table, the way the game does, and writes 1000 into its cell. The game then carries on as before. The code sits in six empty padding gaps of `main` and is chained by branches.

- The game still caps rupees to your wallet: with the biggest wallet the cap is 1000.
- To turn it off, switch it off and **restart the game** (the patched instruction stays in memory until then).
- I tested it on NX2Apple (Mac, Apple M4 Max). I have **not** tested it on a console.

**Install (NX2Apple):** copy the file to
`~/Library/Application Support/nxnative/0400486024DEC000/cheats/E0F3CCFAF50065AE.txt`,
start the game and turn the cheat on from the Cheats menu.

**Install (Atmosphère):** `/atmosphere/contents/0400486024DEC000/cheats/E0F3CCFAF50065AE.txt`.

The cheat only works with build ID `E0F3CCFAF50065AE`. Another game version needs new offsets.

## Save — full inventory

- **Weapons:** Kokiri Sword, Master Sword, Biggoron's Sword, Giant's Knife; Deku, Hylian and Mirror Shields; Fairy Bow, Fairy Slingshot, Megaton Hammer
- **Gear:** Goron and Zora Tunics, Iron and Hover Boots, Goron's Bracelet, Silver and Golden Gauntlets, Silver and Golden Scales
- **Items:** Hookshot, Longshot, Boomerang, Lens of Truth, both ocarinas, Magic Beans, Fishing Rod, Fire, Ice and Light Arrows, Din's Fire, Farore's Wind, Nayru's Love, Stone of Agony, Gerudo's Card
- **All 13 songs**
- **Upgrades:** largest wallet (**1000 rupees**), quiver, bomb bag, bullet bag, nut and stick capacity; arrows 50, bombs 40, bombchus 50, nuts 40, sticks 30, seeds 50
- **20 hearts**, double magic, double defence
- **Story items:** the 3 Spiritual Stones, the 6 Medallions, every mask, every trade item, 100 Gold Skulltula tokens

**What it does not do:** it does **not** complete quests or the story. In this game a quest is a chain of steps, and its "completed" flags are computed from those steps, so they cannot be set by hand without risking a stuck game. The bottles are empty, and the Gold Skulltulas are still out in the world (only the token count is 100).

**Use it:** the save goes in place of a slot of yours. **Copy your whole save folder first.** On NX2Apple the slots are in `Switch/save/0400486024DEC000/slot_XX/` (`slot_01` = slot 2 in the game). If there is a `0400486024DEC000.work` folder next to it, copy the file there too.

### Make your own save 100%

```
python3 tools/zelda100.py progress.sav          # writes progress.sav.100, the original is left alone
python3 tools/zelda100.py progress.sav 500      # with a custom rupee count
```

The script only changes values that are already in the save, so the file keeps its size.

---

## Italiano

📖 **Guida passo passo per NX2Apple: [GUIDE.md](GUIDE.md#guida-passo-passo-per-nx2apple-mac)**

Ho fatto questi file per la mia copia del gioco, che uso sul Mac con [NX2Apple](https://github.com/LNPANDY/NX2Apple). Qui **non ci sono file del gioco**: solo il mio cheat, il mio salvataggio e un piccolo script.

**Cheat «Rupie 1000».** Il gioco tiene i suoi valori in un gestore dei dati, cercandoli per hash del nome (MurmurHash3). Ho agganciato la funzione che legge i valori interi (`main+0x83714c`). Ogni volta che passa di lì, il mio codice cerca `PlayerStatus.CurrentRupee` nella stessa tabella del gioco e scrive 1000 nella sua cella. Il gioco ha comunque il tetto del borsello: con quello più grande arriva a 1000. Per spegnerlo lo disattivi e **riavvii il gioco**. L'ho provato su NX2Apple (Mac M4 Max), **non** su console. Funziona solo con la build `E0F3CCFAF50065AE`.

- NX2Apple: `~/Library/Application Support/nxnative/0400486024DEC000/cheats/E0F3CCFAF50065AE.txt`, poi lo accendi dal menu Cheat.
- Atmosphère: `/atmosphere/contents/0400486024DEC000/cheats/E0F3CCFAF50065AE.txt`.

**Salvataggio.** Ha tutte le armi, l'equipaggiamento, gli oggetti, le 13 canzoni, i potenziamenti al massimo (1000 rupie), 20 cuori, magia e difesa doppie, le pietre, i medaglioni, tutte le maschere e gli oggetti di scambio, e 100 gettoni Skulltula. **Non completa le quest né la storia**: i flag "completata" il gioco li calcola dai passaggi della quest, e impostarli a mano rischia di bloccare la partita. Le bottiglie sono vuote.

**Prima di sostituire uno slot copia tutta la cartella dei salvataggi.** Su NX2Apple gli slot sono in `Switch/save/0400486024DEC000/slot_XX/` (`slot_01` = slot 2 nel gioco). Se accanto c'è la cartella `0400486024DEC000.work`, copia il file anche lì.

**Il tuo salvataggio al 100%:** `python3 tools/zelda100.py progress.sav` crea `progress.sav.100` e lascia intatto l'originale.
