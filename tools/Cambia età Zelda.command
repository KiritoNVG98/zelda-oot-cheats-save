#!/bin/bash
# Doppio clic per cambiare Link da bambino ad adulto (chiudi prima il gioco)
cd "$(dirname "$0")"
/usr/bin/env python3 cambia_eta.py
echo
read -p "Premi Invio per chiudere questa finestra"
