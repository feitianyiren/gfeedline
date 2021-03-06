from gi.repository import Gtk
from ..constants import SHARED_DATA_FILE


class DialogBase(object):

    GLADED = ''
    DIALOG = ''

    def __init__(self, parent, liststore_row=None, liststore=None):
        self.gui = Gtk.Builder()
        self.gui.add_from_file(SHARED_DATA_FILE(self.GLADE))

        self.parent = parent
        self.liststore_row = liststore_row # each liststore's row
        self.liststore = liststore # main liststore

        self.button_ok = self.gui.get_object('button_ok')
        self.button_ok.set_sensitive(False)

        self.dialog = self.gui.get_object(self.DIALOG)
        if self.parent:
            self.dialog.set_transient_for(self.parent)

        self._setup_ui()

        self.gui.connect_signals(self)

    def _setup_ui(self):
        pass

    def on_entry_changed(self, entry, *args):
        has_entry = entry.get_text_length() > 0
        self.button_ok.set_sensitive(has_entry)

class TreeviewBase(object):

    WIDGET = ''

    def __init__(self, gui, liststore):
        self.gui = gui
        self.liststore = liststore

        self.treeview = treeview = gui.get_object(self.WIDGET)
        treeview.set_model(self.liststore)

    def set_cursor_to(self, treeiter):
        model = self.treeview.get_model()
        row = model.get_path(treeiter)
        self.treeview.set_cursor(row, None, False)

class ActionBase(object):

    DIALOG = None
    TREEVIEW = None

    BUTTON_NEW = ''
    BUTTON_PREFS = ''
    BUTTON_DEL = ''

    def __init__(self, gui, mainwindow, liststore, preferences):
        self.liststore = liststore
        self.preferences = preferences
        self.feedsource_treeview = self.TREEVIEW(gui, mainwindow)

        self.button_prefs = gui.get_object(self.BUTTON_PREFS)
        self.button_del = gui.get_object(self.BUTTON_DEL)

    def on_button_new_clicked(self, button):
        dialog = self.DIALOG(self.preferences, liststore=self.liststore)
        response_id, v = dialog.run()

        if response_id == Gtk.ResponseType.OK:
            new_iter = self.liststore.append(v)
            self.feedsource_treeview.set_cursor_to(new_iter)

    def on_button_prefs_clicked(self, treeselection):
        model, treeiter = treeselection.get_selected()

        dialog = self.DIALOG(self.preferences, model[treeiter], liststore=self.liststore)
        response_id, v = dialog.run()

        if response_id == Gtk.ResponseType.OK:
            new_iter = self.liststore.update(v, treeiter)
            self.feedsource_treeview.set_cursor_to(new_iter)

    def on_button_del_clicked(self, treeselection):
        model, treeiter = treeselection.get_selected()
        model.remove(treeiter)
        model, treeiter = treeselection.get_selected()

        if not treeiter:
            self.button_prefs.set_sensitive(False)
            self.button_del.set_sensitive(False)

    def on_treeview_query_tooltip(self, treeview, *args):
        pass

    def on_treeview_cursor_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()
        if treeiter:
            self.button_prefs.set_sensitive(True)
            self.button_del.set_sensitive(True)
