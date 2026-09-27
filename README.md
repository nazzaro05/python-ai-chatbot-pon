# YatsuBot - Python AI Chatbot (Progetto PON)

Chatbot sviluppato in Python come elaborato finale per il modulo scolastico "Robotica Educativa e Coding" (Maggio 2023). Il progetto esplora le basi dell'Intelligenza Artificiale conversazionale, l'elaborazione del linguaggio naturale (NLP) e la creazione di interfacce grafiche desktop.

## Stack Tecnologico
- **Linguaggio:** Python 3
- **Libreria NLP/Chatbot:** ChatterBot (con metriche di similarità e adapter logici per la valutazione matematica)
- **Interfaccia Grafica (GUI):** Tkinter
- **Addestramento:** Dataset testuali strutturati in formato YAML (`ChatterBotCorpusTrainer` e `ListTrainer`)

## Architettura del Codice
- `bot.py`: Script principale che gestisce l'inizializzazione del motore di chat, il caricamento dei moduli di training e l'interfaccia utente (con supporto opzionale a riga di comando).
- Cartella `Training/`: Contiene i dataset tematici in formato YAML utilizzati per addestrare il bot su vari domini (informatica, IA, emozioni, etc.), inclusi moduli personalizzati legati al contesto scolastico.

*Nota: I log di conversazione locali (`risposte.txt`, `modello.txt`) e i database SQLite generati durante l'esecuzione sono esclusi dal controllo di versione per best practice di sicurezza e pulizia del codice.*
