# Klausur ersatzleistung Informatik
# Nils Wilhelm & Oliver Frank
# Spiel zum erkennen von verschiedenen Elektrischen Steck Verbindern

from tkinter import *
import random
import os

highscore = 0

base_path = os.path.dirname(os.path.abspath(__file__)) # Pfade relativ zu dieser Python Datei

leicht_folder_path = os.path.join(base_path, "leicht") # Pfad leichte Bilder
schwer_folder_path = os.path.join(base_path, "schwer") # Pfad schwere Bilder

def start_window(): # Startfenster mit Schwierigkeits Auswahl

    def stop():
        tkFenster.destroy()

    def start_leicht():
        tkFenster.destroy()
        spiel_window(1)

    def start_schwer():
        tkFenster.destroy()
        spiel_window(2)

    tkFenster = Tk() # Start fenster
    tkFenster.title("Stecker raten - Start")
    tkFenster.geometry("300x280")
    tkFenster.resizable(False, False)

    frameSpiel = Frame(master=tkFenster, background="white")
    frameSpiel.place(x=10, y=10, width=280, height=260)

    # Überschrift
    labelWillkommen = Label(master=frameSpiel, text = "Willkommen", font=("Arial", 14, "bold"), background="white")
    labelWillkommen.place(x=50, y=40, width=200, height=30)

    labelWähle = Label(master=frameSpiel, text = "wähle einen Schwierigkeitsgrad", font=("Arial", 10), background="white")
    labelWähle.place(x=40, y=90, width=200, height=30)

    # Knopf Leicht
    buttonLeicht = Button(master=frameSpiel, text="Leicht", command=start_leicht)
    buttonLeicht.place(x=40, y=140, width=80, height=40)
    
    # Knopf Schwer
    buttonSchwer = Button(master=frameSpiel, text="Schwer", command=start_schwer)
    buttonSchwer.place(x=160, y=140, width=80, height=40)
    
    # Knopf schließen
    buttonSchließen = Button(master=frameSpiel, text="Schließen", command=stop)
    buttonSchließen.place(x=40, y=200, width=80, height=30)

    # Knopf Hilfe
    buttonHilfe = Button(master=frameSpiel, text="Hilfe", command=hilfe_window)
    buttonHilfe.place(x=160, y=200, width=80, height=30)

    tkFenster.mainloop()

