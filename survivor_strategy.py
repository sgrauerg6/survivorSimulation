# Class to define survivor strategy for week

import random
import math
from typing import List

class SurvivorStrategy:

  def __init__(self):
    self.num_favorities_select_from = 7
    self.use_consensus_picks = False
    self.weigh_consensus_picks = True
    self.weight_picks_by_win_poss = False
    self.team_rankings_weight = 0.0

  
  # get the number of favorities to select from for each survivor entry
  def NumFavoritiesSelectFrom(self) -> int:
    return self.num_favorities_select_from


  def SetNumFavoritiesSelectFrom(self, num_select_from) -> None:
    self.num_favorities_select_from = num_select_from


  def SetWeightPicksByWinPoss(self, weight_picks_by_win_poss) -> None:
    self.weight_picks_by_win_poss = weight_picks_by_win_poss


  # team rankings weight can be set between 0.0 and 1.0
  # with 1.0 having the most effect
  def SetTeamRankingsWeight(self, team_rankings_weight) -> None:
    # clamp team ranking weight to be between 0 and 1
    team_rankings_weight = max(0.0, min(team_rankings_weight, 1.0))
    self.team_rankings_weight = team_rankings_weight


  # set consensus pick settings
  # note that setting to use consensus picks overrides other settings
  def SetConsensusPickSettings(self, use_consensus_picks, weigh_consensus_picks = True) -> None:
    self.use_consensus_picks = use_consensus_picks
    self.weigh_consensus_picks = weigh_consensus_picks


  # return whether or not consensus picks are used
  def UseConsensusPicks(self) -> bool:
    return self.use_consensus_picks


  # set pick using weighing of consensus picks where teams that have a larger
  # percent of being picked are more likely to be picked
  def __WeightedConsensusPick(self, pick_possibilities):
    weights_picks = []
    for pick_poss in pick_possibilities:
      weights_picks.append(pick_poss[3])
    choice = random.choices(pick_possibilities, weights = weights_picks)[0]
    return choice


  # set weight for favorite
  def __WeightFavorite(self, percent_favorite) -> float:
    return (float(percent_favorite) - 50.0) / 50.0


  # set pick using weighing where teams that are more favored or have a larger
  # percent of being picked are more likely to be picked
  def __WeightedPick(self, pick_possibilities):
    weights_picks = []
    for pick_poss in pick_possibilities:
      weights_picks.append(1.0 + self.__WeightFavorite(pick_poss[1]))
    choice = random.choices(pick_possibilities, weights = weights_picks)[0]
    return choice


  # select team using team rankings where teams lower in rankings are weighted
  # more in earlier weeks
  def __PickWTeamRankings(self, pick_possibilities):
    choice = []
    weights_picks = []
    for pick_poss in pick_possibilities:
      pick_weight = (1.0 - pick_poss[4]) + ((1.0 - self.team_rankings_weight) * 2)
      if self.weight_picks_by_win_poss:
        pick_weight += 1.0 + self.__WeightFavorite(pick_poss[1])
      weights_picks.append(pick_weight)
    choice = random.choices(pick_possibilities, weights = weights_picks)[0]
    return choice


  # make pick for entry using current survivor strategy
  # assumed that there is at least one option in pick_options
  def PickForEntry(self, pick_options):
    # make selection for survivor entry for week from one or more options
    if self.use_consensus_picks:
      # process selection using consensus picks and process accordingly if so
      if self.weigh_consensus_picks:
        return self.__WeightedConsensusPick(pick_options)
      else:
        return random.choice(pick_options)
    elif self.team_rankings_weight > 0:
      # pick team using team rankings as part of weighing where "lesser" teams
      # according to rankings are more likely to be picked so stronger teams
      # saved for future weeks
      return self.__PickWTeamRankings(pick_options)
    elif self.weight_picks_by_win_poss:
      # weight picks so that bigger favorities are more likely to be picked
      return self.__WeightedPick(pick_options)
    else:
      # make selection with all possibilities having equal chance of being
      # selected
      return random.choice(pick_options)
    