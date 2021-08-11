import trf
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TournamentPage(Gtk.Box):
    spacing = 10

    def __init__(self, tournament):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=self.spacing)
        self.tournament = tournament

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.pack_start(self.listbox, True, True, 0)

        # TODO: process value change

        self.name_entry = self.add_entry(
            'Tournament Name:',
            tournament.name)
        self.city_entry = self.add_entry(
            'Tournament City:',
            tournament.city)
        self.federation_entry = self.add_entry(
            'Tournament Federation:',
            tournament.federation)
        self.startdate_entry = self.add_entry(
            'Tournament Start Date:',
            tournament.startdate)
        self.enddate_entry = self.add_entry(
            'Tournament End Date:',
            tournament.enddate)
        self.type_entry = self.add_entry(
            'Tournament Type:',
            tournament.type)
        self.chiefarbiter_entry = self.add_entry(
            'Tournament Chief Arbiter:',
            tournament.chiefarbiter)
        self.deputyarbiters_entry = self.add_entry(
            'Tournament Deputy Arbiters:',
            tournament.deputyarbiters)

    def add_entry(self, label, text):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_homogeneous(True)
        row.add(hbox)

        label = Gtk.Label(label=label, xalign=0)
        hbox.pack_start(label, True, True, self.spacing)

        entry = Gtk.Entry()
        entry.set_text(text)
        hbox.pack_start(entry, True, True, self.spacing)

        self.listbox.add(row)

        return entry


class TrfEditWindow(Gtk.Window):
    def __init__(self, tournament):
        super().__init__(title=f'{tournament.name} - trfedit')
        self.tournament = tournament

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.tournament_page = TournamentPage(tournament)
        self.notebook.append_page(self.tournament_page, Gtk.Label(label="Tournament"))

        # TODO:
        # rounddates: List[str] = field(default_factory=list) 
        # players: List[Player] = field(default_factory=list) 
        # teams: List[str] = field(default_factory=list) 
        # xx_fields: Dict[str, str] = field(default_factory=dict)

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label(label="A page with an image for a Title."))
        self.notebook.append_page(
            self.page2, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        )


with open('example1.trf') as f:
    tour = trf.load(f)
win = TrfEditWindow(tour)
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
