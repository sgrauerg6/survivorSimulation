# class to correspond to season of survivor where unique team is selected each
# week and goal is to pick winner every week

from results_odds_season import ResultsOddsSeason
from survivor_entry import SurvivorEntry
from enum import Enum
from survivor_strategy import SurvivorStrategy


# class for season of survivor with any number of survivor entries at start
class SurvivorSeason:
  
  # initialize survivor season
  def __init__(self, year, num_entries):
    self.entries = []
    self.num_entries = num_entries
    self.year = year
    self.results = ResultsOddsSeason(self.year, "spreadspoke_scores.csv")
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
  def ProcessWeek(self, survive_picks_strategy) -> int:
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
    index_sort = self.results.ConsensusPickPercentIdxSurvivorWeek() if \
      survive_picks_strategy.UseConsensusPicks() else \
      self.results.PercentWinIdxSurvivorWeek()
    week_options.sort(key=lambda x: x[index_sort], reverse = True)

    # go through each entry and add pick
    # select team in first num_favorites_selection if one available using
    # random selection with weighing according to current settings
    # if all num_favorites_selection teams have been used, choose next most
    # likely to win
    for entry in self.entries:
      if entry.NumStrikes() == 0:
        pick_possibilities = week_options[0:survive_picks_strategy.NumFavoritiesSelectFrom()]
        week_pick = []
        # go through each of the favorite pick possibilities
        # and remove if pick already used in entry
        for pick_poss in pick_possibilities:
          if entry.PickUsed(pick_poss[0]):
            pick_possibilities.remove(pick_poss)
        if pick_possibilities:
          week_pick = survive_picks_strategy.PickForEntry(pick_possibilities)
        else:
          # if all favorite pick possibilities used, select next
          # favorite that has not been used
          for pick_poss in week_options[self.num_favorites_selection:]:
            if not entry.PickUsed(pick_poss[0]):
              week_pick = pick_poss
              break
        
        # add pick to win to current survivor entry
        entry.AddPick(week_pick[0])

        # add result of game with pick to current survivor entry
        entry.SetLastPickResult(week_pick[2])

    # return number of entries that "survived" the current week    
    return self.RemainingEntries()

    