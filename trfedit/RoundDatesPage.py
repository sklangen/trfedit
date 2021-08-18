from gi.repository import Gtk
from datetime import date


DATE_FORMAT = '%y/%m/%d'


class RoundDatesPage(Gtk.Box):
    def __init__(self, on_unsaved_changes):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.on_unsaved_changes = on_unsaved_changes
        self.tournament = None

        self.scroll = Gtk.ScrolledWindow()
        self.store = Gtk.ListStore(int, str)
        self.treeview = Gtk.TreeView(model=self.store)

        self.scroll.set_vexpand(True)

        for i, column_title in enumerate(["Round", "Date"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        self.scroll.add(self.treeview)
        self.pack_start(self.scroll, True, True, 0)

        action_bar = Gtk.ActionBar()

        new_round_button = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        new_round_button.connect('clicked', self.on_new_rounddate)
        action_bar.add(new_round_button)

        self.pack_start(action_bar, False, False, 0)

    def on_new_rounddate(self, widget):
        round = len(self.tournament.rounddates)
        today = date.today().strftime(DATE_FORMAT)

        self.store.append([round+1, today])
        self.tournament.rounddates.append(today)

        self.treeview.set_cursor(round)
        self.on_unsaved_changes()

    def set_tournament(self, tournament):
        self.tournament = tournament

        for i, date in enumerate(tournament.rounddates):
            self.store.append([i+1, date])
