from gi.repository import Gtk


class MenuBar(Gtk.MenuBar):
    def __init__(self):
        super().__init__()
        self.agr = Gtk.AccelGroup()

    def add_menu(self, label, items):
        submenu = Gtk.Menu()
        menu = Gtk.MenuItem.new_with_mnemonic(label)
        menu.set_submenu(submenu)

        for stock_id, accelerator, callback in items:
            item = Gtk.ImageMenuItem.new_from_stock(stock_id)
            item.connect('activate', callback)

            if accelerator is not None:
                key, mod = Gtk.accelerator_parse(accelerator)
                item.add_accelerator('activate', self.agr,
                                     key, mod,
                                     Gtk.AccelFlags.VISIBLE)

            submenu.append(item)

        self.append(menu)
