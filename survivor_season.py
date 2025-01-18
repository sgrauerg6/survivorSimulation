# class to correspond to season of survivor where unique team is selected each
# week and goal is to pick winner every week

from results_odds_all_seasons import ResultsOddsAllSeasons
from survivor_entry import SurvivorEntry
import random
import math
from enum import Enum

class PickMethod(Enum):
    FAVORITE_ONLY = 1
    CONSENSUS_W_FAVORITE = 2
    TEAM_RANKING_W_FAVORITE = 3

class SurvivorSeason:
  
  def __init__(self, year, num_weeks, num_entries, num_favorities_selection, weight_favorities, pick_method):
    self.entries = []
    self.num_entries = num_entries
    self.year = year
    self.weeks = num_weeks
    self.results = ResultsOddsAllSeasons("spreadspoke_scores.csv")
    self.week_num = 0
    self.num_favorites_selection = num_favorities_selection
    self.weight_favories = weight_favorities
    self.pick_method = pick_method
    for i in range(self.num_entries):
      self.entries.append(SurvivorEntry())
  
  # get number of entries that are remaining with no wrong picks
  def RemainingEntries(self):
    num_remaining = 0
    for entry in self.entries:
      if entry.NumStrikes() == 0: num_remaining += 1
    return num_remaining
  
  def WeightFavorite(self, percent_favorite):
    return (float(percent_favorite) - 50.0) / 50.0

  # set pick using weighing where teams that are more favored or have a larger
  # percent of being picked are more likely to be picked
  def WeightedPick(self, pick_possibilities):
    weights_picks = []
    for pick_poss in pick_possibilities:
      if self.pick_method == PickMethod.FAVORITE_ONLY:
        weights_picks.append(1.0 + self.WeightFavorite(pick_poss[1]))
      else:
        weights_picks.append(pick_poss[3])
    choice = random.choices(pick_possibilities, weights = weights_picks)[0]
    return choice

  def WeightRankings(self, team_ranking):
    return ()
  
  # select team using team rankings where teams lower in rankings are weighted
  # more in earlier weeks
  def PickWTeamRankings(self, pick_possibilities):
    choice = []
    if (self.week_num > 10):
      if self.weight_favories: choice = self.WeightedPick(pick_possibilities)
      else: choice = random.choice(pick_possibilities)
    else:
      weights_picks = []
      for pick_poss in pick_possibilities:
        weights_picks.append(1.0 - pick_poss[4])
      choice = random.choices(pick_possibilities, weights = weights_picks)[0]
    return choice

  def ProcessWeek(self):
    self.week_num += 1
    week_options = self.results.SurvivorWeekOptions(self.year, self.week_num)
    # sort team options for week by most popular consensus picks or by most
    # favored to win depending on current setting
    index_sort = self.results.PercentWinIdxSurvivorWeek()
    if self.pick_method == PickMethod.CONSENSUS_W_FAVORITE:
      index_sort = self.results.ConsensusPickPercentIdxSurvivorWeek()
    week_options.sort(key=lambda x: x[index_sort], reverse = True) 
    # go through each entry and add pick
    # select random pick of first num_favorites_selection if one available, if not choose next most likely to win
    for entry in self.entries:
      if entry.NumStrikes() == 0:
        pick_possibilities = week_options[0:self.num_favorites_selection]
        week_pick = []
        # go through each of the favorite pick possibilities
        # and remove if pick already used in entry
        for pick_poss in pick_possibilities:
          if entry.PickUsed(pick_poss[0]):
            pick_possibilities.remove(pick_poss)
        if pick_possibilities:
          # make random selection from favorite pick possibilites
          # if at least one hasn't been used
          # add weighing of each pick based on how much of a favorite it is
          week_pick = pick_possibilities[0]
          if self.pick_method == PickMethod.TEAM_RANKING_W_FAVORITE:
            week_pick = self.PickWTeamRankings(pick_possibilities)
          elif self.weight_favories: week_pick = self.WeightedPick(pick_possibilities)
          else: week_pick = random.choice(pick_possibilities)
        else:
          # if all favorite pick possibilities used, select next
          # favorite that has not been used
          for pick_poss in week_options[self.num_favorites_selection:]:
            if not entry.PickUsed(pick_poss[0]):
              week_pick = pick_poss
              break
        entry.AddPick(week_pick[0])
        entry.SetLastPickResult(week_pick[2])
    return self.RemainingEntries()

    