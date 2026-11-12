# Step-by-step guide for NX2Apple (Mac)

🇮🇹 [Guida in italiano più in basso](#guida-passo-passo-per-nx2apple-mac)

This guide is for Ocarina of Time (`0400486024DEC000`) running on **NX2Apple**. You need a Mac where the game already starts in NX2Apple. You don't need to know how to program: every command goes into the **Terminal** app, one at a time, and you press Enter after each.

## 0. Download the files

On the repository page press **Code → Download ZIP**, then double-click the ZIP in Downloads. You get a folder called `zelda-oot-cheats-save-main`. The commands below assume it is in your **Downloads** folder.

## 1. Check your game version

The cheat only works on one version of the game (build `E0F3CCFAF50065AE`). Start the game once, close it, then run:

```
grep -h "cheats:" ~/Downloads/Switch/*/log/0400486024DEC000.log ~/Downloads/Switch/log/0400486024DEC000.log ~/Library/Logs/nxnative/0400486024DEC000.log 2>/dev/null | tail -3
```

- If you see `build E0F3CCFAF50065AE`, you can go on.
- If you see another build, the cheat is **not** for your version: skip to step 3 (the save and the script work anyway).
- If nothing shows up, NX2Apple keeps its library somewhere else. Open NX2Apple, look at where your games are, and use that folder instead of `~/Downloads/Switch` in the commands.

## 2. Install the cheats (rupees at 1000, infinite health, infinite magic, jump without cap)

**a.** Create the cheats folder for the game:
```
mkdir -p ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats
```

**b.** Copy the cheat into it:
```
cp ~/Downloads/zelda-oot-cheats-save-main/cheats/E0F3CCFAF50065AE.txt ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats/
```

**c.** Start the game. In the menu bar at the top, open the **Cheats** menu and turn on the ones you want: **«Rupees 1000 / Rupie 1000»** and/or **«Infinite health / Vita infinita»**, **«Infinite magic / Magia infinita»**. NX2Apple remembers the choice for the next launch.

**d.** Load a save and pick up a rupee or open the menu: the counter goes to 1000 (or to the most your wallet holds).

**e. Infinite health and magic:** while they are on, the hearts and the magic meter stay full.

**f. Age switch (child ↔ adult):** this one is not a cheat. Close the game, double-click `tools/Cambia età Zelda.command` in the repository folder, drag your save folder `0400486024DEC000` into the window when it asks, type the slot number and press Enter. Reopen the game and load the slot. The script backs up the slot first. If macOS says it can't open the file, right-click it → **Open**.

**g. High jump:** close the game, double-click `tools/Salto alto Zelda.command`, drag the Zelda app (`The Legend of Zelda - Ocarina of Time.app`) into the window, press Enter and type how many times higher (I use `35`). Start the game and turn on **«Jump without 5 m cap / Salto senza limite»** in the Cheats menu: without it the game stops the jump at 5 m. To go back to the normal jump, run the `.command` again and type `off`. Save before you try it: from that high you can land where the game never expected you.

**To turn it off:** turn it off in the Cheats menu and **quit and restart the game**. Turning it off while playing does not undo it.

**Check that it loaded:** after a launch, run the command from step 1 again. It should say `4 cheats (0 master, … on, 0 broken, 4 runnable)`. If it says `0 on`, the cheats are loaded but off: turn them on from the menu.

## 3. Use the full-inventory save (every quest done)

**Close the game before you start.** If the game is open, it can overwrite the file.

**a.** Find your save folder:
```
find ~/Downloads ~/Library/Application\ Support -type d -name "0400486024DEC000*" -path "*save*" 2>/dev/null
```
You usually get two folders: `.../save/0400486024DEC000` and `.../save/0400486024DEC000.work`. Inside each there are `slot_00`, `slot_01`, … folders.

**b.** Make a copy of your saves (do not skip this). In the commands below, put the path from step **a** that does **not** end in `.work` in place of `SAVE`:
```
cp -R "SAVE" ~/Desktop/Zelda-save-backup
```
If anything goes wrong, you copy this folder back and you are where you started.

**c.** Choose the slot to replace and the age you want: `save/child` (Link as a child) or `save/adult` (Link as an adult). The folder numbers start at 0: `slot_00` = slot 1 in the game, `slot_01` = slot 2, and so on.

**d.** Copy the save into that slot, **in both folders** (`0400486024DEC000` and `0400486024DEC000.work`). For the child save in slot 2 (use `adult` instead of `child` for the adult one):
```
cp ~/Downloads/zelda-oot-cheats-save-main/save/child/*.sav "SAVE/slot_01/"
cp ~/Downloads/zelda-oot-cheats-save-main/save/child/*.sav "SAVE.work/slot_01/"
```

**e.** Start the game and load that slot.

## 4. Make your own save 100% (instead of using mine)

This keeps your own progress and only gives you the full inventory. Close the game, make the backup from step 3b, then run (slot 2 in this example):

```
python3 ~/Downloads/zelda-oot-cheats-save-main/tools/zelda100.py "SAVE/slot_01/progress.sav"
```

The script writes `progress.sav.100` next to your save and leaves the original alone. If it says `values changed`, put the new file in place of the old one in both folders:

```
cp "SAVE/slot_01/progress.sav.100" "SAVE/slot_01/progress.sav"
cp "SAVE/slot_01/progress.sav.100" "SAVE.work/slot_01/progress.sav"
```

You want a different rupee count? Add it at the end of the first command, for example `… progress.sav 500`.

**Complete the quests too:** with the game closed, double-click `tools/Completa tutto Zelda.command`, drag the `SAVE` folder into the window, type the slot number (or `T` for all slots) and press Enter. Every main and side quest is set as done, except the final battle with Ganon, and every dungeon gets its map, compass, boss key and 30 small keys; the Door of Time opens. For the keys and the Door of Time only, use `tools/Chiavi porte Zelda.command` the same way. Both make a backup of each slot first, in `Backup salvataggi Zelda` next to the `save` folder.

## If something goes wrong

- **The game crashes or the slot doesn't load:** close the game and copy back the backup from step 3b.
- **The cheat doesn't change the rupees:** check the build (step 1) and that the cheat is on (step 2, *Check that it loaded*).
- **The age doesn't change:** close the game completely before running the script (step 2f).
- **The quests:** neither the save nor the script completes quests or the story. That is on purpose: setting them by hand can leave the game stuck.

---

# Guida passo passo per NX2Apple (Mac)

Questa guida è per Ocarina of Time (`0400486024DEC000`) su **NX2Apple**. Ti serve un Mac su cui il gioco si avvia già con NX2Apple. Non devi saper programmare: ogni comando va nell'app **Terminale**, uno alla volta, premendo Invio dopo ciascuno.

## 0. Scarica i file

Nella pagina del repository premi **Code → Download ZIP**, poi fai doppio clic sullo ZIP in Download. Ottieni la cartella `zelda-oot-cheats-save-main`. I comandi qui sotto danno per scontato che sia nella cartella **Download**.

## 1. Controlla la versione del gioco

Il cheat funziona su una sola versione del gioco (build `E0F3CCFAF50065AE`). Avvia il gioco una volta, chiudilo e lancia:

```
grep -h "cheats:" ~/Downloads/Switch/*/log/0400486024DEC000.log ~/Downloads/Switch/log/0400486024DEC000.log ~/Library/Logs/nxnative/0400486024DEC000.log 2>/dev/null | tail -3
```

- Se compare `build E0F3CCFAF50065AE`, puoi andare avanti.
- Se compare un'altra build, il cheat **non** è per la tua versione: passa al punto 3 (il salvataggio e lo script funzionano lo stesso).
- Se non compare niente, NX2Apple tiene la libreria da un'altra parte. Apri NX2Apple, guarda dove sono i tuoi giochi e usa quella cartella al posto di `~/Downloads/Switch` nei comandi.

## 2. Installa i cheat (rupie a 1000, vita infinita, magia infinita, salto senza limite)

**a.** Crea la cartella dei cheat del gioco:
```
mkdir -p ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats
```

**b.** Copiaci dentro il cheat:
```
cp ~/Downloads/zelda-oot-cheats-save-main/cheats/E0F3CCFAF50065AE.txt ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats/
```

**c.** Avvia il gioco. Nella barra dei menu in alto apri il menu **Cheat** e accendi quelli che vuoi: **«Rupees 1000 / Rupie 1000»** e/o **«Infinite health / Vita infinita»**, **«Infinite magic / Magia infinita»**. NX2Apple si ricorda la scelta al lancio successivo.

**d.** Carica una partita e raccogli una rupia oppure apri il menu: il contatore va a 1000 (o al massimo del tuo borsello).

**e. Vita e magia infinite:** finché sono accesi, cuori e barra della magia restano pieni.

**f. Cambio età (bambino ↔ adulto):** questo non è un cheat. Chiudi il gioco, fai doppio clic su `tools/Cambia età Zelda.command` nella cartella del repository, trascina nella finestra la cartella dei salvataggi `0400486024DEC000`, scrivi il numero dello slot e premi Invio. Riapri il gioco e carica lo slot. Lo script fa prima un backup dello slot. Se macOS dice che non può aprirlo, clic destro → **Apri**.

**g. Salto alto:** chiudi il gioco, fai doppio clic su `tools/Salto alto Zelda.command`, trascina nella finestra l'app di Zelda (`The Legend of Zelda - Ocarina of Time.app`), premi Invio e scrivi quante volte più in alto (io uso `35`). Avvia il gioco e accendi **«Jump without 5 m cap / Salto senza limite»** dal menu Cheat: senza, il gioco ferma il salto a 5 metri. Per tornare al salto normale rilancia il `.command` e scrivi `off`. Salva prima di provarlo: da così in alto puoi atterrare dove il gioco non se lo aspetta.

**Per spegnerlo:** spegnilo dal menu Cheat e **chiudi e riapri il gioco**. Spegnerlo mentre giochi non lo annulla.

**Per controllare che sia caricato:** dopo un avvio rilancia il comando del punto 1. Deve dire `4 cheats (0 master, … on, 0 broken, 4 runnable)`. Se dice `0 on`, i cheat sono caricati ma spenti: accendili dal menu.

## 3. Usa il salvataggio con tutto l'inventario (missioni completate)

**Chiudi il gioco prima di iniziare.** Se il gioco è aperto, può sovrascrivere il file.

**a.** Trova la cartella dei salvataggi:
```
find ~/Downloads ~/Library/Application\ Support -type d -name "0400486024DEC000*" -path "*save*" 2>/dev/null
```
Di solito escono due cartelle: `.../save/0400486024DEC000` e `.../save/0400486024DEC000.work`. Dentro ognuna ci sono le cartelle `slot_00`, `slot_01`, …

**b.** Fai una copia dei tuoi salvataggi (non saltare questo passaggio). Nei comandi che seguono, metti al posto di `SAVE` il percorso del punto **a** che **non** finisce con `.work`:
```
cp -R "SAVE" ~/Desktop/Zelda-backup-salvataggi
```
Se qualcosa va storto, ricopi questa cartella al suo posto e sei di nuovo dove eri.

**c.** Scegli lo slot da sostituire e l'età: `save/child` (Link bambino) o `save/adult` (Link adulto). I numeri delle cartelle partono da 0: `slot_00` = slot 1 nel gioco, `slot_01` = slot 2, e così via.

**d.** Copia il salvataggio in quello slot, **in tutte e due le cartelle** (`0400486024DEC000` e `0400486024DEC000.work`). Per il salvataggio bambino nello slot 2 (per l'adulto scrivi `adult` al posto di `child`):
```
cp ~/Downloads/zelda-oot-cheats-save-main/save/child/*.sav "SAVE/slot_01/"
cp ~/Downloads/zelda-oot-cheats-save-main/save/child/*.sav "SAVE.work/slot_01/"
```

**e.** Avvia il gioco e carica quello slot.

## 4. Porta al 100% il tuo salvataggio (invece di usare il mio)

Così tieni i tuoi progressi e ricevi solo l'inventario completo. Chiudi il gioco, fai la copia del punto 3b, poi lancia (slot 2 nell'esempio):

```
python3 ~/Downloads/zelda-oot-cheats-save-main/tools/zelda100.py "SAVE/slot_01/progress.sav"
```

Lo script crea `progress.sav.100` accanto al tuo salvataggio e lascia intatto l'originale. Se scrive `values changed`, metti il file nuovo al posto di quello vecchio in tutte e due le cartelle:

```
cp "SAVE/slot_01/progress.sav.100" "SAVE/slot_01/progress.sav"
cp "SAVE/slot_01/progress.sav.100" "SAVE.work/slot_01/progress.sav"
```

Vuoi un altro numero di rupie? Aggiungilo in fondo al primo comando, per esempio `… progress.sav 500`.

**Completa anche le missioni:** a gioco chiuso fai doppio clic su `tools/Completa tutto Zelda.command`, trascina nella finestra la cartella `SAVE`, scrivi il numero dello slot (o `T` per tutti) e premi Invio. Tutte le missioni principali e secondarie risultano fatte, tranne la battaglia finale con Ganon; ogni dungeon ha mappa, bussola, chiave del boss e 30 chiavi piccole, e la Porta del Tempo si apre. Solo per chiavi e Porta del Tempo usa allo stesso modo `tools/Chiavi porte Zelda.command`. Tutti e due fanno prima un backup di ogni slot in `Backup salvataggi Zelda`, accanto alla cartella `save`.

## Se qualcosa va storto

- **Il gioco va in crash o lo slot non si carica:** chiudi il gioco e ricopia la copia del punto 3b.
- **Il cheat non cambia le rupie:** controlla la build (punto 1) e che il cheat sia acceso (punto 2, *Per controllare che sia caricato*).
- **L'età non cambia:** chiudi del tutto il gioco prima di lanciare lo script (punto 2f).
- **Le quest:** né il salvataggio né lo script completano le quest o la storia. È voluto: impostarle a mano può bloccare la partita.
