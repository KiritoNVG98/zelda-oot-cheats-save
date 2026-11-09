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

## 2. Install the cheats (rupees at 1000, age switch)

**a.** Create the cheats folder for the game:
```
mkdir -p ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats
```

**b.** Copy the cheat into it:
```
cp ~/Downloads/zelda-oot-cheats-save-main/cheats/E0F3CCFAF50065AE.txt ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats/
```

**c.** Start the game. In the menu bar at the top, open the **Cheats** menu and turn on the ones you want: **«Rupees 1000 / Rupie 1000»** and/or **«Age switch: L+R+ZL+ZR + Up = adult, Down = child»**. NX2Apple remembers the choice for the next launch.

**d.** Load a save and pick up a rupee or open the menu: the counter goes to 1000 (or to the most your wallet holds).

**e. Age switch:** hold **L + R + ZL + ZR** and press **D-pad Up** (adult) or **D-pad Down** (child) for a second. Then open the menu → System → **Save**, and **Load** the same slot: you come back with the other age. The game only reads the age when it loads a save, so nothing changes before that. Don't do it inside a dungeon that only exists for one age.

**To turn it off:** turn it off in the Cheats menu and **quit and restart the game**. Turning it off while playing does not undo it.

**Check that it loaded:** after a launch, run the command from step 1 again. It should say `2 cheats (0 master, … on, 0 broken, 2 runnable)`. If it says `0 on`, the cheats are loaded but off: turn them on from the menu.

## 3. Use the full-inventory save

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

## If something goes wrong

- **The game crashes or the slot doesn't load:** close the game and copy back the backup from step 3b.
- **The cheat doesn't change the rupees:** check the build (step 1) and that the cheat is on (step 2, *Check that it loaded*).
- **The age doesn't change:** after the combo you must save and load the slot (step 2e).
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

## 2. Installa i cheat (rupie a 1000, cambio età)

**a.** Crea la cartella dei cheat del gioco:
```
mkdir -p ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats
```

**b.** Copiaci dentro il cheat:
```
cp ~/Downloads/zelda-oot-cheats-save-main/cheats/E0F3CCFAF50065AE.txt ~/Library/Application\ Support/nxnative/0400486024DEC000/cheats/
```

**c.** Avvia il gioco. Nella barra dei menu in alto apri il menu **Cheat** e accendi quelli che vuoi: **«Rupees 1000 / Rupie 1000»** e/o **«Age switch … / Cambio eta'»**. NX2Apple si ricorda la scelta al lancio successivo.

**d.** Carica una partita e raccogli una rupia oppure apri il menu: il contatore va a 1000 (o al massimo del tuo borsello).

**e. Cambio età:** tieni **L + R + ZL + ZR** e premi **↑** (adulto) o **↓** (bambino) per un secondo. Poi apri il menu → Sistema → **Salva** e **Carica** lo stesso slot: ricompari con l'altra età. Il gioco legge l'età solo quando carica una partita, quindi prima non cambia niente. Non farlo dentro un tempio che esiste per una sola età.

**Per spegnerlo:** spegnilo dal menu Cheat e **chiudi e riapri il gioco**. Spegnerlo mentre giochi non lo annulla.

**Per controllare che sia caricato:** dopo un avvio rilancia il comando del punto 1. Deve dire `2 cheats (0 master, … on, 0 broken, 2 runnable)`. Se dice `0 on`, i cheat sono caricati ma spenti: accendili dal menu.

## 3. Usa il salvataggio con tutto l'inventario

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

## Se qualcosa va storto

- **Il gioco va in crash o lo slot non si carica:** chiudi il gioco e ricopia la copia del punto 3b.
- **Il cheat non cambia le rupie:** controlla la build (punto 1) e che il cheat sia acceso (punto 2, *Per controllare che sia caricato*).
- **L'età non cambia:** dopo la combinazione devi salvare e ricaricare lo slot (punto 2e).
- **Le quest:** né il salvataggio né lo script completano le quest o la storia. È voluto: impostarle a mano può bloccare la partita.
