from gi.repository import Gtk
from trf import Game

from .TreeView import TreeViewBackend, TreeView, TextColumn, ComboColumn


class ComboStore(Gtk.ListStore):
    def __init__(self, types, selectables):
        super().__init__(*types)

        for selectable in selectables:
            self.append(selectable)

    def get_name(self, key):
        for option in self:
            if option[0] == key:
                return option[1]
        return ''


class OppositeComboStore(ComboStore):
    def __init__(self, selectables):
        super().__init__((str, str, str), selectables)

    def get_opposite(self, key):
        for k, _, opposite in self:
            if k == key:
                return opposite
        return None


def make_player_store(players):
    players = sorted(players, key=lambda p: p.name)
    return ComboStore(
        (int, str),
        [None, ''] + [[p.startrank, p.name] for p in players])


color_store = OppositeComboStore([
    [' ', '', None],
    ['w', 'White', 'b'],
    ['b', 'Black', 'w']
])


result_store = OppositeComboStore([
    [' ', '', None],
    ['1', 'Win', '0'],
    ['=', 'Draw', '='],
    ['0', 'Loss', '1'],
    ['w', 'Win but no move played', 'l'],
    ['d', 'Draw but no move played', 'd'],
    ['l', 'Loss but no move played', 'w'],
    ['+', 'Forfeit win', '-'],
    ['-', 'Forfeit loss', '+'],
    ['h', 'Half point bye', None],
    ['f', 'Full point bye', None],
    ['u', 'Unpaired', None]
])


class GamesBackend(TreeViewBackend):
    def __init__(self, win, index):
        player_store = make_player_store(win.tournament.players)
        super().__init__(Gtk.ListStore(int, str, str, str), [
            TextColumn('Round'),
            ComboColumn('Opponent', player_store, self.on_opponent_changed),
            ComboColumn('Color', color_store, self.on_color_changed),
            TextColumn('Result', self.on_result_changed)
        ])
        self.win = win
        self.index = index

        self.player_store = player_store

        self.player = win.tournament.players[index]

        for i, game in enumerate(self.player.games):
            self.append_game_to_store(game)

    def append_game_to_store(self, game):
        self.store.append([
            game.round,
            self.player_store.get_name(game.startrank),
            color_store.get_name(game.color),
            game.result
        ])

    def on_opponent_changed(self, widget, path, option):
        startrank, name = self.player_store[option]
        index = int(path)
        game = self.player.games[index]

        old_opponent = self.get_player_by_startrank(game.startrank)
        if old_opponent is not None:
            old_opponent.games[index] = self.make_blank_game(game.round)

        new_opponent = self.get_player_by_startrank(startrank)
        if new_opponent is not None:
            new_opponent.games[index] = self.make_blank_game(game.round)
            new_opponent.games[index].startrank = self.player.startrank

        game.startrank = startrank
        self.store[path][1] = name

        game.color = ' '
        self.store[path][2] = ''

        game.result = ' '
        self.store[path][3] = ''

        self.win.on_unsaved_changes()

    def on_color_changed(self, widget, path, option):
        key, value, opposite = color_store[option]
        index = int(path)
        game = self.player.games[index]

        game.color = key
        self.store[path][2] = value

        if opposite is not None:
            opponent = self.get_player_by_startrank(game.startrank)
            if opponent is not None:
                opponent.games[index].color = opposite

        self.win.on_unsaved_changes()

    def get_player_by_startrank(self, startrank):
        return next(filter(lambda p: p.startrank == startrank,
                           self.win.tournament.players), None)

    def on_result_changed(self, widget, path, text):
        pass

    def append_new_row(self):
        round = len(self.store)
        self.append_game_to_store(self.make_blank_game(round))
        return round

    def make_blank_game(self, round):
        return Game(
            startrank=None,
            color=' ',
            result=' ',
            round=round)

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
