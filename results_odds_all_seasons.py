# class to load data across all seasons from csv file

import csv

class ResultsOddsAllSeasons:

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

  # dictionary of team abbreviation used in consenus picks to abbreviation used in processing
  # only given if different from team abbreviation used in processing
  kConsPicksAbbrevToProcAbbrev = {
    "STL" : "LAR",
    "OAK" : "LVR",
    "LV" : "LVR",
    "SD" : "LAC",
    "WSH" : "WAS"
  }

  def __init__(self, all_results_csv):
    with open(all_results_csv, newline='') as f:
      reader = csv.reader(f)
      data = list(reader)
    #print(data)
    # go through data and add winning team
    for row in data[1:]:
      if int(row[5]) > int(row[6]):
        row.append(ResultsOddsAllSeasons.kTeamNameToAbbrev[row[4]])
      elif int(row[5]) == int(row[6]):
        row.append("TIE")
      else:
        row.append(ResultsOddsAllSeasons.kTeamNameToAbbrev[row[7]])
    # generate list with season, week, predicted winner, odds, and winner
    self.survivor_data = []
    for row in data[1:]:
      try:
        survivor_data_row = []
        survivor_data_row.append(int(row[1]))
        survivor_data_row.append(int(row[2]))
        survivor_data_row.append(row[8])
        survivor_data_row.append(self.SpreadToWinPercent(float(row[9])))
        survivor_data_row.append(row[-1])
        self.survivor_data.append(survivor_data_row)
      except ValueError:
        pass
    #print(self.survivor_data)
    week_options = self.SurvivorWeekOptions(2024, 18)
    #print(week_options)

  # compute approximate win percent from spread
  def SpreadToWinPercent(self, spread):
    return round((float(98 - 50) / 15.5) * min(15.5, abs(spread)) + 50.0)

  # get survivor week options
  def SurvivorWeekOptions(self, year, week):
    week_options = []
    # get consensus picks for week
    consensus_picks_file = "consensus_picks_" + str(year) + "_" + str(week) + ".csv"
    with open(consensus_picks_file, newline='') as f:
      reader = csv.reader(f)
      consensus_picks_data = list(reader)
    consensus_pick_team = {}
    column_num_average = 0
    headers_row = consensus_picks_data[0]
    for i in range(0, len(headers_row)): 
      if headers_row[i] == "Average":
        column_num_average = i
        break
    for row in consensus_picks_data[1:]:
      #print(row)
      team = row[0]
      # adjust team abbreviation if needed to match team abbreviation used
      # in processing
      if team in ResultsOddsAllSeasons.kConsPicksAbbrevToProcAbbrev:
        team = ResultsOddsAllSeasons.kConsPicksAbbrevToProcAbbrev[row[0]]
      consensus_pick_team[team] = row[column_num_average]
    for survivor_data_game in self.survivor_data:
      if survivor_data_game[0] == year and survivor_data_game[1] == week:
        favored_team = survivor_data_game[2]
        game_data = survivor_data_game[2:5]
        game_data.append(float(consensus_pick_team[favored_team]))
        week_options.append(game_data)
    return week_options
  
  def PercentWinIdxSurvivorWeek(self):
    return 1
  
  def ConsensusPickPercentIdxSurvivorWeek(self):
    return 3