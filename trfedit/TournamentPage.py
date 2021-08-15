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
