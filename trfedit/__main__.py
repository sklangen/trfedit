import gi
import locale
import sys
import warnings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .Window import Window


def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    locale.setlocale(locale.LC_ALL, locale='en_US')

    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]

    win = Window(path)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
