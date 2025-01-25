# class to correspond to season of survivor where unique team is selected each
# week and goal is to pick winner every week

from results_odds_season import ResultsOddsSeason
from survivor_entry import SurvivorEntry
from enum import Enum
from survivor_strategy import SurvivorStrategy
import copy


# class for season of survivor with any number of survivor entries at start
class SurvivorSeason:

  # path of file with results and odds for all seasons
  kResultsOddsAllSeasonsFilePath = "spreadspoke_scores.csv"
  
  # initialize survivor season
  def __init__(self, year : int, num_entries : int):
    self.entries = []
    self.num_entries = num_entries
    self.year = year
    self.results = ResultsOddsSeason(self.year, SurvivorSeason.kResultsOddsAllSeasonsFilePath)
    self.week_num = 0
    for i in range(self.num_entries):
      self.entries.append(SurvivorEntry())
  

  # get number of entries that are remaining with no wrong picks
  def RemainingEntries(self) -> int:
    num_remaining = 0
    for entry in self.entries:
      if entry.NumStrikes() == 0: num_remaining += 1
    return num_remaining


  # process week of survivor with any number of entries
  def ProcessWeek(self, survive_picks_strategy : SurvivorStrategy) -> int:
    # increment week
    self.week_num += 1

    # get list with survivor week options for week
    # each row of list contains favored team in game, percent chance to win
    # (based on odds), consensus pick %, team ranking, and winning team of
    # game
    # only favored teams are considered
    week_options = self.results.SurvivorWeekOptions(self.year, self.week_num)

    # sort team options for week by most popular consensus picks or by most
    # favored to win depending on current setting
    if (survive_picks_strategy.use_consensus_picks):
      week_options.sort(key=lambda game_data: game_data.fav_team_consensus_pick_percent, reverse = True)
    else:
      week_options.sort(key=lambda game_data: game_data.fav_team_win_percent, reverse = True)

    # go through each entry and add pick
    # select team in first num_favorites_selection if one available using
    # random selection with weighing according to current settings
    # if all num_favorites_selection teams have been used, choose next most
    # likely to win
    for entry in self.entries:
      if entry.NumStrikes() == 0:
        # generate initial list of pick possibilities from top favorities (or consensus picks if that
        # survivor strategy used)
        pick_possibilities = week_options[0:survive_picks_strategy.num_favorities_select_from]
        week_pick = []

        # generate list of picks to remove since already used in previous week
        possibilities_remove = []
        for pick_poss in pick_possibilities:
          if entry.PickUsed(pick_poss.favored_team):
            possibilities_remove.append(pick_poss)

        # remove picks already used from list of pick possibilities
        for poss_remove in possibilities_remove:
            pick_possibilities.remove(poss_remove)
        if pick_possibilities:
          week_pick = survive_picks_strategy.PickForEntry(pick_possibilities)
        else:
          # if all favorite pick possibilities used, select next
          # favorite that has not been used
          for pick_poss in week_options[survive_picks_strategy.num_favorities_select_from:]:
            if not entry.PickUsed(pick_poss.favored_team):
              week_pick = pick_poss
              break

        if entry.PickUsed(week_pick.favored_team):
            print("PICK USED: " + week_pick.favored_team)
            print(str(entry.AllPicks()))
            pick_poss_fav = []
            for pick_poss in pick_possibilities:
               pick_poss_fav.append(pick_poss.favored_team)
            print(pick_poss_fav)
        
        # add pick to win to current survivor entry
        entry.AddPick(week_pick.favored_team)

        # add result of game with pick to current survivor entry
        entry.SetLastPickResult(week_pick.winning_team)

    # return number of entries that "survived" the current week    
    return self.RemainingEntries()

    
