import tkinter as tk
from pygame import mixer
from tkinter import messagebox
import json, logging, os

logging.basicConfig(filename="files/logs/game.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logging.info("Logger activated")

class DoNotPressGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Do not press the button game")
        self.root.attributes('-fullscreen', True)  # Make the window full screen
        self.root.configure(bg="#36393F")
        self.root.bind('<Escape>', self.open_menu)

        # Initialize the mixer
        mixer.init()

        self.counter = 0
        self.settings_opened = False
        self.options_opened = False
        self.menu = None
        self.options = False

        self.parametrai = {
            "sound": 1.0,
            "sound_effects": 1.0
        }

        try:
            self.load_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Game errored! Report id: {e}")
            exit()

        # Logging systems
        if not os.path.exists("files/logs"):
            os.makedirs("files/logs")
        self.enemies = [
            "Lempa", "Sluota", "Vampyras", "Šuo", "Pikachu", "Drakonas", "UFO"
        ]
        self.messages = [
            "Sveikas atvykęs į žaidima!",
            "Tai kaip sekasi?",
            "Moki skaityti žaidimo pavadinima tikiuosi aš",
            "Nes nemanau kad moki skaityt iš viso",
            "Tiesa sakau?",
            "Kažkas tau neaišku?",
            "Klausyk tu, tu be kostiumo...",
            "Ei! Ko mane pertraukei?",
            "Pakaks! Viskas nebegaliu",
            "Aš išeinu!",
            "Kaip tu mane radai?",
            "Bet realiai, kodėl tu mane spaudinėji?",
            "Neturi ką veikt?",
            "Tuoj kaip pisiu tau iš lempos per galva!",
            "Gaudyk!",
            "Tai kaip susitariam?",
            "Ar tu baigi spaudinėjęs šį mygtuką",
            "Ar man tau trenkt iš šluotos per kupra?",
            "Iš šluotos?",
            "Gaudyk!",
            "Va šetau!",
            "Vis dar spaudinėt gali?", # 21
            "Tuoj be nagų liksi!",
            "Palauk, atitemsiu vampyrą tau",
            "Gaudyk!",
            "Pulk vampyre!",
            "Neišsigandai?",
            "Tuoj atsiųsiu tau šunį",
            "Gaudyk!",
            "Pulk šuniuk jį!",
            "Neišsigandai vistiek?",
            "Tuoj atsiųsiu tau pokemoną",
            "Tiksliau pokemoną: Pikachu",
            "Reik tik pirma aišku pagauti jį",
            "Gaudyk!",
            "Ok pagavau, bet jis kažkur dingo...",
            "Radau!",
            "Pikachu, na ką tu čia darai?",
            "Pikachu, pulk jį!",
            "Matau kad nepaeis čia su tavim susitarti...",
            "Tuoj atsiųsiu tau drakoną",
            "Biški drakono nerandu, luktelk",
            "Nu kur jis dingo?",
            "Gal čia?",
            "O gal čia?",
            "Nerandu jo... Džiaukis",
            "Pabėgo čiuju",
            "Per ta laika pasiklausyk šitos",
            "Gražios dainos :)",
            "Nu patiko?",
            "NEPATIKO?",
            "KAIP ĮSIŽEIDŽIAU!",
            "Vsio, atsiųsiu tau UFO",
            "Bet luktelėk...",
            "Aš juk esu tik mygtukas...",
            "Tai grobiam ko mes čia dar laukiam!",
            "Kviečia Mygtukas komandą:",
            "XD", # 56
        ]

        self.images = ['files/images/lempa.png', 'files/images/sluota1.png', 'files/images/sluota2.png', 'files/images/vampyras.png',
                       'files/images/suo1.png', 'files/images/suo2.png', 'files/images/pikachu1.png', 'files/images/pikachu2.png',
                       'files/images/catchingpokemon.png', 'files/images/pikachu.png']
        self.music = ['files/music/background/1.mp3', 'files/music/background/2.mp3', 'files/music/background/3.mp3']
        self.sound_effects = ['files/sound/click.wav']
        self.generate_pyinstaller_command()
        # Load the background music
        try:
            mixer.music.load(self.music[1])
            self.sound_effect = mixer.Sound(self.sound_effects[0])

            mixer.music.set_volume(self.parametrai["sound"])  # Set the volume of the music
            self.sound_effect.set_volume(self.parametrai["sound_effects"])  # Set the volume of the sound effect

            # Play the background music
            mixer.music.play(-1)  # -1 means the music will loop indefinitely
            logging.debug("Background music loaded and started")
        except Exception as e:
            logging.error(f"Error loading the background music: {e}")
            messagebox.showerror("Error", f"Game errored! Report id: {e}")
            exit() # Game did not even started so do not need to destroy the window
        
        self.game_title = tk.Label(self.root, text="Do not press the button game", font=("Monaco", 32), bg="#36393F", fg="#ffffff")
        self.game_title.pack(pady=20)
        
        self.label = tk.Label(self.root, text="", font=("Monaco", 16), bg="#36393F", fg="#ffffff")
        self.label.pack(pady=20)

        self.hp_current = 100
        self.hp = tk.Label(self.root, text=f"HP: {self.hp_current}", font=("Monaco", 16), bg="#36393F", fg="#ffffff")
        self.hp.pack(pady=20)

        self.button = tk.Button(self.root, text="Nespaudi manęs", command=self.button_press, bg="#36393F", fg="#ffffff", font=("Monaco", 12))
        self.button.pack()

        self.warning = tk.Label(self.root, text="Version: 0.0.1-ALPHA (This release is limited for some of the testers)", font=("Monaco", 8), bg="#36393F", fg="red")
        self.warning.place(relx=1, rely=1, anchor="se")

    def load_settings(self):
        try:
            with open("files/settings.json", "r") as file:
                self.parametrai = json.load(file)
                logging.debug("Settings loaded")
        except FileNotFoundError:
            self.save_settings()
            logging.debug("Settings file not found, creating new one")
    
    def generate_pyinstaller_command(self):
        data_files = self.images + self.music + self.sound_effects
        add_data_options = [f'--add-data "{file};{os.path.dirname(file)}"' for file in data_files]
        add_data_str = ' '.join(add_data_options)
        command = f'pyinstaller {add_data_str} main.py'
        print(command)

    def save_settings(self):
        with open("files/settings.json", "w") as file:
            json.dump(self.parametrai, file, indent=4)
            logging.debug("Settings saved")

    def open_menu(self, event):
        if self.settings_opened:
            self.menu.destroy()
            self.settings_opened = False
            mixer.music.unpause()
        else:
            self.settings_opened = True
            self.menu = tk.Frame(self.root)
            mixer.music.pause()
            self.menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            resume_button = tk.Button(self.menu, text="Resume", command=self.exit_menu, width=100, height=2, bg="green", fg="white")
            resume_button.pack()

            options_button = tk.Button(self.menu, text="Options", command=self.open_options, width=100, height=2, bg="blue", fg="white")
            options_button.pack()

            exit_button = tk.Button(self.menu, text="Exit", command=self.root.destroy, width=100, height=2, bg="red", fg="white")
            exit_button.pack()

    def open_options(self):
        if self.options_opened:
            self.options.destroy()
            self.options_opened = False
            logging.debug("Options closed")
        else:
            logging.debug("Options opened")
            self.options_opened = True
            self.options = tk.Frame(self.root)
            self.options.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            volume_label = tk.Label(self.options, text="Volume", font=("Monaco", 12))
            volume_label.pack()

            volume = tk.Scale(self.options, from_=0, to=1, resolution=0.01, orient='horizontal', command=self.change_volume)
            volume.set(mixer.music.get_volume())
            volume.pack()

            sound_effects_label = tk.Label(self.options, text="Sound Effects", font=("Monaco", 12))
            sound_effects_label.pack()

            sound_effects_volume = tk.Scale(self.options, from_=0, to=1, resolution=0.01, orient='horizontal', command=self.change_sound_effects_volume)
            sound_effects_volume.set(self.sound_effect.get_volume())
            sound_effects_volume.pack()

            # Button to close options
            close_button = tk.Button(self.options, text="Close", command=self.options.destroy)
            close_button.pack()

    def change_volume(self, value):
        mixer.music.set_volume(float(value))
        logging.debug(f"Volume changed to {value}")
        self.parametrai["sound"] = float(value)
        self.save_settings()

    def change_sound_effects_volume(self, value):
        self.sound_effect.set_volume(float(value))
        logging.debug(f"Sound effects volume changed to {value}")
        self.parametrai["sound_effects"] = float(value)
        self.save_settings()

    def exit_menu(self):
        self.menu.destroy()
        self.settings_opened = False
        mixer.music.unpause()
        logging.debug("Options closed")

    def take_hp(self, hp):
        self.hp_current -= hp
        if self.hp_current <= 0:
            logging.info(f"Player died at {self.counter} press")
            self.hp.config(text="HP: 0")
            self.label.config(text="PAGALIAU TAVE NUKOVIAU! OMG NOOBAS!! HAHAHAHAHA")
            mixer.music.stop()
            messagebox.showinfo("Game Over", "You died!")
            self.root.quit()
        logging.debug(f"HP taken: {hp}")
        self.hp.config(text=f"HP: {self.hp_current}")

    def heal_hp(self, hp):
        self.hp_current += hp
        if self.hp_current > 100:
            self.hp_current = 100
        self.hp.config(text=f"HP: {self.hp_current}")

    def button_press(self):
        try:
            print(f"Button pressed {self.counter}")
            logging.debug(f"Button pressed {self.counter}")
            self.sound_effect.play()
            if self.counter < len(self.messages):
                self.label.config(text=self.messages[self.counter])
                self.button.config(state="disabled")
                self.root.after(1000, self.button.config, {"state": "normal"})
                if self.counter == 2:
                    self.game_title.config(fg="red")
                    self.root.after(1000, self.game_title.config, {"fg": "#ffffff"})
                if self.counter == 9:  # Hide the button after the 3rd press
                    self.button.pack_forget()
                    self.root.after(3500, self.button.pack)  # Show the button again after 2 seconds
                if self.counter == 14: # Show image after the 15th press
                    self.lempa = tk.PhotoImage(file=self.images[0])
                    self.lempa_image = tk.Label(self.root, image=self.lempa, bg="#36393F")
                    self.lempa_image.pack()
                    self.take_hp(10)
                if self.counter == 15:
                    self.lempa_image.destroy()
                if self.counter == 19:
                    self.sluota1 = tk.PhotoImage(file=self.images[1])
                    self.sluota1_image = tk.Label(self.root, image=self.sluota1, bg="#36393F")
                    self.sluota1_image.pack()
                    self.take_hp(10)
                if self.counter == 20:
                    self.sluota1_image.destroy()
                    self.sluota2 = tk.PhotoImage(file=self.images[2])
                    self.sluota2_image = tk.Label(self.root, image=self.sluota2, bg="#36393F")
                    self.sluota2_image.pack()
                    self.take_hp(10)
                if self.counter == 21:
                    self.sluota2_image.destroy()
                if self.counter == 24:
                    self.vampyras = tk.PhotoImage(file=self.images[3])
                    self.vampyras_image = tk.Label(self.root, image=self.vampyras, bg="#36393F")
                    self.vampyras_image.pack()
                    self.take_hp(10)
                if self.counter == 26:
                    self.vampyras_image.destroy()
                if self.counter == 28:
                    self.suo = tk.PhotoImage(file=self.images[4])
                    self.suo_image = tk.Label(self.root, image=self.suo, bg="#36393F")
                    self.suo_image.pack()
                    self.take_hp(10)
                if self.counter == 29:
                    self.suo_image.destroy()
                    self.suo = tk.PhotoImage(file=self.images[5])
                    self.suo_image = tk.Label(self.root, image=self.suo, bg="#36393F")
                    self.suo_image.pack()
                if self.counter == 30:
                    self.suo_image.destroy()
                if self.counter == 34:
                    self.cathing_pikachu = tk.PhotoImage(file=self.images[8])
                    self.cathing_pikachu_image = tk.Label(self.root, image=self.cathing_pikachu, bg="#36393F")
                    self.cathing_pikachu_image.pack()
                    self.heal_hp(35)
                if self.counter == 35:
                    self.cathing_pikachu_image.destroy()
                if self.counter == 37:
                    self.pikachu = tk.PhotoImage(file=self.images[9])
                    self.pikachu_image = tk.Label(self.root, image=self.pikachu, bg="#36393F")
                    self.pikachu_image.pack()
                if self.counter == 38:
                    self.pikachu_image.destroy()
                    self.pikachu = tk.PhotoImage(file=self.images[6])
                    self.pikachu_image = tk.Label(self.root, image=self.pikachu, bg="#36393F")
                    self.pikachu_image.pack()
                if self.counter == 39:
                    self.pikachu_image.destroy()
                self.counter += 1
            else:
                messagebox.showinfo("Game Over", "Game finished!")
                self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Game errored! You were at {self.counter} Report id: {e}")
            self.root.quit()

class GameIntro:
    def __init__(self, game):
        try:
            self.game = game

            self.root = tk.Tk()
            self.root.title("Game Intro")
            self.root.attributes('-fullscreen', True)  # Make the window full screen
            self.root.configure(bg="#36393F")

            self.title = tk.Label(self.root, text="Do not press the button game", font=("Monaco", 32), fg="#888", bg="#36393F")
            self.title.pack(pady=20)

            self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Monaco", 12), width=100, height=2, bg="green", fg="white")
            self.start_button.pack()
            self.start_button.pack_forget()  # Initially hide the button
            self.exit_game = tk.Button(self.root, text="Exit Game", command=self.exit_game, font=("Monaco", 12), width=100, height=2, bg="red", fg="white")
            self.exit_game.pack()
            self.exit_game.pack_forget()  # Initially hide the button
            # Show the button after 3 seconds
            self.root.after(3000, self.start_button.pack)
            self.root.after(3000, self.exit_game.pack)

            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Game errored! Report id: {e}")
            self.root.quit()

    def start_game(self):
        self.root.destroy()
        self.game.root.deiconify()

    def exit_game(self):
        self.root.quit()
        self.game.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = DoNotPressGame(root)
    root.withdraw()
    intro = GameIntro(game)