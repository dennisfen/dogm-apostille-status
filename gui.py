#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from time import sleep

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QVBoxLayout)

from apostille_request import ApostilleChecker, read_entries


class RequestThread(QThread):
    def __init__(self, apostille_checker):
        QThread.__init__(self)
        self.checker = apostille_checker

    def __del__(self):
        self.wait()

    def run(self):
        self.checker.request_status()
        sleep(5)
        print(self.checker)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.table_model = QStandardItemModel()
        self.table_view = QTableView()
        self.v_box = QVBoxLayout()
        self.apostilles = []

        # temp
        self.apostille_threads = []

        self.init_ui()

    def init_ui(self):

        entries = read_entries('entries.json')
        for entry in entries['entry']:
            item = ApostilleChecker(entry)
            self.apostilles.append(item)
            self.table_model.appendRow([QStandardItem(item.id),
                                        QStandardItem(item.name),
                                        QStandardItem(item.status_string)])

        for idx, apostille in enumerate(self.apostilles):
            self.apostille_threads.append(RequestThread(apostille))
            self.apostille_threads[idx].start()

        self.table_model.setHorizontalHeaderLabels(["Номер", "Имя", "Статус"])
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.resizeColumnsToContents()
        self.v_box.addWidget(self.table_view)

        self.setLayout(self.v_box)
        self.setWindowTitle('Статус подготовки апостилей')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
