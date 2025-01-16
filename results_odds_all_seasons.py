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

  # get survivor week options in order from most biggest favorite to smallest
  # favority
  def SurvivorWeekOptions(self, year, week):
    week_options = []
    for survivor_data_game in self.survivor_data:
      if survivor_data_game[0] == year and survivor_data_game[1] == week:
        week_options.append(survivor_data_game[2:5])
    week_options.sort(key=lambda x: x[1], reverse = True) 
    return week_options