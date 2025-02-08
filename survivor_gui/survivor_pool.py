# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6 import QtCore, QtWidgets
from survivor_season import SurvivorSeason
from survivor_strategy import SurvivorStrategy
from pick_options_table_w_info import PickOptionsTableWInfo
from picks_table_w_info import PicksTableWInfo

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
