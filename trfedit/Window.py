from gi.repository import Gtk

from .TournamentPage import TournamentPage
from .MenuBar import MenuBar


class Window(Gtk.Window):
    def __init__(self, tournament):
        super().__init__(title=f'{tournament.name} - trfedit')
        self.tournament = tournament

        menu_bar = MenuBar()
        self.add_accel_group(menu_bar.agr)

        menu_bar.add_menu('_File', [
            (Gtk.STOCK_NEW,     '<Control>N',   self.on_file_new),
            (Gtk.STOCK_OPEN,    '<Control>O',   self.on_file_open),
            (Gtk.STOCK_SAVE,    '<Control>S',   self.on_file_save),
            (Gtk.STOCK_SAVE_AS, None,           self.on_file_save_as),
            (Gtk.STOCK_QUIT,    '<Control>Q',   Gtk.main_quit)
        ])

        self.notebook = Gtk.Notebook()
        self.tournament_page = TournamentPage(tournament)
        self.notebook.append_page(
            self.tournament_page,
            Gtk.Label(label="Tournament"))

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(menu_bar, False, False, 0)
        vbox.pack_start(self.notebook, False, False, 0)

        self.add(vbox)

        # TODO:
        # rounddates: List[str] = field(default_factory=list)
        # players: List[Player] = field(default_factory=list)
        # teams: List[str] = field(default_factory=list)
        # xx_fields: Dict[str, str] = field(default_factory=dict)

    def on_file_new(self, widget):
        print('NEW FILE!')

    def on_file_open(self, widget):
        print('OPEN FILE!')

    def on_file_save(self, widget):
        print('SAVE FILE!')

    def on_file_save_as(self, widget):
        print('SAVE FILE AS!')
