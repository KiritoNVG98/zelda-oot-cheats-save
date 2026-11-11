#!/bin/bash
# Doppio clic: salto alto per Zelda Ocarina of Time su NX2Apple (chiudi prima il gioco)
cd "$(dirname "$0")"
python3 -c "import zstandard" 2>/dev/null || { echo "Installo il modulo zstandard..."; python3 -m pip install --user zstandard || exit 1; }
echo "Trascina qui l'app di Zelda (The Legend of Zelda - Ocarina of Time.app) e premi Invio:"
read -r APP
echo "Quante volte più alto? (es. 35; scrivi off per disattivare):"
read -r MULT
/usr/bin/env python3 salto_alto.py "$APP" "$MULT"
echo
read -p "Premi Invio per chiudere questa finestra"