def spiel_window(difficulty): # Hauptfenster

    score = 0 # Punktestand
    timer = 0
    
    if difficulty == 1: # Timer an Schwierigkeitsgrad anpassen
        timer = 30
    elif difficulty == 2:
        timer = 45
    
    if difficulty == 1:
        folder_path = leicht_folder_path
    elif difficulty == 2:
        folder_path = schwer_folder_path
    else:
        print("Fehler bei der Auswahl des Schwierigkeitsgrades")

    def start():
        tkFenster.destroy()
        start_window()

    def load_gif(folder_path): # Zufälliges Bild aus Ordner laden
        gif_files = [f for f in os.listdir(folder_path) if f.endswith(".gif")]
        if not gif_files:
            raise ValueError("Keine GIF-Dateien im Ordner gefunden")
        return gif_files
    
    def update_timer():
        nonlocal timer
        if tkFenster.winfo_exists():  # Prüfen, ob das Fenster noch existiert
            if timer > 0:
                timer -= 1
                labelTimer.config(text=f"Zeit: {timer}s")
                tkFenster.after(1000, update_timer)
            else:
                tkFenster.destroy()
                ende_window(score)

    def check_antwort(answer):
        nonlocal score, gif_files, gif_path, correct_answer, gif_image, timer, folder_path

        if answer == correct_answer: # Antwort überprüfen
            score += 1
            labelScore.config(text=f"{score}")
        else:
            tkFenster.destroy()
            ende_window(score)
            return
        
        try: # Neues Bild und Antwortmöglichkeiten
            gif_path = os.path.join(folder_path, random.choice(gif_files))
            gif_image = PhotoImage(file=gif_path)
            bild.config(image=gif_image)
            bild.image = gif_image

            setup_buttons()  # Setze neue Buttons
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")
            bild.config(image="", text="Bild nicht verfügbar")

    def setup_buttons(): # Knöpfe erstellen mit einer richtigen und 3 falschen Antworten
        nonlocal correct_answer # Richtige Antwort auswählen
        random.shuffle(gif_files)
        correct_answer = os.path.basename(gif_path)

        wrong_answers = [f for f in gif_files if f != correct_answer] # 3 Falsche Antworten
        wrong_answers = random.sample(wrong_answers, 3)

        all_answers = [correct_answer] + wrong_answers # Alle Antworten mischen
        random.shuffle(all_answers)

        for idx, option in enumerate(all_answers): # Knöpfe aktualisieren
            button_text = os.path.splitext(option)[0]  # Nur Name ohne .gif
            answer_buttons[idx].config(text=button_text, command=lambda ans=option: check_antwort(ans))

    tkFenster = Tk() # Haupt Fenster
    tkFenster.title("Stecker raten - Spiel")
    tkFenster.geometry("510x765")
    tkFenster.resizable(False, False)

    frameSpiel = Frame(master=tkFenster, background="white")
    frameSpiel.place(x=10, y=10, width=490, height=745)

    # Punktestand Text
    labelScoreText = Label(master=frameSpiel, text = "Score:", background="orange")
    labelScoreText.place(x=40, y=20, width=60, height=30)
    # Punktestand Anzeige
    labelScore = Label(master=frameSpiel, text = score, background="orange")
    labelScore.place(x=100, y=20, width=30, height=30)
    
    # Timer
    labelTimer = Label(master=frameSpiel, text =f"Zeit: {timer}s", background="orange")
    labelTimer.place(x=220, y=20, width=50, height=30)
    
    # Highscore Text
    labelHighText = Label(master=frameSpiel, text = "Highscore:", background="orange")
    labelHighText.place(x=360, y=20, width=60, height=30)
    # Highscore Anzeige
    labelHigh = Label(master=frameSpiel, text = highscore, background="orange")
    labelHigh.place(x=420, y=20, width=30, height=30)

    gif_files = load_gif(folder_path)
    gif_path = os.path.join(folder_path, random.choice(gif_files))
    correct_answer = os.path.basename(gif_path)
    
    # Rahmen um Bilder
    frameBild = Frame(master=frameSpiel,
                   background="grey")
    frameBild.place(x=40, y=70, width=410, height=410)
    
    try:
        gif_image = PhotoImage(file=gif_path)
        bild = Label(master=frameSpiel, image=gif_image, background="white")
        bild.place(x=45, y=75, width=400, height=400)
    except Exception as e:
        print(f"Fehler beim Laden vom Bild: {e}")
        bild = Label(master=frameSpiel, text="Bild nicht verfügbar", background="white")
        bild.place(x=45, y=75, width=400, height=400)

    answer_buttons = []
    for idx in range(4):
        button = Button(
            master=frameSpiel,
            background=["red", "orange", "green", "yellow"][idx],
            font=("Arial", 12, "bold")
        )
        button.place(
            x=40 if idx % 2 == 0 else 250,
            y=495 if idx < 2 else 595,
            width=200,
            height=80
        )
        answer_buttons.append(button)
        
    # Knopf nochmal spielen
    buttonZurück = Button(master=frameSpiel, text="Zurück", command=start)
    buttonZurück.place(x=40, y=695, width=100, height=30)

    # SKnopf spiel schließen
    buttonHilfe = Button(master=frameSpiel, text="Hilfe", command=hilfe_window)
    buttonHilfe.place(x=350, y=695, width=100, height=30)

    setup_buttons() # Knöpfe platzieren
    update_timer() # Timer starten
    tkFenster.mainloop()

