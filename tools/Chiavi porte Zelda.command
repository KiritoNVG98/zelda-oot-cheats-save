#!/bin/bash
# Doppio clic per aprire tutte le porte chiuse a chiave: chiavi piccole e del boss in ogni dungeon (chiudi prima il gioco)
cd "$(dirname "$0")"
/usr/bin/env python3 chiavi_porte.py
echo
read -p "Premi Invio per chiudere questa finestra"
