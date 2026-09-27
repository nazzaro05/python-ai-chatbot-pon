# YatsuBot - Python AI Chatbot (Progetto PON)

Questo progetto è un chatbot in Python sviluppato originariamente come elaborato finale per il modulo "Robotica Educativa e Coding" (Maggio 2023) e successivamente ampliato.

Il bot utilizza la libreria `chatterbot` per elaborare il linguaggio naturale e gestire le conversazioni. È in grado di apprendere dinamicamente nuovi input dall'utente (salvandoli in un database SQLite locale) ed è stato pre-addestrato su una serie di file YAML tematici (informatica, IA, emozioni, ecc.).

## Funzionalità principali
- **NLP e Machine Learning:** Utilizza il `BestMatch` logic adapter per trovare la risposta più coerente in base alla soglia di similarità (0.94).
- **Addestramento modulare:** Il bot carica dataset specifici (YAML) tramite `ChatterBotCorpusTrainer` e `ListTrainer`.
- **Interfaccia Grafica:** Implementa una GUI creata con `tkinter` per permettere l'interazione visiva, con supporto di fallback a riga di comando (CLI) tramite `colorama`.
- **Apprendimento continuo:** Nel file sorgente, la funzione `bot.learn_response(statement)` permette al bot di registrare nuovi pattern conversazionali in tempo reale.

## Struttura del codice
- `bot.py`: Il file core contenente la logica di inizializzazione, l'impostazione degli adapter e la gestione dell'interfaccia grafica.
- Cartella `Training`: Contiene i dataset YAML utilizzati per addestrare il bot su vari argomenti.

*Nota: I file del database SQLite e i log di conversazione generati durante i test locali sono stati esclusi dal repository per questioni di privacy e pulizia del codice.*
