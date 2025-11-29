from nicegui import ui
from ui.base import Base
from model.game import Game

class PicsUI(Base):
        
    def __init__(self, game: Game ):
        self.game = game

    def draw(self):
        self.label_word = ui.label(self.game.hidden_word).classes("text-xl font-mono mt-4")
        self.omino = ui.image().bind_source_from(self.game, "frame", backward=lambda frame: Game.draw_hangman(frame, Game.DRAW_MODE_PICS)).classes('min-h-48 max-h-96 min-w-32 max-w-fit')
        
        self.label_correct = ui.label()
        self.letters_correct = ui.row()
        
        self.label_wrong = ui.label()
        self.letters_wrong = ui.row()

        ui.label("Inserisci una lettera:").classes("mt-6")
        
        self.letters_list = ui.row().classes("flex flex-wrap justify-center gap-2 w-full")
        with self.letters_list:
            self.chips = []
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                chip = ui.chip(letter, color="gray-200", text_color="black") \
                        .classes("cursor-pointer select-none text-lg px-3") \
                        .on_click(lambda l=letter: self.on_submit(l))
                self.chips.append(chip)    

    def update(self):
        self.label_word.text = self.game.hidden_word.upper()
        
        if len(self.game.correct_letters) > 0:
            self.label_correct.text = f"Lettere corrette"
            self.letters_correct.clear()
            with self.letters_correct:
                for letter in sorted(self.game.correct_letters):
                    ui.chip(letter.upper(), color='green').classes("select-none text-lg px-3")
        else:
            self.label_correct.text = ""
            self.letters_correct.clear()
            
        if len(self.game.wrong_letters) > 0:
            self.label_wrong.text = f"Lettere sbagliate"
            self.letters_wrong.clear()
            with self.letters_wrong:
                for letter in sorted(self.game.wrong_letters):
                    ui.chip(letter.upper(), color='red').classes("select-none text-lg px-3")
        else:
            self.label_wrong.text = ""
            self.letters_wrong.clear()

        for chip in self.chips:
            if chip.text.lower() in self.game.correct_letters + self.game.wrong_letters:
                self.disable_chip(chip.text)
            else:
                self.enable_chip(chip.text)

        self.handle_end_game()

    def handle_end_game(self):
        if self.game.is_won():
            ui.notify("🎉 Hai vinto!", color="green")
            self.disable_all_chips()
        elif self.game.is_lost():
            ui.notify(f"💀 Hai perso! La parola era: {self.game.word.upper()}", color="red")
            self.disable_all_chips()

    def on_submit(self, letter: str):
        result = self.game.try_letter(letter)

        if result == "duplicate":
            ui.notify("Hai già provato questa lettera!", color="red")
        # elif result == "ok":
            # ui.notify("✔️ Lettera corretta!", color="green")
        # elif result == "wrong":
            # ui.notify("❌ Lettera sbagliata!", color="red")

        # Aggiorna UI
        # self.update()

        # Controllo fine partita
        # self.handle_end_game()        

    def disable_chip(self, letter):
        for chip in self.chips:
            if chip.text == letter:
                chip.disable()
                chip.set_visibility(False)
                break     

    def enable_chip(self, letter):
        for chip in self.chips:
            if chip.text == letter:
                chip.enable()
                chip.set_visibility(True)
                break                  
            
    def disable_all_chips(self):
        for chip in self.chips:
            chip.disable()   
            chip.set_visibility(False)
            
    def enable_all_chips(self) :
        for chip in self.chips:
            chip.enable()  
            chip.set_visibility(True)  