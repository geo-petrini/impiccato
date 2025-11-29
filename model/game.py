import os
import sys
import random

from nicegui import binding
# ============================================================
# MODEL — Logica di gioco
# ============================================================

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

class Event:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def unsubscribe(self, callback):
        self.subscribers.remove(callback)

    def nofify(self, *args, **kwargs):
        for callback in self.subscribers:
            callback(*args, **kwargs)


@binding.bindable_dataclass
class Game:
    MAX_ERRORS = 10
    DRAW_MODE_PICS = 'DRAW_MODE_PICS'
    DRAW_MODE_TEXT = 'DRAW_MODE_TEXT'

    STATUS_NEW = 'new'
    STATUS_PLAYING = 'playing'
    STATUS_WON = 'won'
    STATUS_LOST = 'lost'  

    def __init__(self, word_list_path=resource_path('data/parole.txt')):
        self.word_list_path = word_list_path
        self.on_change = Event()
        self.reset()

    def reset(self):
        self.word = self._choose_word()
        self.correct_letters = []
        self.wrong_letters = []
        self.hidden_word = self._mask_word()
        self.on_change.nofify( {'status':self.STATUS_NEW} )

    @property
    def frame(self):
        return len(self.wrong_letters)
    
    # @property
    # def status(self):
    #     if self.is_won():
    #         return self.STATUS_WON
    #     elif self.is_lost():
    #         return self.STATUS_LOST
    #     elif len(self.correct_letters + self.wrong_letters) == 0:
    #         return self.STATUS_NEW
    #     else:
    #         return self.STATUS_PLAYING
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
        result = None

        if letter in self.correct_letters or letter in self.wrong_letters:
            result="duplicate"

        elif letter in self.word:
            self.correct_letters.append(letter)
            self.hidden_word = self._mask_word()
            result = "ok"
        else:
            self.wrong_letters.append(letter)
            result = "wrong"

        self.on_change.nofify( {'tried':letter, 'result':result, 'status':self.STATUS_PLAYING} )
        return result

    def is_won(self) -> bool:
        condition = self.word == self.hidden_word.replace(" ", "")
        # self.on_change.nofify( {'status':self.STATUS_WON if condition else self.STATUS_PLAYING} ) 
        return condition

    def is_lost(self) -> bool:
        condition = len(self.wrong_letters) >= self.MAX_ERRORS
        # self.on_change.nofify( {'status':self.STATUS_LOST if condition else self.STATUS_PLAYING} )
        return condition

    @staticmethod
    def draw_hangman(errors: int, mode=DRAW_MODE_TEXT):
        if mode == Game.DRAW_MODE_TEXT:
            return Game._draw_hangman_text(errors)
        if mode == Game.DRAW_MODE_PICS:
            return Game._draw_hangman_pics(errors)
        

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
    _____
    |/  
    |   
    |   
    |   
    |
____|____
            """,
            r"""
    _____
    |/  |
    |   
    |   
    |   
    |
____|____
            """,
            r"""
    _____
    |/  |
    |   O
    |   
    |   
    |
____|____
            """,
            r"""
    _____
    |/  |
    |  _O
    |   
    |   
    |
____|____
            """,
            r"""
    _____
    |/  |
    |  _O_
    |   
    |   
    |
____|____
            """,
            r"""
    _____
    |/  |
    |  _O_
    |   |
    |   
    |
____|____
            """,
            r"""
    _____
    |/  |
    |  _O_
    |   |
    |  / 
    |
____|____
            """,
            r"""
    _____
    |/  |
    |  _O_
    |   |
    |  / \
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


