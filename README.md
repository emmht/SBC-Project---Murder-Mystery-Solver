# SBC-Project---Murder-Mystery-Solver

## Descriere
Acest proiect implementează un sistem capabil să rezolve puzzle-uri de tip murder mystery.

Aplicația permite selectarea unui puzzle din interfață, afișarea indiciilor și determinarea automată a soluției folosind raționament logic în Prolog.

## Tehnologii folosite
- Python
- SWI-Prolog
- Tkinter

## Structura proiectului
- `logic/` - încărcarea puzzle-urilor, generarea faptelor Prolog, rularea solverului
- `prolog/` - fișierele Prolog (`solver.pl`, `facts.pl`)
- `puzzles/` - puzzle-uri în format JSON
- `ui/` - interfața grafică
- `main.py` - punct de intrare alternativ pentru testare

## Funcționalități
- selectarea unui puzzle din interfață
- afișarea suspecților, camerelor, armelor și indiciilor
- conversia puzzle-ului în fapte Prolog
- rezolvarea puzzle-ului cu SWI-Prolog
- afișarea soluției
- afișarea unei explicații pas cu pas

## Cerințe
- Python 3.13
- SWI-Prolog
- Tkinter

## Autori
- Andries Costin
- Mihalescu Iulia
- Nitu Emma-Maria
