#!/bin/bash
# Doppio clic per completare tutte le missioni principali e secondarie (tranne Ganon). Chiudi prima il gioco.
cd "$(dirname "$0")"
/usr/bin/env python3 completa_tutto.py
echo
read -p "Premi Invio per chiudere questa finestra"
