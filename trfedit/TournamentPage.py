from gi.repository import Gtk


class TournamentPage(Gtk.Box):
    spacing = 10

    def __init__(self, tournament, on_unsaved_changes):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=self.spacing)
        self.tournament = tournament
        self.on_unsaved_changes = on_unsaved_changes

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.pack_start(self.listbox, True, True, 0)

        # TODO: process value change

        self.name_entry = self.add_entry(
            'Tournament Name:',
            tournament.name,
            self.on_name_changed)

        self.city_entry = self.add_entry(
            'Tournament City:',
            tournament.city,
            self.on_city_changed)

        self.federation_entry = self.add_entry(
            'Tournament Federation:',
            tournament.federation,
            self.on_federation_changed)

        self.startdate_entry = self.add_entry(
            'Tournament Start Date:',
            tournament.startdate,
            self.on_startdate_changed)

        self.enddate_entry = self.add_entry(
            'Tournament End Date:',
            tournament.enddate,
            self.on_enddate_changed)

        self.type_entry = self.add_entry(
            'Tournament Type:',
            tournament.type,
            self.on_type_changed)

        self.chiefarbiter_entry = self.add_entry(
            'Tournament Chief Arbiter:',
            tournament.chiefarbiter,
            self.on_chiefarbiter_changed)

        self.deputyarbiters_entry = self.add_entry(
            'Tournament Deputy Arbiters:',
            tournament.deputyarbiters,
            self.on_deputyarbiters_changed)

    def add_entry(self, label, text, on_changed):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_homogeneous(True)
        row.add(hbox)

        label = Gtk.Label(label=label, xalign=0)
        hbox.pack_start(label, True, True, self.spacing)

        entry = Gtk.Entry()
        entry.set_text(text)
        entry.connect('changed', on_changed)
        hbox.pack_start(entry, True, True, self.spacing)

        self.listbox.add(row)

        return entry

    def on_name_changed(self, widget):
        self.tournament.name = widget.get_text()
        self.on_unsaved_changes()

    def on_city_changed(self, widget):
        self.tournament.city = widget.get_text()
        self.on_unsaved_changes()

    def on_federation_changed(self, widget):
        self.tournament.federation = widget.get_text()
        self.on_unsaved_changes()

    def on_startdate_changed(self, widget):
        self.tournament.startdate = widget.get_text()
        self.on_unsaved_changes()

    def on_enddate_changed(self, widget):
        self.tournament.enddate = widget.get_text()
        self.on_unsaved_changes()

    def on_type_changed(self, widget):
        self.tournament.type = widget.get_text()
        self.on_unsaved_changes()

    def on_chiefarbiter_changed(self, widget):
        self.tournament.chiefarbiter = widget.get_text()
        self.on_unsaved_changes()

    def on_deputyarbiters_changed(self, widget):
        self.tournament.deputyarbiters = widget.get_text()
        self.on_unsaved_changes()
