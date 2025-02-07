# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtGui import QColor
from PySide6 import QtCore, QtWidgets
from survivor_season import SurvivorSeason
from survivor_strategy import SurvivorStrategy

# class corresponding to vertical box layout that contains survivor pick results table and info
# above it
class PicksTableWInfo(QtWidgets.QVBoxLayout):

  # initialize layout with survivor entries table and corresponding info
  def __init__(self, parent, num_entries : int, nfl_season : int, num_weeks : int):
    super().__init__()
    self.setSpacing(0)
    self.__num_entries = num_entries
    self.__nfl_season = nfl_season
    self.__num_weeks = num_weeks

    # set up header with info for survivor entries for seaons
    self.__season_entries_header = QtWidgets.QLabel()
    self.UpdateSeasonEntriesHeader(self.__num_entries)
    self.__season_entries_header.setStyleSheet("color:rgba(0, 0, 0, 100%)")
    font = self.__season_entries_header.font()
    font.setPointSize(20)
    font.setBold(False)
    self.__season_entries_header.setFont(font)
    self.addWidget(self.__season_entries_header)

    # set title for survivor entries table
    picks_title = QtWidgets.QLabel("Survivor Entries")
    picks_title.setStyleSheet("color:rgba(0, 0, 0, 100%)")
    font = picks_title.font()
    font.setPointSize(12)
    font.setBold(True)
    picks_title.setFont(font)
    self.addWidget(picks_title)

    # set up survivor entries table
    self.__picks_table = QtWidgets.QTableWidget(self.__num_entries, self.__num_weeks, parent)
    self.__picks_table.setStyleSheet("background:rgba(102, 64, 25, 100%)")
    self.__picks_table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.__picks_table.setFocusPolicy(QtCore.Qt.NoFocus)
    self.__picks_table.setSelectionMode(QAbstractItemView.NoSelection)
    weeks_header = []
    for i in range(1, num_weeks + 1):
      weeks_header.append("Week " + str(i))
    self.__picks_table.setHorizontalHeaderLabels(weeks_header)
    self.__picks_table.setFixedWidth(750)
    self.addWidget(self.__picks_table)


  # update season survivor entries header, specifically the number of entries remaining
  def UpdateSeasonEntriesHeader(self, entries_remaining : int) -> None:
    self.__season_entries_header.setText(\
      "NFL Season: " + str(self.__nfl_season) + "   Entries At Start: " + str(self.__num_entries) + \
      "   Remaining Entries: " + str(entries_remaining))


  # clear all survivor entries from table
  def ClearPicks(self) -> None:
    self.__picks_table.clear()
    weeks_header = []
    for i in range(1, self.__num_weeks + 1):
      weeks_header.append("Week " + str(i))
    self.__picks_table.setHorizontalHeaderLabels(weeks_header)
    self.__picks_table.setFixedWidth(750)


  # populate table with current state of survivor entries
  def AddSurvivorEntriesToTable(self, survivor_season : int) -> None:
    # retrieve all entries
    entries = survivor_season.entries
    # sort entries for display by
    # (1) number of entries (reverse)
    # (2) whether the last picks is a strike or not
    # (3) by team
    entries.sort(key=lambda entry:entry.picks_results[-1][0])
    entries.sort(key=lambda entry:entry.IsLastPickStrike())
    entries.sort(key=lambda entry:len(entry.AllPicks()), reverse=True)
    # go through each entry and add to row in table
    for i in range(len(entries)):
      entry = survivor_season.entries[i]
      entry_picks = entry.AllPicks()
      for j in range(len(entry_picks)):
        pick_label = QtWidgets.QLabel(entry_picks[j])
        if entry.IsPickStrike(j):
          # set background to red if strike in week (pick lost)
          pick_label.setStyleSheet("QLabel { background-color : red; }");
        else:
          # set background to green if no strike in week (pick won or tied if tie isn't a strike)
          pick_label.setStyleSheet("QLabel { background-color : green; }");
        self.__picks_table.setCellWidget(i, j, pick_label)


  # scroll table to specified week
  def ScrollTableToWeek(self, week_num : int) -> None:
    self.__picks_table.setItem(0, week_num - 1, QTableWidgetItem())
    self.__picks_table.scrollToItem(self.__picks_table.item(0, week_num - 1))


