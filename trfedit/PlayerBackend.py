from gi.repository import Gtk
from trf import Player

from .TreeViewPage import TreeViewPageBackend


class PlayerBackend(TreeViewPageBackend):
    def __init__(self, win):
        super().__init__(Gtk.ListStore(int, str, str, str, int, str, int, str, str, int), [
            ('Start Rank', None),
            ('Name', self.on_name_edited),
            ('Sex', self.on_sex_edited),
            ('Title', self.on_title_edited),
            ('Rating', self.on_rating_edited),
            ('Federation', self.on_fed_edited),
            ('ID', self.on_id_edited),
            ('Date of Birth', self.on_birthdate_edited),
            ('Points', self.on_points_edited),
            ('Rank', self.on_rank_edited)
        ])
        self.win = win

    def on_name_edited(self, widget, path, text):
        # TODO: on_name_edited
        pass
 
    def on_sex_edited(self, widget, path, text):
        # TODO: on_sex_edited
        pass

    def on_title_edited(self, widget, path, text):
        # TODO: on_title_edited
        pass

    def on_rating_edited(self, widget, path, text):
        # TODO: on_rating_edited
        pass

    def on_fed_edited(self, widget, path, text):
        # TODO: on_fed_edited
        pass

    def on_id_edited(self, widget, path, text):
        # TODO: on_id_edited
        pass

    def on_birthdate_edited(self, widget, path, text):
        # TODO: on_birthdate_edited
        pass

    def on_points_edited(self, widget, path, text):
        # TODO: on_points_edited
        pass

    def on_rank_edited(self, widget, path, text):
        # TODO: on_rank_edite
        pass

    def append_new_row(self):
        index = len(self.tournament.players)
        player = Player(name='New player', startrank=index+1)
        self.append_player_to_store(player)
        self.tournament.players.append(player)

        return index

    def append_player_to_store(self, player):
        self.store.append([
            player.startrank,
            player.name,
            player.sex,
            player.title,
            player.rating,
            player.fed,
            player.id,
            player.birthdate,
            format(player.points, '.1f'),
            player.rank
        ])

    def swap_rows(self, i1, i2):
        a = self.tournament.players[i1]
        b = self.tournament.players[i2]

        self.tournament.players[i1] = b
        self.tournament.players[i2] = a

        # TODO: Fix startranks in teams
        for player in self.tournament.players:
            for game in player.games:
                if game.startrank == a.startrank:
                    game.startrank = b.startrank
                elif game.startrank == b.startrank:
                    game.startrank = a.startrank

        t = a.startrank
        a.startrank = b.startrank
        b.startrank = t

        self.swap_store_rows(i1, i2)
        self.store[i1][0] = b.startrank
        self.store[i2][0] = a.startrank

    def remove_row_from_data(self, index):
        startrank = self.tournament.players[index].startrank
        del self.tournament.players[index]

        for player in self.tournament.players:
            player.games = list(filter(lambda g: g.startrank != startrank,
                                       player.games))

    def __len__(self):
        return len(self.tournament.players)

    def set_tournament(self, tournament):
        self.tournament = tournament

        self.store.clear()
        for player in tournament.players:
            self.append_player_to_store(player)
