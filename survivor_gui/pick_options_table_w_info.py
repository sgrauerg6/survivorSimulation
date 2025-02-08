# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtGui import QColor
from PySide6 import QtCore, QtWidgets
from typing import List
from single_game import SingleGame

# class corresponding to vertical box layout that contains table with survivor pick options for week and info
# above it
class PickOptionsTableWInfo(QtWidgets.QVBoxLayout):

  def __init__(self, parent : QWidget):
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


  def ClearPicksInfo(self) -> None:
    self.picks_info.clear()
    pick_info_header = ["Favored Team", "% Win", "Consensus %", "Team Rating", "Picks Count", "Result"]
    self.picks_info.setHorizontalHeaderLabels(pick_info_header)
    self.week_info_title.setText("")


  def UpdatePicksInfo(self, pick_options_week : List[List[SingleGame]], week_idx : int, week_picks : List[str]) -> None:
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
