from nicegui import ui, native

from ui.pics import PicsUI
from ui.text import TextUI
from model.game import Game


class Impiccato:
    icon = '🎮'
    title = "Gioco dell'Impiccato"
    
    def __init__(self):
        self.game = Game()
        self.game.on_change.subscribe(self.watch)
        self.dark = ui.dark_mode()
        self.dark.value = None
        self.renderers = {}

        with ui.column().classes("items-center justify-center w-full"):
            self.draw_elements()

    def draw_elements(self):
        # Per debug
        # self.debug_word = ui.label(f"(debug) parola: {self.game.word}").classes("text-sm text-gray-400")
        # self.mode_button = ui.button(icon='contrast', on_click=self.toggle_mode).classes("fixed top-1 left-1 z-50")
        ui.button("Nuova Partita", on_click=self.new_game).classes("top-1 right-1 fixed z-50")

        with ui.splitter(value=8, limits=(92, 8)).classes('w-full select-none mt-8') as splitter:
            with splitter.before:
                self.tabs = ui.tabs().props('vertical').classes('w-full')
                with self.tabs:
                    pics = ui.tab('pics', label='', icon='monitor')
                    text = ui.tab('text', label='', icon='terminal')
                    cfg = ui.tab('cfg', label='', icon='settings')
            with splitter.after:
                with ui.tab_panels(self.tabs, value=pics).props('vertical').classes('w-full h-full'):
                    with ui.tab_panel(pics).classes("items-center justify-center w-full"):
                        self.renderers['pics'] = PicsUI(self.game)
                        self.renderers['pics'].draw()
                    with ui.tab_panel(text).classes():
                        self.renderers['text'] = TextUI(self.game)
                        self.renderers['text'].draw()
                    with ui.tab_panel(cfg).classes():
                        ui.label('Tema').classes('mt-4')
                        self.mode_button = ui.toggle({'auto':'Auto', 'dark':'Scuro', 'light':'Chiaro'}, value='auto', on_change=self.toggle_mode).classes("m-4")
                        # with ui.teleport(f'#{self.mode_button.html_id}')

    # ---------------- EVENTI UI ----------------

    def watch(self, data):
        # print(f'game event: {data}')
        for renderer in self.renderers.values():
            # print(f'updating renderer: {renderer}')
            renderer.update()

    def new_game(self, _):
        self.game.reset()
        # self.debug_word.text = f"(debug) parola: {self.game.word}"
        for renderer in self.renderers.values():
            renderer.update()
        ui.notify("Nuova partita!", color="blue")

    def toggle_mode(self, event):     
        print(f'{event.sender.props}')  
        if event.value == 'auto':
            self.dark.value = None
        if event.value == 'light':
            self.dark.value = False
        if event.value == 'dark':
            self.dark.value = True
        

        

        # if event.value == 'pics':
        #     self.dark.disable()
        # else:
        #     self.dark.enable()


@ui.page('/')
def page():
    iui = Impiccato()

# ============================================================
# MAIN
# ============================================================

if __name__ in {"__main__", "__mp_main__"}:
    
    ui.run(
        # reload=False, 
        # native=True,  
        # window_size=(400, 800), 
        # fullscreen=False, 
        favicon=Impiccato.icon, 
        title=Impiccato.title,
        port=native.find_open_port()
        )



