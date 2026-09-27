import os
import dill
import nltk
import tkinter as tk
from tkinter import *
from colorama import Fore, Style

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_first_response

# ---------------------------------------------------------
# Configurazione iniziale del Bot
# ---------------------------------------------------------
bot = ChatBot(
    'YatsuBot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'response_selection_method': get_first_response,
            'maximum_similarity_threshold': 0.94,
            'priority': 0,
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
            'priority': 2,  
        }
    ]
)

# ---------------------------------------------------------
# Funzioni di utilità per il training e il logging
# ---------------------------------------------------------
def train_from_file(trainer, file_path):
    """Legge un file testuale e lo utilizza per addestrare il bot."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            training_data = file.readlines()
        trainer.train(training_data)
        
        # Opzionale: Backup del modello testuale
        try:
            with open(r"modello.txt", 'ab') as out_file:
                dill.dump(training_data, out_file)
        except Exception as e:
            print(f"Avviso: Impossibile salvare il modello testuale ({e})")
    else:
        print(f"Avviso: File di training non trovato -> {file_path}")

def log_conversation(statement):
    """Salva lo statement della conversazione nel log locale."""
    try:
        with open(r"risposte.txt", 'ab') as file:
            dill.dump(statement, file)
    except Exception as e:
        pass # Ignora l'errore se il file non è accessibile o non necessario in produzione

# Inizializza il file del modello testuale se non esiste
try:
    if not os.path.exists(r"modello.txt"):
        with open(r"modello.txt", 'wb') as file:
            dill.dump("", file)
except Exception:
    pass

# ---------------------------------------------------------
# Logica di Addestramento
# ---------------------------------------------------------
choice_default = input("Eseguire il training di default? (S/N): ").strip().upper()
if choice_default == "S":
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    
    trainer = ListTrainer(bot)
    
    # Lista dei moduli di training di base
    default_modules = [
        r"Training\sports.yml", r"Training\scienza.yml", r"Training\psicologia.yml",
        r"Training\politica.yml", r"Training\movies.yml", r"Training\soldi.yml",
        r"Training\humor.yml", r"Training\gossip.yml", r"Training\emozioni.yml",
        r"Training\computers.yml", r"Training\ai.yml", r"Training\profilo.yml"
    ]
    
    for module in default_modules:
        train_from_file(trainer, module)
        
    trainer.export_for_training("./training.txt")
    print("Training di default completato.")

choice_custom = input("Eseguire il training personalizzato (ListTrainer)? (S/N): ").strip().upper()
if choice_custom == "S":
    trainer = ListTrainer(bot)
    custom_modules = [r"Training\animali.yml", r"Training\itisInformatica.yml"]
    
    for module in custom_modules:
        train_from_file(trainer, module)
        
    trainer.export_for_training("./training.txt")
    print("Training personalizzato completato.")

# ---------------------------------------------------------
# Interfaccia Grafica (GUI) - Tkinter
# ---------------------------------------------------------
def invia_messaggio_gui():
    """Gestisce l'invio del messaggio tramite interfaccia grafica."""
    messaggio = messaggio_inserito.get().strip()
    if non messaggio:
        return

    statement = Statement(text=messaggio)
    bot.learn_response(statement)
    log_conversation(statement)
    
    messaggio_inserito.delete(0, tk.END)
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"Tu: {messaggio}\n")
    
    if messaggio.lower() == "stop":
        chat.insert(tk.END, "Yatsu: Arrivederci!\n")
        chat.config(state=tk.DISABLED)
        root.after(2000, root.destroy)  
    else:
        risposta = bot.get_response(messaggio)
        chat.insert(tk.END, f"Yatsu: {risposta}\n")
        
    chat.config(state=tk.DISABLED)
    chat.yview(tk.END)

choice_gui = input("Avviare l'interfaccia grafica? (S/N): ").strip().upper()
if choice_gui == "S":
    root = tk.Tk()
    root.title("YatsuBot Conversation")

    chat = tk.Text(root, bd=1, height="8", width="50", font=("Arial", 16))
    chat.config(state=tk.DISABLED)
    chat.configure(bg="#f4f4f4") # Sostituito il rosso acceso con un grigio chiaro più formale
    
    chat.configure(state=tk.NORMAL)
    chat.insert(tk.END, "Yatsu: Ciao, come posso aiutarti?\n")
    chat.configure(state=tk.DISABLED)

    try:
        logo = tk.PhotoImage(file=r"YatsuImage.png").subsample(18)
        logo_label = tk.Label(root, image=logo, bg="#f4f4f4")
        logo_label.place(relx=1.0, x=-10, y=10, anchor="ne")
    except Exception as e:
        print(f"Avviso: Impossibile caricare il logo ({e})")

    messaggio_inserito = tk.Entry(root, bd=1, width="30", font=("Arial", 16))
    messaggio_inserito.bind("<Return>", (lambda event: invia_messaggio_gui()))
    messaggio_inserito.configure(bg="#ffffff")

    invia_pulsante = tk.Button(root, text="Invia", command=invia_messaggio_gui, bg="#C4C5C5")

    chat.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    messaggio_inserito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    invia_pulsante.pack(side=tk.RIGHT)
    
    root.mainloop()

# ---------------------------------------------------------
# Interfaccia a Riga di Comando (CLI)
# ---------------------------------------------------------
else:
    print(Fore.RED + "Yatsu: " + Style.RESET_ALL + "Ciao, come posso aiutarti?")
    while True:
        try:
            user_input = input(Fore.BLUE + "Tu: " + Style.RESET_ALL).strip()
            if not user_input:
                continue

            statement = Statement(text=user_input)
            bot.learn_response(statement)
            log_conversation(statement)
            
            if user_input.lower() == "stop":
                print(Fore.RED + "Yatsu: " + Style.RESET_ALL + "Arrivederci!")
                break

            bot_response = bot.get_response(user_input)
            print(Fore.RED + "Yatsu: " + Style.RESET_ALL + str(bot_response))
            
        except KeyboardInterrupt:
            print("\nChiusura del bot...")
            break
