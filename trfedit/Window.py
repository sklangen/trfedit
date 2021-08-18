from gi.repository import Gtk
import trf

from .TournamentPage import TournamentPage
from .MenuBar import MenuBar


class Window(Gtk.Window):
    def __init__(self, tournament, tournament_path=None):
        super().__init__(title=f'{tournament.name} - trfedit')
        self.tournament = tournament
        self.tournament_path = tournament_path

        menu_bar = MenuBar()
        self.add_accel_group(menu_bar.agr)

        self.unsaved_changes = False

        menu_bar.add_menu('_File', [
            (Gtk.STOCK_NEW,     '<Control>N',   self.on_file_new),
            (Gtk.STOCK_OPEN,    '<Control>O',   self.on_file_open),
            (Gtk.STOCK_SAVE,    '<Control>S',   self.on_file_save),
            (Gtk.STOCK_SAVE_AS, None,           self.on_file_save_as),
            (Gtk.STOCK_QUIT,    '<Control>Q',   self.on_quit)
        ])

        self.notebook = Gtk.Notebook()
        self.tournament_page = TournamentPage(tournament, self.on_unsaved_changes)
        self.notebook.append_page(
            self.tournament_page,
            Gtk.Label(label='Tournament'))

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(menu_bar, False, False, 0)
        vbox.pack_start(self.notebook, False, False, 0)

        self.add(vbox)

        self.connect('delete-event', self.on_quit)

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
        self.save_tournament(self.tournament_path)

    def on_file_save_as(self, widget):
        self.save_tournament(None)

    def save_tournament(self, path):
        if path is None:
            dialog = Gtk.FileChooserDialog(
                'Please choose a file', self,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                path = dialog.get_filename()

            dialog.destroy()

        if path is None:
            return

        try:
            with open(path, 'w') as f:
                trf.dump(f, self.tournament)
        except Exception as e:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text='Error saving tournament')

            dialog.format_secondary_text(str(e))
            dialog.run()

            dialog.destroy()
            raise e

        self.tournament_path = path
        self.unsaved_changes = False

    def on_unsaved_changes(self):
        self.unsaved_changes = True

    def on_quit(self, widget, event=None):
        self.quit()

    def quit(self):
        if self.unsaved_changes:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text='Unsaved changes may be lost')

            dialog.format_secondary_text(
                'Do you want to save before exiting?')

            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                self.save_tournament(self.tournament_path)

            dialog.destroy()

        Gtk.main_quit()
