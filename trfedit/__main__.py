import trf
import gi
import warnings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .Window import Window


def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with open('example1.trf') as f:
        tour = trf.load(f)

    win = Window(tour)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
