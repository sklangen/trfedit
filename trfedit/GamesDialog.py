from gi.repository import Gtk
from trf import Game

from .TreeView import TreeViewBackend, TreeView, TextColumn, ComboColumn


color_store = Gtk.ListStore(str, str)
color_store.append([' ', ' '])
color_store.append(['w', 'White'])
color_store.append(['b', 'Black'])


class GamesBackend(TreeViewBackend):
    def __init__(self, win, index):
        super().__init__(Gtk.ListStore(int, int, str, str), [
            TextColumn('Round'),
            TextColumn('Opponent', self.on_opponent_changed),
            ComboColumn('Color', color_store, self.on_color_changed),
            TextColumn('Result', self.on_result_changed)
        ])
        self.win = win
        self.index = index

        self.player = win.tournament.players[index]

        for i, game in enumerate(self.player.games):
            self.append_game_to_store(i+1, game)

    def append_game_to_store(self, round, game):
        self.store.append([
            round,
            game.startrank,
            self.get_color_name(game.color),
            game.result
        ])

    def get_color_name(self, color):
        if color in 'wW':
            return 'White'
        if color in 'bB':
            return 'Black'
        return ''

    def on_opponent_changed(self, widget, path, text):
        pass

    def on_color_changed(self, widget, path, option, *a):
        # TODO: update opponents color
        key, value = color_store[option]
        self.player.games[int(path)].color = key
        self.store[path][2] = value
        self.win.on_unsaved_changes()

    def on_result_changed(self, widget, path, text):
        pass

    def append_new_row(self):
        round = len(self.store)
        self.append_game_to_store(round, Game())
        return round

    def swap_rows(self, i1, i2):
        self.swap_store_rows(i1, i2)

    def remove_row_from_data(self, index):
        pass

    def __len__(self):
        return len(self.store)


class GamesDialog(Gtk.Dialog):
    def __init__(self, win, index):
        super().__init__(transient_for=win, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(640, 480)

        self.backend = GamesBackend(win, index)
        self.set_title(f'Games of {self.backend.player.name}')

        self.treeview = TreeView(win, self.backend)

        box = self.get_content_area()
        box.add(self.treeview)

        self.show_all()
