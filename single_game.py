# Class corresponding to a single game

# Class corresponding to a single game where the favored team is a candidate
# for selection for week in survivor
class SingleGame:

  # dictionary of team name in input game data to abbreviation used in survivor
  # season processing
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

  # indices corresponding to specific data in input game data that is given as
  # list
  kSeasonYearIdx = 1
  kSeasonWeekIdx = 2
  kHomeTeamIdx = 4
  kHomeTeamScore = 5
  kAwayTeamScore = 6
  kAwayTeamIdx = 7
  kFavoredTeamIdx = 8
  kFavoredTeamSpreadIdx = 9
  

  # initialize data for game from list with specific data in known indices
  def __init__(self, game_data):
    # retrieve season year and week and home/away team from game data
    self.season_year = int(game_data[SingleGame.kSeasonYearIdx])
    self.season_week = int(game_data[SingleGame.kSeasonWeekIdx])
    self.home_team = SingleGame.kTeamNameToAbbrev[game_data[SingleGame.kHomeTeamIdx]]
    self.away_team = SingleGame.kTeamNameToAbbrev[game_data[SingleGame.kAwayTeamIdx]]
    
    # set favored team to home team if no favored team
    # favored team in game data given using abbreviation so no need to convert
    if (game_data[8] != "PICK"):
      self.favored_team = game_data[SingleGame.kFavoredTeamIdx]
    else:
      self.favored_team = self.home_team
    
    # retrieve and set underdog team
    if self.away_team != self.favored_team:
      self.underdog = self.away_team
    else:
      self.underdog = self.home_team
    
    # set percent chance that favorite will win from spread
    self.fav_team_win_percent = self.__SpreadToWinPercent(float(game_data[SingleGame.kFavoredTeamSpreadIdx]))

    # determine and add winning team
    if int(game_data[SingleGame.kHomeTeamScore]) > int(game_data[SingleGame.kAwayTeamScore]):
      self.winning_team = self.home_team
    elif int(game_data[SingleGame.kHomeTeamScore]) == int(game_data[SingleGame.kAwayTeamScore]):
      self.winning_team = "TIE"
    else:
      self.winning_team = self.away_team
    
    # initialize favored team consensus pick percent and team ranking
    # to default values
    self.fav_team_consensus_pick_percent = 0.0
    self.fav_team_ranking = 5.0


  # compute approximate win percent from spread
  def __SpreadToWinPercent(self, spread) -> float:
    return round((float(98 - 50) / 15.5) * min(15.5, abs(spread)) + 50.0)


  # add consensus pick percentage for favored team
  def AddFavTeamConsensusPickPercent(self, consensus_pick_by_team) -> None:
    self.fav_team_consensus_pick_percent = consensus_pick_by_team[self.favored_team]


  # add team ranking for favored team
  def AddFavTeamTeamRanking(self, team_rankings_by_team) -> None:
    self.fav_team_ranking = team_rankings_by_team[self.favored_team]
