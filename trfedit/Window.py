from gi.repository import Gtk
import traceback
import trf

from .TournamentPage import TournamentPage
from .RoundDatesPage import RoundDatesPage
from .MenuBar import MenuBar


class Window(Gtk.Window):
    def __init__(self):
        super().__init__(title='trfedit')
        self.tournament = None
        self.tournament_path = None

        menu_bar = MenuBar()
        self.add_accel_group(menu_bar.agr)

        self.unsaved_changes = False

        self.notebook = Gtk.Notebook()

        self.tournament_page = TournamentPage(self.on_unsaved_changes)
        self.notebook.append_page(
            self.tournament_page,
            Gtk.Label(label='Tournament'))

        self.rounddates_page = RoundDatesPage(self)
        self.notebook.append_page(
            self.rounddates_page,
            Gtk.Label(label='Round Dates'))

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(menu_bar, False, False, 0)
        vbox.pack_start(self.notebook, True, True, 0)

        self.add(vbox)

        self.connect('delete-event', self.on_quit)

        # TODO:
        # rounddates: List[str] = field(default_factory=list)
        # players: List[Player] = field(default_factory=list)
        # teams: List[str] = field(default_factory=list)
        # xx_fields: Dict[str, str] = field(default_factory=dict)

        menu_bar.add_menu('_File', [
            (Gtk.STOCK_NEW,     '<Control>N',           self.on_file_new),
            (Gtk.STOCK_OPEN,    '<Control>O',           self.on_file_open),
            (Gtk.STOCK_SAVE,    '<Control>S',           self.on_file_save),
            (Gtk.STOCK_SAVE_AS, '<Shift><Control>S',    self.on_file_save_as),
            (Gtk.STOCK_QUIT,    '<Control>Q',           self.on_quit)
        ])

        menu_bar.add_menu('Round Dates', [
            # TODO: This is not a "stock" action
            (Gtk.STOCK_NEW, '<Control>R',   self.rounddates_page.on_new_rounddate)
        ])

    def on_file_new(self, widget):
        self.ensure_changes_saved()

        path = self.ask_for_tournament_path()
        if path is not None:
            self.tournament_path = path
            self.set_tournament_to_new_tournament()
            self.update_title()

    def ensure_changes_saved(self):
        while self.unsaved_changes:
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
            else:
                self.unsaved_changes = False

            dialog.destroy()

    def update_title(self):
        self.set_title(self.tournament_path + ' - trfedit')

    def on_file_open(self, widget):
        self.ensure_changes_saved()

        path = self.ask_for_tournament_path()
        if path is not None:
            self.set_tournament_by_path(path)

    def on_file_save(self, widget):
        self.save_tournament(self.tournament_path)

    def on_file_save_as(self, widget):
        self.save_tournament(None)

    def save_tournament(self, path):
        if path is None:
            path = self.ask_for_tournament_path()

        if path is None:
            return

        try:
            with open(path, 'w') as f:
                trf.dump(f, self.tournament)
        except Exception as e:
            self.show_error_dialog('Error writing tournament', str(e))
            traceback.print_exc()
            return

        self.tournament_path = path
        self.unsaved_changes = False

    def ask_for_tournament_path(self):
        path = None

        dialog = Gtk.FileChooserDialog(
            'Please choose a file', self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()

        dialog.destroy()
        return path

    def show_error_dialog(self, title, secondary_text):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            text=title)

        dialog.format_secondary_text(secondary_text)
        dialog.run()

        dialog.destroy()

    def on_unsaved_changes(self):
        self.unsaved_changes = True

    def on_quit(self, widget, event=None):
        self.quit()

    def quit(self):
        self.ensure_changes_saved()
        Gtk.main_quit()

    def set_tournament(self, tournament):
        self.tournament = tournament
        self.tournament_page.set_tournament(tournament)
        self.rounddates_page.set_tournament(tournament)
        self.tournament_path = None

    def set_tournament_to_new_tournament(self):
        self.set_tournament(trf.Tournament(name='Unnamed Tournament'))

    def set_tournament_by_path(self, path):
        try:
            with open(path, 'r') as f:
                tour = trf.load(f)

            self.set_tournament(tour)
            self.tournament_path = path
            self.update_title()
        except Exception as e:
            self.show_error_dialog('Error reading tournament', str(e))
            traceback.print_exc()

            if self.tournament is None:
                self.set_tournament_to_new_tournament()