# class corresponding to vertical box layout that contains table with survivor pick options for week and info
# above it
class PickOptionsTableWInfo(QtWidgets.QVBoxLayout):

  def __init__(self, parent):
    super().__init__()
    self.setSpacing(0)
    self.week_info_title = QtWidgets.QLabel("")
    font = self.week_info_title.font();
    font.setPointSize(24);
    font.setBold(True);
    self.week_info_title.setFont(font);
    self.week_info_title.setStyleSheet("color:rgba(0, 0, 127, 100%)")
    self.week_info_title.setContentsMargins(0, 0, 0, 5)
    self.picks_info = QtWidgets.QTableWidget(16, 6, parent)
    self.picks_info.setStyleSheet("background:rgba(0,0,0,100%)")
    self.picks_info.setEditTriggers(QTableWidget.NoEditTriggers)
    self.picks_info.setFocusPolicy(QtCore.Qt.NoFocus)
    self.picks_info.setSelectionMode(QAbstractItemView.NoSelection)
    pick_info_header = ["Favored Team", "% Win", "Consensus %", "Team Rating", "Picks Count", "Result"]
    header = self.picks_info.horizontalHeader()
    for column in range(header.count()):
      header.setSectionResizeMode(column, QHeaderView.Stretch)
    self.picks_info.setHorizontalHeaderLabels(pick_info_header)
    self.picks_info.verticalHeader().setVisible(False)
    self.picks_info.setFixedWidth(502)
    self.picks_info.setFixedHeight(515)
    self.addWidget(self.week_info_title, 0)
    self.addWidget(self.picks_info, 1)


  def ClearPicksInfo(self):
    self.picks_info.clear()
    pick_info_header = ["Favored Team", "% Win", "Consensus %", "Team Rating", "Picks Count", "Result"]
    self.picks_info.setHorizontalHeaderLabels(pick_info_header)
    self.week_info_title.setText("")


  def UpdatePicksInfo(self, pick_options_week, week_idx : int, week_picks) -> None:
    for pick_idx in range(0, min(16, len(pick_options_week[week_idx]))):
      favored_team_lbl = QtWidgets.QLabel()
      favored_team_lbl.setMargin(5)
      result_lbl = QtWidgets.QLabel()
      result_lbl.setMargin(5)
      self.picks_info.setCellWidget(pick_idx, 0, favored_team_lbl)
      self.picks_info.setCellWidget(pick_idx, 5, result_lbl)
      self.picks_info.setItem(pick_idx, 1, QTableWidgetItem(str(pick_options_week[week_idx][pick_idx].fav_team_win_percent)))
      self.picks_info.setItem(pick_idx, 2, QTableWidgetItem(str(pick_options_week[week_idx][pick_idx].fav_team_consensus_pick_percent)))
      self.picks_info.setItem(pick_idx, 3, QTableWidgetItem(str(round(pick_options_week[week_idx][pick_idx].fav_team_ranking, 2))))
      self.picks_info.setItem(pick_idx, 4, QTableWidgetItem(str(week_picks.count(pick_options_week[week_idx][pick_idx].favored_team))))
      if pick_options_week[week_idx][pick_idx].winning_team == pick_options_week[week_idx][pick_idx].favored_team or pick_options_week[week_idx][pick_idx].winning_team == "TIE":
        favored_team_lbl.setText(\
            "<span style='font-size:18px;'><b>" + pick_options_week[week_idx][pick_idx].favored_team + \
            "</b></span><span style='font-size:10px;'>" + " vs " + pick_options_week[week_idx][pick_idx].underdog + "</span>")
        favored_team_lbl.setStyleSheet("QLabel { background-color : green; }");
        result_lbl.setText("<span style='font-size:18px;'><b>" + " W " + "</span>" + "</b></span><span style='font-size:10px;'>" + \
            str(pick_options_week[week_idx][pick_idx].winning_score) + "-" + str(pick_options_week[week_idx][pick_idx].losing_score) + "<\span>")
        result_lbl.setStyleSheet("QLabel { background-color : green; }");
        for col in range(1, 5):
          self.picks_info.item(pick_idx, col).setBackground(QColor("green"))
      else:
        favored_team_lbl.setText(\
            "<span style='font-size:18px;'><b>" + pick_options_week[week_idx][pick_idx].favored_team + \
            "</b></span><span style='font-size:10px;'>" + " vs " + pick_options_week[week_idx][pick_idx].underdog + "</span>")
        favored_team_lbl.setStyleSheet("QLabel { background-color : red; }");
        result_lbl.setText("<span style='font-size:18px;'><b>" + " L " + "</span>" + "</b></span><span style='font-size:10px;'>" + \
            str(pick_options_week[week_idx][pick_idx].losing_score) + "-" + str(pick_options_week[week_idx][pick_idx].winning_score) + "<\span>")
        result_lbl.setStyleSheet("QLabel { background-color : red; }");
        for col in range(1, 5):
          self.picks_info.item(pick_idx, col).setBackground(QColor("red"))
    self.picks_info.resizeColumnsToContents()
    header = self.picks_info.horizontalHeader()
    for column in range(header.count()):
      header.setSectionResizeMode(column, QHeaderView.Stretch)


  def UpdateWeekInfoTitle(self, week_num : int) -> None:
    self.week_info_title.setText("Week " + str(week_num + 1) + " Games")



