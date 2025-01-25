# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QColor
import random
from PySide6 import QtCore, QtWidgets
from survivor_season import SurvivorSeason
from survivor_strategy import SurvivorStrategy

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().resize(1850, 700)
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.num_entries = 150
        self.nfl_season = 2024
        self.num_weeks = 18

        self.layout = QtWidgets.QVBoxLayout(self)
        self.tableWidget = QtWidgets.QTableWidget(self.num_entries, self.num_weeks, self);
        self.layout.addWidget(self.tableWidget);

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)
        self.survivor_strategy = SurvivorStrategy()
        self.survivor_season_no_weighing = SurvivorSeason(self.nfl_season, self.num_entries)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        print("Week: " + str(self.survivor_season_no_weighing.week_num))
        if self.survivor_season_no_weighing.week_num < self.num_weeks:
          self.surviving_entries_no_weighing = self.survivor_season_no_weighing.ProcessWeek(self.survivor_strategy)
          print("Week num: " + str(self.survivor_season_no_weighing.week_num))
          print("Num entries: " + str(self.surviving_entries_no_weighing))
          self.AddSurvivorEntriesToTable()
        else:
          self.tableWidget.clear()
          self.survivor_season_no_weighing = SurvivorSeason(self.nfl_season, self.num_entries)



    def AddSurvivorEntriesToTable(self):
        entries = self.survivor_season_no_weighing.entries
        # sort entries for display by
        # (1) number of entries (reverse),
        # (2) whether the last picks is a strike or not, and
        # (3) by team
        entries.sort(key=lambda entry:entry.picks_results[-1][0])
        entries.sort(key=lambda entry:entry.IsLastPickStrike())
        entries.sort(key=lambda entry:len(entry.AllPicks()), reverse=True)
        for i in range(len(entries)):
            entry = self.survivor_season_no_weighing.entries[i]
            entry_picks = entry.AllPicks()
            for j in range(len(entry_picks)):
              self.tableWidget.setItem(i, j, QTableWidgetItem(str(entry_picks[j])))
              if entry.IsPickStrike(j):
                self.tableWidget.item(i, j).setBackground(QColor("red"))
              else:
                self.tableWidget.item(i, j).setBackground(QColor("green"))


if __name__ == "__main__":
    app = QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
