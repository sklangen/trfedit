from abc import ABC, abstractmethod
from gi.repository import Gtk, Gdk


class TreeViewPageBackend(ABC):
    def __init__(self, store, columns):
        self.store = store
        self.columns = columns

    @abstractmethod
    def __len__(self):
        pass

    def remove_row(self, index):
        iter = self.store[index].iter
        self.store.remove(iter)
        self.remove_row_from_data(index)

    @abstractmethod
    def remove_row_from_data(self, index):
        pass

    @abstractmethod
    def swap_rows(self, index):
        pass

    @abstractmethod
    def append_new_row(self):
        pass


class TreeViewPage(Gtk.Box):
    def __init__(self, win, backend):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.win = win
        self.backend = backend

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True)

        self.treeview = Gtk.TreeView(model=self.backend.store)
        self.treeview.connect('key-press-event', self.on_key_typed)

        for i, (title, on_edited) in enumerate(self.backend.columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i)
            self.treeview.append_column(column)

            if on_edited is not None:
                renderer.set_property('editable', True)
                renderer.connect('edited', on_edited)

        self.scroll.add(self.treeview)
        self.pack_start(self.scroll, True, True, 0)

        action_bar = Gtk.ActionBar()

        new_button = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        new_button.connect('clicked', self.on_new)
        action_bar.add(new_button)

        remove_button = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        remove_button.connect('clicked', self.on_remove)
        action_bar.add(remove_button)

        up_button = Gtk.Button.new_from_stock(Gtk.STOCK_GO_UP)
        up_button.connect('clicked', self.on_up)
        action_bar.add(up_button)

        down_button = Gtk.Button.new_from_stock(Gtk.STOCK_GO_DOWN)
        down_button.connect('clicked', self.on_down)
        action_bar.add(down_button)

        self.pack_start(action_bar, False, False, 0)

    def on_key_typed(self, widget, event):
        if event.keyval in (Gdk.KEY_Delete, Gdk.KEY_BackSpace):
            self.remove_row()

    def on_remove(self, widget):
        self.remove_row()

    def remove_row(self):
        index = self.get_selected_row()
        if index is not None:
            self.backend.remove_row(index)
            self.win.on_unsaved_changes()

    def on_down(self, widget):
        self.move_row(+1)

    def on_up(self, widget):
        self.move_row(-1)

    def move_row(self, dir):
        index = self.get_selected_row()
        if index is not None:
            other = (index+dir) % len(self.backend)
            self.backend.swap_rows(index, other)

            self.treeview.set_cursor(other)
            self.win.on_unsaved_changes()

    def on_new(self, widget):
        index = self.backend.append_new_row()
        self.treeview.set_cursor(index)
        self.win.on_unsaved_changes()

    def get_selected_row(self):
        path, _ = self.treeview.get_cursor()
        if path is None:
            return None
        return path.get_indices()[0]
