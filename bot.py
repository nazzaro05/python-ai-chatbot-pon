#import os #Libreira os che uso per la funzione os.remove per cancellare il database del bot
from chatterbot import ChatBot
#import json #Non so come si usa, Forza Napoli
from chatterbot.trainers import ChatterBotCorpusTrainer
import dill
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_first_response
import nltk
import tkinter as tk
from colorama import Fore, Style
from tkinter import *\

# Funzione per inviare il messaggio all'interfaccia grafica
def invia_messaggio():
    messaggio = messaggio_inserito.get()
    statement = Statement(text=messaggio)
    bot.learn_response(statement)
    with open(r"risposte.txt", 'ab') as file:
        dill.dump(statement, file)
    messaggio_inserito.delete(0, tk.END)
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, "tu : " + messaggio + "\n")
    if messaggio.lower() == "stop":
        chat.insert(tk.END, "yatsu : ciao!\n")
        chat.config(state=tk.DISABLED)
        root.after(2000, root.destroy)  # Chiude la finestra dopo 2 secondi
    else:
        risposta = bot.get_response(messaggio)
        chat.insert(tk.END, "yatsu : " + str(risposta) + "\n")
    chat.config(state=tk.DISABLED)
    chat.yview(tk.END)
        
        

def train(s):
        with open(s, 'r') as file:
                dati_di_addestramento = file.readlines()
        trainer.train(dati_di_addestramento)
        with open(r"modello.txt", 'ab') as file:
                dill.dump(dati_di_addestramento, file)
                
with open(r"modello.txt", 'wb') as file:
                dill.dump("", file)


# creo il bot assegnando ad ogni logic adapter una prioritá, ovviamente quello
# che ha la prioritá piú alta é il "get first response" in 
# modo tale che il bot sia capace di trovare la risposta alla nostra domanda

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
        ,
        # Time logic adapter temporaneamente disabilitato perché troppo invasivo
        # {
        #     'import_path': 'chatterbot.logic.TimeLogicAdapter',
        #       'threshold': 0.98,
        #      'priority': 3 
        # }
        
    ]
)

#Mostra il nome del file del database del bot
#print(bot.storage.database_uri)

#Svuota il database del bot
#db_path = bot.storage.database_uri.replace('sqlite:///', '')
#os.remove(db_path)


if input("Vuoi allenare il bot col training di default?:(S/N) ").upper()=="S":
        trainer = ChatterBotCorpusTrainer(bot)
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        trainer = ListTrainer(bot)
        train(r"Training\sports.yml")
        train(r"Training\scienza.yml")
        train(r"Training\psicologia.yml")
        train(r"Training\politica.yml")
        train(r"Training\movies.yml")
        train(r"Training\soldi.yml")
        train(r"Training\humor.yml")
        train(r"Training\gossip.yml")
        train(r"Training\emozioni.yml")
        train(r"Training\computers.yml")
        train(r"Training\ai.yml")
        train(r"Training\profilo.yml") 
        trainer.export_for_training("./training.txt")
        
if input("Vuoi allenare il bot con il ListTrainer?(Training personalizzato) (S/N): ").upper()=="S":
        trainer = ListTrainer(bot)
        train(r"Training\animali.yml")
        train(r"Training\itisInformatica.yml")
        trainer.export_for_training("./training.txt")
        

if input("Vuoi iniziare la conversazione con l´interfaccia grafica? (S/N): ").upper()=="S":
        # Avvio del bot
        # Avviamo l'interfaccia grafica
        # Creiamo l'interfaccia grafica utilizzando Tkinter
        root = tk.Tk()
        root.title("YatsuBot Conversation")

        # Creiamo la finestra di chat
        chat = tk.Text(root, bd=1, height="8", width="50", font=("Arial", 16))
        chat.config(state=tk.DISABLED)
        chat.configure(bg="red")
        
        # Aggiungiamo il messaggio di benvenuto al campo di chat
        chat.configure(state=tk.NORMAL)
        chat.insert(tk.END, "yatsu : Ciao,come posso aiutarti?\n")
        chat.configure(state=tk.DISABLED)

        # Carichiamo l'immagine del logo
        logo = tk.PhotoImage(file=r"YatsuImage.png")
        logo = logo.subsample(18)  # Riduciamo le dimensioni dell'immagine

        # Aggiungiamo il logo alla finestra di chat
        logo_label = tk.Label(root, image=logo, bg="#FF7557")
        logo_label.place(relx=1.0, x=-10, y=10, anchor="ne")  # Posizioniamo l'immagine in alto a destra

        # Creiamo la finestra di inserimento del messaggio
        messaggio_inserito = tk.Entry(root, bd=1, width="30", font=("Arial", 16))
        messaggio_inserito.bind("<Return>", (lambda event: invia_messaggio()))
        messaggio_inserito.configure(bg="#AFBEBD")

        # Creiamo il pulsante "Invia"
        invia_pulsante = tk.Button(root, text="Invia", command=invia_messaggio)
        invia_pulsante.configure(bg="#C4C5C5")

        # Posizioniamo gli elementi nell'interfaccia grafica
        chat.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        messaggio_inserito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        invia_pulsante.pack(side=tk.RIGHT)
        
        root.mainloop()
else:
        # Avvio del bot
        print(Fore.RED+"yatsu : "+Style.RESET_ALL+"Ciao,come posso aiutarti?")
        while True:
                try:
                        # Leggi l'input dell'utente
                        user_input = input(Fore.BLUE+"tu : "+ Style.RESET_ALL)

                        # Ottieni la risposta del bot e lui impara quella dell'utente(che viene convertita in statement)
                        statement = Statement(text=user_input)
                        bot.learn_response(statement)
                        with open(r"risposte.txt", 'ab') as file:
                                dill.dump(statement, file)
                                
                        if user_input.lower() == "stop":
                                print(Fore.RED+"yatsu : "+Style.RESET_ALL+"ciao!" )
                                break

                        bot_response = bot.get_response(user_input)
                        
                        # Stampa la risposta del bot
                        print(Fore.RED+"yatsu : "+ Style.RESET_ALL+ str(bot_response))
                        
                except KeyboardInterrupt :
                        break