from results_odds_all_seasons import ResultsOddsAllSeasons
from survivor_season import SurvivorSeason
from consensus_picks import ConsensusPicks
from team_rankings import TeamRankings
from survivor_strategy import SurvivorStrategy
import sys

# program takes in NFL season to use for survivor simulation and number of entries
# retrieve year of season and number of starting entries from input arguments
year = int(sys.argv[1])
num_entries = int(sys.argv[2])

# set multiple strategies to make survivor picks
survivor_strategy = SurvivorStrategy() 
survivor_strategy_favorities_weighted = SurvivorStrategy()
survivor_strategy_favorities_weighted.SetWeightPicksByWinPoss(True)
survivor_strategy_consensus = SurvivorStrategy()
survivor_strategy_consensus.SetConsensusPickSettings(True, True) 
survivor_strategy_w_team_rankings = SurvivorStrategy()
survivor_strategy_w_team_rankings.SetTeamRankingsWeight(1.0)
survivor_strategy_w_team_rankings_to_week_10 = SurvivorStrategy()
survivor_strategy_w_team_rankings_to_week_10.SetTeamRankingsWeight(1.0)
survivor_strategy_w_fav_weighted_team_rankings_to_week_10 = SurvivorStrategy()
survivor_strategy_w_fav_weighted_team_rankings_to_week_10.SetTeamRankingsWeight(1.0)
survivor_strategy_w_fav_weighted_team_rankings_to_week_10.SetWeightPicksByWinPoss(True)

for year in range(year, year + 1):
  # initialize multiple survivor seasons, one for each survivor strategy
  survivor_season_no_weighing = SurvivorSeason(year, num_entries)
  survivor_season_weight_favorities = SurvivorSeason(year, num_entries)
  survivor_season_consensus_weighted = SurvivorSeason(year, num_entries)
  survivor_seasons_w_team_rankings = SurvivorSeason(year, num_entries)
  survivor_seasons_w_team_rankings_to_week_10 = SurvivorSeason(year, num_entries)
  survivor_seasons_w_fav_weighted_team_rankings_to_week_10 = SurvivorSeason(year, num_entries)

  # NFL season had 17 weeks before 2021 and 18 weeks after that
  num_weeks = 17 if (year < 2021) else 18

  # go through each week of the season and process survivor entries for week
  # using specified survivor strategy to select teams for each entry
  for week_num in range(num_weeks):
    if week_num >= 9:
      survivor_strategy_w_team_rankings_to_week_10.SetTeamRankingsWeight(0.0)
    surviving_entries_no_weighing = survivor_season_no_weighing.ProcessWeek(survivor_strategy)
    surviving_entries_weight_favories = survivor_season_weight_favorities.ProcessWeek(survivor_strategy_favorities_weighted)
    surviving_entries_consensus_weighted = survivor_season_consensus_weighted.ProcessWeek(survivor_strategy_consensus)
    surviving_entries_w_team_rankings = survivor_seasons_w_team_rankings.ProcessWeek(survivor_strategy_w_team_rankings)
    surviving_entries_w_team_rankings_to_week_10 = survivor_seasons_w_team_rankings_to_week_10.ProcessWeek(survivor_strategy_w_team_rankings_to_week_10)
    surviving_entries_w_fav_weighted_team_rankings_to_week_10 = survivor_seasons_w_fav_weighted_team_rankings_to_week_10.ProcessWeek(survivor_strategy_w_fav_weighted_team_rankings_to_week_10)
  
  # print number of surviving entries in full season using each survivor strategy
  print()
  print("Year: " + str(year))
  print("Num entries at start: " + str(num_entries))
  print("Surviving entries w/ picks randomly selected from favorities: " + str(surviving_entries_no_weighing))
  print("Surviving entries w/ picks weighted to bigger favorities: " + str(surviving_entries_weight_favories))
  print("Surviving entries w/ picks weighted by consensus picks: " + str(surviving_entries_consensus_weighted))
  print("Surviving entries w/ picks weighted by team rankings: " + str(surviving_entries_w_team_rankings))
  print("Surviving entries w/ picks weighted by team rankings (till week 10): " + str(surviving_entries_w_team_rankings_to_week_10))
  print("Surviving entries w/ picks weighted to bigger favorities and team rankings (till week 10): " + str(surviving_entries_w_fav_weighted_team_rankings_to_week_10))