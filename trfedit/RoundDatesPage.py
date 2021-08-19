from gi.repository import Gtk, Gdk

import datetime
import re


DATE_FORMAT = '%y/%m/%d'


class RoundDatesPage(Gtk.Box):
    def __init__(self, win):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.win = win
        self.tournament = None

        self.scroll = Gtk.ScrolledWindow()
        self.store = Gtk.ListStore(int, str)
        self.treeview = Gtk.TreeView(model=self.store)

        self.scroll.set_vexpand(True)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Round', renderer, text=0)
        self.treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.on_round_edited)
        column = Gtk.TreeViewColumn('Date', renderer, text=1)
        self.treeview.append_column(column)

        self.scroll.add(self.treeview)
        self.pack_start(self.scroll, True, True, 0)

        self.treeview.connect('key-press-event', self.on_key_typed)

        action_bar = Gtk.ActionBar()

        new_button = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        new_button.connect('clicked', self.on_new_rounddate)
        action_bar.add(new_button)

        remove_button = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        remove_button.connect('clicked', self.on_remove_rounddate)
        action_bar.add(remove_button)

        self.pack_start(action_bar, False, False, 0)

    def on_remove_rounddate(self, widget):
        self.remove_round_date()

    def remove_round_date(self):
        path, _ = self.treeview.get_cursor()
        if path is not None:
            i_date_date_date_date_datendex = path.get_indices()[0]
            iter = self.store.get_iter(path)

            self.store.remove(iter)
            del self.tournament.rounddates[index]

            self.on_unsaved_changes()

    def on_round_edited(self, widget, path, text):
        if re.search('\\s+', text):
            self.win.show_error_dialog('Invalid round date',
                                       'No whitespace allowed in round dates')
            return

        self.tournament.rounddates[int(path)] = text
        self.store[path][1] = text
        self.win.on_unsaved_changes()

    def on_key_typed(self, widget, event):
        if event.keyval in (Gdk.KEY_Delete, Gdk.KEY_BackSpace):
            self.remove_round_date()

    def on_new_rounddate(self, widget):
        round = len(self.tournament.rounddates)
        today = datetime.date.today().strftime(DATE_FORMAT)

        self.store.append([round+1, today])
        self.tournament.rounddates.append(today)

        self.treeview.set_cursor(round)
        self.win.on_unsaved_changes()

    def set_tournament(self, tournament):
        self.tournament = tournament

        self.store.clear()

        for i, date in enumerate(tournament.rounddates):
            self.store.append([i+1, date])
