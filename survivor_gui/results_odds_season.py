# class to load data across season from csv file

import csv
from team_rankings import TeamRankings
from consensus_picks import ConsensusPicks
from typing import List
from single_game import SingleGame

# class to load and store win/loss for each game, odds, and other data across season
class ResultsOddsSeason:

  # initialize survivor data for season using csv file with all data
  def __init__(self, season_year : int, all_results_csv_file_path : str):
    # read csv file with data from all seasons
    self.all_results_data = []
    with open(all_results_csv_file_path, newline='') as f:
      reader = csv.reader(f)
      self.all_results_data = list(reader)

    # generate list of SingleGame objects with data for each single game
    # in season
    self.survivor_data = []
    for game_data_row in self.all_results_data[1:]:
      try:
        # only add game data for games that correspond to input season year
        if (int(game_data_row[1]) == season_year):
          # generate SingleGame object from game data in row
          # and add to survivor data for season
          self.survivor_data.append(SingleGame(game_data_row))
      except ValueError:
        pass


  # get survivor week options as list of SingleGame objects corresponding
  # to all games for the week of the season
  def SurvivorWeekOptions(self, year : int, week : int) -> List[SingleGame]:
    # get team rankings for week
    teams_w_rankings = TeamRankings.RetrieveTeamRankings(year, week)
    # get consensus picks for week
    consensus_pick_team = ConsensusPicks.ConsensusPicksForWeek(year, week)
    week_options = []
    for survivor_data_game in self.survivor_data:
      if survivor_data_game.season_year == year and survivor_data_game.season_week == week:
        # add consensus pick percent and team ranking for favored team to game data
        survivor_data_game.AddFavTeamConsensusPickPercent(consensus_pick_team)
        survivor_data_game.AddFavTeamTeamRanking(teams_w_rankings)
        # add current game data to list of game data for week
        week_options.append(survivor_data_game)
    
    # return list of game data corresponding to all games in week
    return week_options


  # get starting year, month, and day for week of season
'''  def StartingDateWeekOfSeason(self, year : int, week : int) -> List[int]:
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

    return year_start_week, month_start_week, day_start_week'''