class SurvivorPool(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    super().resize(1500, 700)
    super().setStyleSheet("background-color:rgba(0,155,255,100%);")
    self.num_entries = 150
    self.nfl_season = 2024
    self.num_weeks = 18

    # set up headline label for top of layout
    self.headline_label = QtWidgets.QLabel("NFL Survivor Pool Simulation", alignment=QtCore.Qt.AlignCenter)
    font = self.headline_label.font();
    font.setPointSize(50);
    font.setBold(True);
    self.headline_label.setFont(font);
    self.headline_label.setStyleSheet("color:rgba(0, 0, 0, 100%)")

    # set up layout with picks table with corresponding info
    self.picks_tbl_w_info = PicksTableWInfo(self, self.num_entries, self.nfl_season, self.num_weeks)

    # set up layout with pick options for week and corresponding info
    self.week_info_layout = PickOptionsTableWInfo(self)

    # set up horizontal layout with picks on the left side and
    # info about week for season week on right side
    self.picks_info_layout = QtWidgets.QHBoxLayout()
    self.picks_info_layout.setSpacing(100)
    self.picks_info_layout.addLayout(self.picks_tbl_w_info, 1)
    self.picks_info_layout.addSpacing(50)
    self.picks_info_layout.addLayout(self.week_info_layout, 1)
    self.picks_info_layout.addStretch(0.25)

    # add button to simulate season week
    self.simulate_week_btn = QtWidgets.QPushButton("Simulate Week 1")
    font = self.simulate_week_btn.font();
    font.setPointSize(20);
    font.setBold(True);
    self.simulate_week_btn.setFont(font)
    self.simulate_week_btn.setFixedHeight(35)
    self.simulate_week_btn.setStyleSheet("background:rgba(255,255,0,100%); color:rgba(0, 0, 0, 100%)")
    self.simulate_week_btn.clicked.connect(self.SimulateWeek)

    # set up main layout
    self.main_layout = QtWidgets.QVBoxLayout(self)
    self.main_layout.addWidget(self.headline_label)
    self.main_layout.addLayout(self.picks_info_layout)
    self.main_layout.addWidget(self.simulate_week_btn)

    # initialize survivor season and strategy for picks
    self.survivor_season = SurvivorSeason(self.nfl_season, self.num_entries)
    self.survivor_strategy = SurvivorStrategy()
    self.pick_options_week = []


  # simulate season week for survivor pool including picks for each active entry
  @QtCore.Slot()
  def SimulateWeek(self) -> None:
    self.week_info_layout.UpdateWeekInfoTitle(self.survivor_season.week_num)
    if self.survivor_season.week_num < self.num_weeks:
      # generate survivor pool picks for week using survivor strategy
      self.surviving_entries = self.survivor_season.ProcessWeek(self.survivor_strategy)

      # update table with survivor picks with survivor pool entries for week
      self.picks_tbl_w_info.UpdateSeasonEntriesHeader(self.surviving_entries)
      self.picks_tbl_w_info.ScrollTableToWeek(self.survivor_season.week_num);
      self.picks_tbl_w_info.AddSurvivorEntriesToTable(self.survivor_season)

      # update table with pick options for week
      self.pick_options_week.append(self.survivor_season.week_options)
      self.AddPickOptionsInfoToTable(self.survivor_season.week_num)

      # Update button for simulating week to increment to following week
      # or to reset to start if in final week
      if (self.survivor_season.week_num + 1) <= self.num_weeks:
        self.simulate_week_btn.setText("Simulate Week " + str(self.survivor_season.week_num + 1))
      else:
        self.simulate_week_btn.setText("Reset To Start")
    else:
      # all weeks of season have been simulated, so reset back to starting week
      self.picks_tbl_w_info.ClearPicks()
      self.week_info_layout.ClearPicksInfo()
      self.picks_tbl_w_info.UpdateSeasonEntriesHeader(self.num_entries)
      self.survivor_season = SurvivorSeason(self.nfl_season, self.num_entries)
      self.simulate_week_btn.setText("Simulate Week " + str(self.survivor_season.week_num + 1))


  def AddPickOptionsInfoToTable(self, week : int) -> None:
    week_picks = []
    week_idx = week - 1

    # get survivor pick for all entries for all weeks
    entries = self.survivor_season.entries

    # get picks for season week
    for entry in entries:
      if len(entry.AllPicks()) == self.survivor_season.week_num:
        week_picks.append(entry.picks_results[week_idx][0])

    # update pick options info for season week
    self.week_info_layout.UpdatePicksInfo(self.pick_options_week, week_idx, week_picks)


if __name__ == "__main__":
  app = QApplication([])
  window = SurvivorPool()
  window.show()
  sys.exit(app.exec())
