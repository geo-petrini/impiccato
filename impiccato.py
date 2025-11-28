import os, sys
from nicegui import ui, binding, native
import random


def resource_path(relative_path):
    '''
    data loader per pyinstall
    infatti all'esecuzione pyinstall crea una cartella temporanea salvata in _MEIPASS
    '''
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ============================================================
# MODEL — Logica di gioco
# ============================================================

@binding.bindable_dataclass
class ImpiccatoGame:
    MAX_ERRORS = 10
    DRAW_MODE_PICS = 'DRAW_MODE_PICS'
    DRAW_MODE_TEXT = 'DRAW_MODE_TEXT'
    frame = 0

    def __init__(self, mode=DRAW_MODE_PICS, word_list_path=resource_path('data/parole.txt')):
        self.word_list_path = word_list_path
        self.mode = mode
        self.reset()

    def reset(self):
        self.word = self._choose_word()
        self.correct_letters = []
        self.wrong_letters = []
        self.hidden_word = self._mask_word()
        self.frame = ImpiccatoGame.draw_hamgman( len(self.wrong_letters), self.mode)

    # ---------------- LOGICA ----------------

    def _choose_word(self) -> str:
        with open(self.word_list_path) as fh:
            words = [w.strip() for w in fh.readlines() if len(w.strip()) > 3]
        return random.choice(words)

    def _mask_word(self) -> str:
        out = ""
        for c in self.word:
            out += (" " + c) if c in self.correct_letters else " _"
        return out

    def try_letter(self, letter: str) -> str:
        """Restituisce 'ok', 'duplicate' o 'wrong'."""
        letter = letter.lower()

        if letter in self.correct_letters or letter in self.wrong_letters:
            return "duplicate"

        if letter in self.word:
            self.correct_letters.append(letter)
            self.hidden_word = self._mask_word()
            return "ok"

        self.wrong_letters.append(letter)
        self.frame = ImpiccatoGame.draw_hamgman( len(self.wrong_letters), self.mode)
        return "wrong"

    def is_won(self) -> bool:
        return self.word == self.hidden_word.replace(" ", "")

    def is_lost(self) -> bool:
        return len(self.wrong_letters) >= self.MAX_ERRORS

    @staticmethod
    def draw_hamgman(errors: int, mode=DRAW_MODE_TEXT):
        if mode == ImpiccatoGame.DRAW_MODE_TEXT:
            return ImpiccatoGame._draw_hangman_text(errors)
        if mode == ImpiccatoGame.DRAW_MODE_PICS:
            return ImpiccatoGame._draw_hangman_pics(errors)
        

    @staticmethod
    def _draw_hangman_text(error: int) -> str:
        if error < 0: error = 0
        if error > 10: error = 10
       
        frames = [
            r"""
            
            
            
            
            
            """,
            r"""
            
            
            
            
_________
            r""",
            r"""
    |
    |
    |
    |
    |
____|____
            """,
            r"""
----
    |
    |
    |
    |
    |
____|____
            """,
            r"""
----
 |  |
    |
    |
    |
    |
____|____
            """,
            r"""
----
 |  |
 O  |
    |
    |
    |
____|____
            """,
            r"""
----
 |  |
_O  |
    |
    |
    |
____|____
            """,
            r"""
----
 |  |
_O_ |
    |
    |
    |
____|____
            """,
            r"""
----
 |  |
_O_ |
 |  |
    |
    |
____|____
            """,
            r"""
----
 |  |
_O_ |
 |  |
/   |
    |
____|____
            """,
            r"""
----
 |  |
_O_ |
 |  |
/ \ |
    |
____|____
            """,
        ]
        return frames[error]

    @staticmethod
    def _draw_hangman_pics(error: int):
        """
        Le immagini devono essere:
            media/00.png
            media/01.png
            ...
            media/10.png
        """
        if error < 0: error = 0
        if error > 10: error = 10

        filename = resource_path(f"media/{error:02}.png") #:02 formatta i numeri con leading zero

        if not os.path.exists(filename):
            return None
 
        return filename

# ============================================================
# VIEW/CONTROLLER — Interfaccia NiceGUI
# ============================================================

class ImpiccatoUI:
    icon = '🎮'
    title = "Gioco dell'Impiccato"
    
    def __init__(self):
        self.game = ImpiccatoGame()
        with ui.column().classes("items-center justify-center w-full"):
            self.draw_elements()

    def draw_elements(self):
        # Per debug
        # self.debug_word = ui.label(f"(debug) parola: {self.game.word}").classes("text-sm text-gray-400")

        self.label_word = ui.label(self.game.hidden_word).classes("text-xl font-mono mt-4")
        self.label_correct = ui.label()
        
        self.letters_correct = ui.row()
        
        self.label_wrong = ui.label()
        self.letters_wrong = ui.row()

        self.omino = ui.image().bind_source_from(self.game, "frame").classes('min-h-48 max-h-96 min-w-32 max-w-fit')

        ui.label("Inserisci una lettera:").classes("mt-6")
        
        self.letters_list = ui.row().classes("flex flex-wrap justify-center gap-2 w-full")
        with self.letters_list:
            self.chips = []
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                chip = ui.chip(letter, color="gray-200", text_color="black") \
                        .classes("cursor-pointer select-none text-lg px-3") \
                        .on_click(lambda l=letter: self.on_submit(l))
                self.chips.append(chip)            

        ui.button("Nuova Partita", on_click=self.new_game).classes("mt-4")
        
    # ---------------- EVENTI UI ----------------

    def disable_chip(self, letter):
        for chip in self.chips:
            if chip.text == letter:
                chip.disable()
                chip.set_visibility(False)
                break      
            
    def disable_all_chips(self):
        for chip in self.chips:
            chip.disable()   
            chip.set_visibility(False)
            
    def enable_all_chips(self) :
        for chip in self.chips:
            chip.enable()  
            chip.set_visibility(True)    
            
    def display_end_game(self):  
        if self.game.is_won():
            ui.notify("🎉 Hai vinto!", color="green")
            self.disable_all_chips()
        elif self.game.is_lost():
            ui.notify(f"💀 Hai perso! La parola era: {self.game.word.upper()}", color="red")
            self.disable_all_chips()
            
    def on_submit(self, letter: str):
        result = self.game.try_letter(letter)
        
        self.disable_chip(letter)

        if result == "duplicate":
            ui.notify("Hai già provato questa lettera!", color="red")
        # elif result == "ok":
            # ui.notify("✔️ Lettera corretta!", color="green")
        # elif result == "wrong":
            # ui.notify("❌ Lettera sbagliata!", color="red")

        # Aggiorna UI
        self.update_ui()

        # Controllo fine partita
        self.display_end_game()

    def update_ui(self):
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

        

    def new_game(self, _):
        self.game.reset()
        # self.debug_word.text = f"(debug) parola: {self.game.word}"
        self.enable_all_chips()
        self.update_ui()
        ui.notify("Nuova partita!", color="blue")


@ui.page('/')
def page():
    iui = ImpiccatoUI()

# ============================================================
# MAIN
# ============================================================

if __name__ in {"__main__", "__mp_main__"}:
    
    ui.run(
        reload=False, 
        native=True,  
        window_size=(400, 800), 
        fullscreen=False, 
        favicon=ImpiccatoUI.icon, 
        title=ImpiccatoUI.title,
        port=native.find_open_port()
        )



