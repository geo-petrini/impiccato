from nicegui import ui
from ui.base import Base
from model.game import Game

class TextUI(Base):
    def __init__(self, game: Game ):
        self.game = game

    def draw(self):
        self.log = ui.log().classes("w-full min-h-80")
        self.log.push(self.game.hidden_word.upper())
        self.log.push('')
        self.log.push(self.game.draw_hangman(self.game.frame, Game.DRAW_MODE_TEXT), classes='text-blue')
        self.log.push('')
        # self.log.push(f'Lettere possibili: {", ".join(self.list_available_letters())}', classes='text-gray-600')
        self.input_letter = ui.input(placeholder="Lettera").classes("w-24").on('keydown.enter', self.on_submit).on_value_change(self.on_type)
        # self.input_letter = ui.input(placeholder="Lettera", validation={'Lunghezza non valida': lambda value: len(value) == 1}).classes("w-24").on('keydown.enter', self.on_submit).on_value_change(self.on_type)

    def update(self):
        self.log.clear()
        self.log.push(self.game.hidden_word.upper())
        self.log.push(' ')
        self.log.push( self.game.draw_hangman(self.game.frame, Game.DRAW_MODE_TEXT), classes='text-blue')
        if len(self.game.correct_letters) > 0:
            self.log.push(f"Lettere corrette: {', '.join(sorted([l.upper() for l in self.game.correct_letters]))}", classes='text-green')
        if len(self.game.wrong_letters) > 0:
            self.log.push(f"Lettere sbagliate: {', '.join(sorted([l.upper() for l in self.game.wrong_letters]))}", classes='text-red')
        # self.log.push(f'Lettere possibili: {", ".join(self.list_available_letters())}', classes='text-gray-600')

        # Controllo fine partita
        self.handle_end_game()    

    def list_available_letters(self):
        used_letters = self.game.correct_letters + self.game.wrong_letters
        all_letters = [chr(c) for c in range(ord('a'), ord('z')+1)]
        available_letters = [l.upper() for l in all_letters if l not in used_letters]
        return available_letters

    def on_type(self, event):
        # print(f'{event}')
        text = event.value.lower()
        if len(text) > 1:
            text = text[-1]

        if not text.isalpha():
            text = ''

        if text in self.game.correct_letters + self.game.wrong_letters:
            ui.notify(f"Hai già provato la lettera {text}!", color="red")
            text = ''
        self.input_letter.set_value(text)
        self.input_letter.update()


    def on_submit(self, event):
        letter = self.input_letter.value.lower()
        if len(letter) != 1 or not letter.isalpha():
            ui.notify("Inserisci una singola lettera valida!", color="red")
            self.input_letter.value = ""
            return

        result = self.game.try_letter(letter)

        if result == "duplicate":
            ui.notify("Hai già provato questa lettera!", color="red")
        # elif result == "ok":
            # ui.notify("✔️ Lettera corretta!", color="green")
        # elif result == "wrong":
            # ui.notify("❌ Lettera sbagliata!", color="red")

        # Aggiorna UI
        # self.update()
        self.input_letter.value = ""

        
    def handle_end_game(self):
        if self.game.is_won():
            ui.notify("🎉 Hai vinto!", color="green")
            self.input_letter.disable()
        elif self.game.is_lost():
            ui.notify(f"💀 Hai perso! La parola era: {self.game.word.upper()}", color="red")
            self.input_letter.disable()        