def ende_window(score):

    global highscore

    if score > highscore:
        highscore = score

    def start():
        tkFenster.destroy()
        start_window()

    def stop():
        tkFenster.destroy()

    tkFenster = Tk() # Spiel Vorbei Fenster
    tkFenster.title("Stecker raten - Ende")
    tkFenster.geometry("300x250")
    tkFenster.resizable(False, False)

    frameSpiel = Frame(master=tkFenster,
                   background="white")
    frameSpiel.place(x=10, y=10, width=280, height=230)

    # Überschrift
    labelPunkteText = Label(master=frameSpiel,text = "Game Over", font=("Arial", 14, "bold"), background="white")
    labelPunkteText.place(x=80, y=20, width=120, height=30)

    # Punkte Text
    labelPunkteText = Label(master=frameSpiel,text = "Punkte:", background="white")
    labelPunkteText.place(x=95, y=60, width=60, height=30)
    # Punkte Anzeige
    labelPunkte = Label(master=frameSpiel, text = score, background="white")
    labelPunkte.place(x=155, y=60, width=30, height=30)

    # Highscore Text
    labelPunkteText = Label(master=frameSpiel, text = "Highscore:", background="white")
    labelPunkteText.place(x=95, y=100, width=60, height=30)
    # Highscore Anzeige
    labelPunkte = Label(master=frameSpiel, text = highscore,
                        background="white")
    labelPunkte.place(x=155, y=100, width=30, height=30)

    # Knopf nochmal spielen
    buttonStart = Button(master=frameSpiel, text="Start Menü", command=start)
    buttonStart.place(x=70, y=140, width=140, height=30)

    # SKnopf spiel schließen
    buttonSchließen = Button(master=frameSpiel, text="Spiel Schließen", command=stop)
    buttonSchließen.place(x=70, y=180, width=140, height=30)
    
    tkFenster.mainloop()

def hilfe_window():

    def stop():
        tkFenster.destroy()

    tkFenster = Tk() # Hilfe / Spielanleitung Fenster
    tkFenster.title("Hilfe")
    tkFenster.geometry("900x350")
    tkFenster.resizable(False, False)

    frameSpiel = Frame(master=tkFenster,
                   background="white")
    frameSpiel.place(x=10, y=10, width=880, height=330)

    # Hilfe Überschrift
    labelÜberschrift = Label(master=frameSpiel,
                        text = "Spielanleitung",
                        background="white",
                        font=("Arial", 20, "bold"))
    labelÜberschrift.place(x=305, y=30, width=250, height=30)
    
    # Hilfe Text
    labelText = Label(master=frameSpiel,
                        text = "Um ein Spiel zu starten drücke im Start-Fenster entweder auf „Leicht“ oder „Schwer“.\n"
                        "Im Spiel bekommst du Oben ein Bild angezeigt, worauf ein Anschluss für Elektronische Geräte abgebildet ist.\n"
                        "Es könnte alles sein. Vom herkömmlichen USB Stecker bis hin zum Gardena Gartenschlauch Verbinder ist alles dabei.\n"
                        "Unter dem Bild siehst du dann 4 verschiedene Antwortmöglichkeiten. Klicke auf die Antwort die du für richtig hälst.\n"
                        "Deine Richtigen Antworte werden gezählt.\n"
                        "Das Spiel endet wenn du eine Falsche Antwort anklickst oder der Timer abläuft.\n"
                        "Dein Highscore wird gespeicher bis du das spiel einmal schließt.",
                        background="white",
                        font=("Arial", 12))
    labelText.place(x=20, y=60, width=840, height=200)

    # SKnopf spiel schließen
    buttonSchließen = Button(master=frameSpiel, text="Schließen", command=stop)
    buttonSchließen.place(x=355, y=280, width=140, height=30)

    tkFenster.mainloop()
    
start_window()