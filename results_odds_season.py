# class to load data across season from csv file

import csv
from team_rankings import TeamRankings
from consensus_picks import ConsensusPicks
from typing import List

# class to load and store win/loss for each game, odds, and other data across season
class ResultsOddsSeason:

  # dictionary of team name to abbreviation
  kTeamNameToAbbrev = {
    "St. Louis Cardinals" : "ARI",
    "Phoenix Cardinals" : "ARI",
    "Arizona Cardinals" : "ARI",
    "Atlanta Falcons" : "ATL",
    "Baltimore Ravens" : "BAL",
    "Buffalo Bills" : "BUF",
    "Carolina Panthers" : "CAR",
    "Chicago Bears" : "CHI",
    "Cincinnati Bengals" : "CIN",
    "Cleveland Browns" : "CLE",
    "Dallas Cowboys" : "DAL",
    "Denver Broncos" : "DEN",
    "Detroit Lions" : "DET",
    "Green Bay Packers" : "GB",
    "Houston Texans" : "HOU",
    "Baltimore Colts" : "IND",
    "Indianapolis Colts" : "IND",
    "Jacksonville Jaguars" : "JAX",
    "Kansas City Chiefs" : "KC",
    "Oakland Raiders" : "LVR",
    "Los Angeles Raiders" : "LVR",
    "Las Vegas Raiders" : "LVR",
    "San Diego Chargers" : "LAC",
    "Los Angeles Chargers" : "LAC",
    "St. Louis Rams" : "LAR",
    "Los Angeles Rams" : "LAR",
    "Miami Dolphins" : "MIA",
    "Minnesota Vikings" : "MIN",
    "Boston Patriots" : "NE",
    "New England Patriots" : "NE",
    "New Orleans Saints" : "NO",
    "New York Giants" : "NYG",
    "New York Jets" : "NYJ",
    "Philadelphia Eagles" : "PHI",
    "Pittsburgh Steelers" : "PIT",
    "San Francisco 49ers" : "SF",
    "Seattle Seahawks" : "SEA",
    "Tampa Bay Buccaneers" : "TB",
    "Houston Oilers" : "TEN",
    "Tennessee Oilers" : "TEN",
    "Tennessee Titans" : "TEN",
    "Washington Redskins" : "WAS",
    "Washington Football Team" : "WAS",
    "Washington Commanders" : "WAS",
  }


  # initialize survivor data for season using csv file with all data
  def __init__(self, season_year, all_results_csv):
    # read csv file with data from all seasons
    self.all_results_data = []
    with open(all_results_csv, newline='') as f:
      reader = csv.reader(f)
      self.all_results_data = list(reader)

    # go through data and add winning team
    for row in self.all_results_data[1:]:
      if int(row[5]) > int(row[6]):
        row.append(ResultsOddsSeason.kTeamNameToAbbrev[row[4]])
      elif int(row[5]) == int(row[6]):
        row.append("TIE")
      else:
        row.append(ResultsOddsSeason.kTeamNameToAbbrev[row[7]])

    # generate list with season, week, predicted winner, odds, and winner
    self.survivor_data = []
    for row in self.all_results_data[1:]:
      try:
        # only add entries that correspond to input season year
        if (int(row[1]) == season_year):
          survivor_data_row = []
          survivor_data_row.append(int(row[1]))
          survivor_data_row.append(int(row[2]))
          survivor_data_row.append(row[8])
          survivor_data_row.append(self.__SpreadToWinPercent(float(row[9])))
          survivor_data_row.append(row[-1])
          self.survivor_data.append(survivor_data_row)
      except ValueError:
        pass


  # compute approximate win percent from spread
  def __SpreadToWinPercent(self, spread) -> float:
    return round((float(98 - 50) / 15.5) * min(15.5, abs(spread)) + 50.0)


  # get starting year, month, and day for week of season
  def StartingDateWeekOfSeason(self, year, week) -> List[int]:
    # get starting date for season
    index_year = 1
    index_week = 2
    for game_data in self.all_results_data:
      if (game_data[index_year] == str(year)) and ((game_data[index_week]) == str(week)):
        starting_date = game_data[0]
        break
    month_start_week = str(starting_date.split('/')[0]).zfill(2)
    day_start_week = str(starting_date.split('/')[1]).zfill(2)
    year_start_week = str(starting_date.split('/')[2]).zfill(2)

    return year_start_week, month_start_week, day_start_week 


  # get survivor week options
  def SurvivorWeekOptions(self, year, week) -> List[str]:
    # get team rankings for week
    teams_w_rankings = TeamRankings.RetrieveTeamRankings(year, week)
    # get consensus picks for week
    consensus_pick_team = ConsensusPicks.ConsensusPicksForWeek(year, week)
    week_options = []
    for survivor_data_game in self.survivor_data:
      if survivor_data_game[0] == year and survivor_data_game[1] == week:
        favored_team = survivor_data_game[2]
        if (favored_team != "PICK"):
          game_data = survivor_data_game[2:5]
          game_data.append(consensus_pick_team[favored_team])
          game_data.append(teams_w_rankings[favored_team])
          week_options.append(game_data)
    return week_options
  

  # get column index of percent chance to win
  def PercentWinIdxSurvivorWeek(self):
    return 1
  

  # get column index of average consensus pick
  def ConsensusPickPercentIdxSurvivorWeek(self):
    return 3
  

  # get column index of team ranking
  def TeamRankingIdxSurvivorWeek(self):
    return 3