"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson

    This file is part of Fast_Serial.

    Fast_Serial is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    Fast_Serial is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Fast_Serial.  If not, see <https://www.gnu.org/licenses/>
"""
import re

from PyQt5.QtWidgets import QListWidgetItem, QAbstractItemView
from lib.set import add_user_setting, filters

from lib.dialogs import FilterDialog
try:
    import scripts  # @UnresolvedImport
except ModuleNotFoundError:
    scripts = None

from lib.project import logset
debug, info, warn, err = logset('app')

class FilterUi():
    """ Part of the MainWindow """

    def init_filter_elements(self):

        self.ui.filterList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        for element in filters:
            if len(element) == 2:  # old config files may have only 2 elements
                name, the_filter = element
                selected = False
            else:
                name, the_filter, selected = element
            item = QListWidgetItem(name)
            item.filter = the_filter
            self.ui.filterList.addItem(item)
            item.setSelected(selected)

        self.ui.filterList.itemClicked.connect(self.on_filter_clicked_item)
        self.ui.filterList.itemSelectionChanged.connect(self.on_selection)
        self.ui.addFilterButton.clicked.connect(self.on_filter_add)
        self.ui.editFilterButton.clicked.connect(self.on_filter_edit)
        self.ui.removeFilterButton.clicked.connect(self.on_filter_remove)

        self.ui.upFilterButton.clicked.connect(self.on_filter_list_up)
        self.ui.downFilterButton.clicked.connect(self.on_filter_list_down)

        self.ui.editFilterButton.setEnabled(False)
        self.ui.removeFilterButton.setEnabled(False)
        self.ui.upFilterButton.setEnabled(False)
        self.ui.downFilterButton.setEnabled(False)

        # by default, accept all lines and write them to the terminal
        self.active_filter = re.compile(".*")

    def on_filter_list_up(self):
        row = self.ui.filterList.currentRow()
        currentItem = self.ui.filterList.takeItem(row)
        new_row = row - 1
        self.ui.filterList.insertItem(new_row, currentItem)
        self.ui.filterList.setCurrentRow(new_row);
        self.ui.upFilterButton.setEnabled(new_row != 0)
        self.ui.downFilterButton.setEnabled(True)
        self.save_filters()

    def on_filter_list_down(self):
        row = self.ui.filterList.currentRow()
        currentItem = self.ui.filterList.takeItem(row)
        new_row = row + 1
        self.ui.filterList.insertItem(new_row, currentItem)
        self.ui.filterList.setCurrentRow(new_row);
        maxr = self.ui.filterList.count() - 1
        self.ui.downFilterButton.setEnabled(new_row != maxr)
        self.ui.upFilterButton.setEnabled(True)
        self.save_filters()

    def on_filter_clicked_item(self, item):
        _ = item
        self.ui.editFilterButton.setEnabled(True)  # enable once a row is selected
        self.ui.removeFilterButton.setEnabled(True)

        row = self.ui.filterList.currentRow()
        maxr = self.ui.filterList.count() - 1
        self.ui.upFilterButton.setEnabled(row != 0)
        self.ui.downFilterButton.setEnabled(row != maxr)

    def on_selection(self):
        ''' Items selected changed '''
        filters = []
        for item in self.ui.filterList.selectedItems():
            filters.append(item.filter)
        search = "|".join(filters)
        self.active_filter = re.compile(search)
        self.save_filters()

    def on_filter_add(self):
        info(f"clicked Add Button")

        dialog = FilterDialog(self)
        FilterDialog.name = ""
        FilterDialog.filter = ""
        success = dialog.exec()
        if not success:
            return

        if FilterDialog.name == "" or FilterDialog.filter == "":
            return

        item = QListWidgetItem(FilterDialog.name)
        item.filter = FilterDialog.filter
        self.ui.filterList.addItem(item)
        self.save_filters()

    def save_filters(self):
        filters = []
        for i in range(self.ui.filterList.count()):
            item = self.ui.filterList.item(i)
            name = item.text()
            the_filter = item.filter
            selected = item in self.ui.filterList.selectedItems()
            filters.append((name, the_filter, selected))
        add_user_setting('filters', filters)

    def on_filter_edit(self):
        item = self.ui.filterList.currentItem()
        dialog = FilterDialog(self, item.text(), item.filter)
        info(f"edit {FilterDialog.name}")

        success = dialog.exec()
        if not success:
            return

        if FilterDialog.name == "" or FilterDialog.filter == "":
            return

        item.setText(FilterDialog.name)
        item.filter = FilterDialog.filter

        self.save_filters()

    def on_filter_remove(self):
        item = self.ui.filterList.currentItem()

        row = self.ui.filterList.currentRow()
        self.ui.filterList.takeItem(row)

        self.save_filters()
