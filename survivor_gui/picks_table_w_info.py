from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView
from PySide6 import QtCore, QtWidgets
from survivor_season import SurvivorSeason
from survivor_strategy import SurvivorStrategy

# class corresponding to vertical box layout that contains survivor pick results table and info
# above it
class PicksTableWInfo(QtWidgets.QVBoxLayout):

  # initialize layout with survivor entries table and corresponding info
  def __init__(self, parent : QWidget, num_entries : int, nfl_season : int, num_weeks : int):
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
  def AddSurvivorEntriesToTable(self, survivor_season : SurvivorSeason) -> None:
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
