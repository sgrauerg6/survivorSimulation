# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView
from PySide6.QtGui import QColor
import random
from PySide6 import QtCore, QtWidgets
from survivor_season import SurvivorSeason
from survivor_strategy import SurvivorStrategy

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().resize(1500, 700)
        super().setStyleSheet("background-color:rgba(0,155,255,100%);")
        self.num_entries = 150
        self.nfl_season = 2024
        self.num_weeks = 18

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.picks_info_layout = QtWidgets.QHBoxLayout()
        self.picks_info_layout.setSpacing(100)
        self.picks_layout = QtWidgets.QVBoxLayout()
        self.picks_layout.setSpacing(0)
        self.season_entries_header = QtWidgets.QLabel("NFL Season: 2024  Entries At Start: 150   Remaining Entries: 150")
        self.season_entries_header.setStyleSheet("color:rgba(0, 0, 0, 100%)")
        font = self.season_entries_header.font();
        font.setPointSize(20);
        font.setBold(False);
        self.season_entries_header.setFont(font);
        self.picks_title = QtWidgets.QLabel("Survivor Entries")
        self.picks_title.setStyleSheet("color:rgba(0, 0, 0, 100%)")
        font = self.picks_title.font();
        font.setPointSize(12);
        font.setBold(True);
        self.picks_title.setFont(font);
        self.picks_layout.addWidget(self.season_entries_header)
        self.picks_layout.addWidget(self.picks_title)
        self.picks_table = QtWidgets.QTableWidget(self.num_entries, self.num_weeks, self)
        self.picks_table.setStyleSheet("background:rgba(102, 64, 25, 100%)")
        self.picks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.picks_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.picks_table.setSelectionMode(QAbstractItemView.NoSelection)
        weeks_header = []
        for i in range(1, self.num_weeks + 1):
          weeks_header.append("Week " + str(i))
        self.picks_table.setHorizontalHeaderLabels(weeks_header)
        self.picks_table.setFixedWidth(750)
        self.week_info_layout = QtWidgets.QVBoxLayout()
        self.week_info_layout.setSpacing(0)
        self.week_info_title = QtWidgets.QLabel("")
        font = self.week_info_title.font();
        font.setPointSize(24);
        font.setBold(True);
        self.week_info_title.setFont(font);
        self.week_info_title.setStyleSheet("color:rgba(0, 0, 127, 100%)")
        #self.week_info_title.setFixedHeight(38)
        self.week_info_title.setContentsMargins(0, 0, 0, 5)
        self.picks_info = QtWidgets.QTableWidget(16, 5, self)
        self.picks_info.setStyleSheet("background:rgba(0,0,0,100%)")
        self.picks_info.setEditTriggers(QTableWidget.NoEditTriggers)
        self.picks_info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.picks_info.setSelectionMode(QAbstractItemView.NoSelection)
        pick_info_header = ["Favored Team", "% Win", "Consensus %", "Team Rating", "Picks Count"]
        self.picks_info.setHorizontalHeaderLabels(pick_info_header)
        self.picks_info.verticalHeader().setVisible(False)
        self.picks_info.setFixedWidth(502)
        self.picks_info.setFixedHeight(515)
        self.picks_layout.addWidget(self.picks_table)
        self.week_info_layout.addWidget(self.week_info_title, 0)
        self.week_info_layout.addWidget(self.picks_info, 1)

        self.picks_info_layout.addLayout(self.picks_layout, 1)
        self.picks_info_layout.addSpacing(50)
        self.picks_info_layout.addLayout(self.week_info_layout, 1)
        self.picks_info_layout.addStretch(0.25)

        self.button = QtWidgets.QPushButton("Simulate Week 1")
        font = self.button.font();
        font.setPointSize(20);
        font.setBold(True);
        self.button.setFont(font)
        self.button.setFixedHeight(35)
        self.button.setStyleSheet("background:rgba(255,255,0,100%); color:rgba(0, 0, 0, 100%)")
        self.headline_label = QtWidgets.QLabel("NFL Survivor Pool Simulation", alignment=QtCore.Qt.AlignCenter)
        font = self.headline_label.font();
        font.setPointSize(50);
        font.setBold(True);
        self.headline_label.setFont(font);
        self.headline_label.setStyleSheet("color:rgba(0, 0, 0, 100%)")

        self.main_layout.addWidget(self.headline_label)
        self.main_layout.addLayout(self.picks_info_layout)
        self.main_layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)
        self.survivor_strategy = SurvivorStrategy()
        self.survivor_season_no_weighing = SurvivorSeason(self.nfl_season, self.num_entries)

    @QtCore.Slot()
    def magic(self):
        print("Week: " + str(self.survivor_season_no_weighing.week_num))
        self.week_info_title.setText("Week " + str(self.survivor_season_no_weighing.week_num + 1) + " Games")
        if self.survivor_season_no_weighing.week_num < self.num_weeks:
          self.surviving_entries_no_weighing = self.survivor_season_no_weighing.ProcessWeek(self.survivor_strategy)
          self.season_entries_header.setText("NFL Season: 2024   Entries At Start: 150   Remaining Entries: " + str(self.surviving_entries_no_weighing))
          print("Week num: " + str(self.survivor_season_no_weighing.week_num))
          print("Num entries: " + str(self.surviving_entries_no_weighing))
          self.AddSurvivorEntriesToTable()
          self.AddPickOptionsInfoToTable()
          self.picks_table.setItem(0, self.survivor_season_no_weighing.week_num - 1, QTableWidgetItem())
          self.picks_table.scrollToItem(self.picks_table.item(0, self.survivor_season_no_weighing.week_num - 1))
          if (self.survivor_season_no_weighing.week_num + 1) <= self.num_weeks:
            self.button.setText("Simulate Week " + str(self.survivor_season_no_weighing.week_num + 1))
          else:
            self.button.setText("Reset To Start")
        else:
          self.picks_table.clear()
          self.picks_info.clear()
          self.season_entries_header.setText("NFL Season: 2024   Entries At Start: 150   Remaining Entries: 150")
          pick_info_header = ["Favored Team", "% Win", "Consensus %", "Team Rating", "Picks Count"]
          self.picks_info.setHorizontalHeaderLabels(pick_info_header)
          self.week_info_title.setText("")
          weeks_header = []
          for i in range(1, self.num_weeks + 1):
            weeks_header.append("Week " + str(i))
          self.picks_table.setHorizontalHeaderLabels(weeks_header)
          self.picks_table.setFixedWidth(750)
          self.survivor_season_no_weighing = SurvivorSeason(self.nfl_season, self.num_entries)
          self.button.setText("Simulate Week " + str(self.survivor_season_no_weighing.week_num + 1))


    def AddPickOptionsInfoToTable(self):
        pick_options = self.survivor_season_no_weighing.week_options
        entries = self.survivor_season_no_weighing.entries
        week_picks = []
        for entry in entries:
            if len(entry.AllPicks()) == self.survivor_season_no_weighing.week_num:
                week_picks.append(entry.picks_results[-1][0])
        for pick_idx in range(0, min(16, len(pick_options))):
          favored_team_lbl = QtWidgets.QLabel()
          favored_team_lbl.setMargin(5)
          favored_team_lbl.setText(\
            "<span style='font-size:16px;'><b>" + pick_options[pick_idx].favored_team + \
            "</b></span><span style='font-size:10px;'>" + " vs " + pick_options[pick_idx].underdog + "</span>")
          self.picks_info.setCellWidget(pick_idx, 0, favored_team_lbl)
          self.picks_info.setItem(pick_idx, 1, QTableWidgetItem(str(pick_options[pick_idx].fav_team_win_percent)))
          self.picks_info.setItem(pick_idx, 2, QTableWidgetItem(str(pick_options[pick_idx].fav_team_consensus_pick_percent)))
          self.picks_info.setItem(pick_idx, 3, QTableWidgetItem(str(round(pick_options[pick_idx].fav_team_ranking, 2))))
          self.picks_info.setItem(pick_idx, 4, QTableWidgetItem(str(week_picks.count(pick_options[pick_idx].favored_team))))
          if pick_options[pick_idx].winning_team == pick_options[pick_idx].favored_team or pick_options[pick_idx].winning_team == "TIE":
            favored_team_lbl.setStyleSheet("QLabel { background-color : green; }");
            for col in range(1, 5):
              self.picks_info.item(pick_idx, col).setBackground(QColor("green"))
          else:
            favored_team_lbl.setStyleSheet("QLabel { background-color : red; }");
            for col in range(1, 5):
              self.picks_info.item(pick_idx, col).setBackground(QColor("red"))


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
              #self.picks_table.setItem(i, j, QTableWidgetItem(str(entry_picks[j])))
              if entry.IsPickStrike(j):
                pick_label = QtWidgets.QLabel(entry_picks[j])
                pick_label.setStyleSheet("QLabel { background-color : red; }");
                self.picks_table.setCellWidget(i, j, pick_label)
                #self.picks_table.item(i, j).setBackground(QColor("red"))
              else:
                pick_label = QtWidgets.QLabel(entry_picks[j])
                pick_label.setStyleSheet("QLabel { background-color : green; }");
                self.picks_table.setCellWidget(i, j, pick_label)
                #self.picks_table.item(i, j).setBackground(QColor("green"))


if __name__ == "__main__":
    app = QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
