# class to correspond to season of survivor where unique team is selected each
# week and goal is to pick winner every week

from results_odds_all_seasons import ResultsOddsAllSeasons
from survivor_entry import SurvivorEntry
import random
import math

class SurvivorSeason:
  
  def __init__(self, year, num_weeks, num_entries):
    self.entries = []
    self.num_entries = num_entries
    self.year = year
    self.weeks = num_weeks
    self.results = ResultsOddsAllSeasons("spreadspoke_scores.csv")
    self.week_num = 0
    self.num_favorites_selection = 7
    for i in range(self.num_entries):
      self.entries.append(SurvivorEntry())
  
  def RemainingEntries(self):
    num_remaining = 0
    for entry in self.entries:
      if entry.NumStrikes() == 0: num_remaining += 1
    return num_remaining
  
  def WeightFavorite(self, percent_favorite):
    return (float(percent_favorite) - 50.0) / 50.0

  def WeightedPick(self, pick_possibilities):
    weights_picks = []
    for pick_poss in pick_possibilities:
      weights_picks.append(1.0 + self.WeightFavorite(pick_poss[1]))
    print(pick_possibilities)
    print(weights_picks)
    choice = random.choices(pick_possibilities, weights = weights_picks)[0]
    print(choice)
    return choice

  def ProcessWeek(self):
    self.week_num += 1
    week_options = self.results.SurvivorWeekOptions(self.year, self.week_num)
    print("WEEK " + str(self.week_num))
    print(week_options)
    print("Number of entries at start of week: " + str(self.RemainingEntries()))
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
          week_pick = self.WeightedPick(pick_possibilities)
          #week_pick = random.choice(pick_possibilities)
        else:
          # if all favorite pick possibilities used, select next
          # favorite that has not been used
          for pick_poss in week_options[self.num_favorites_selection:]:
            if not entry.PickUsed(pick_poss[0]):
              week_pick = pick_poss
              break
        entry.AddPick(week_pick[0])
        print("")
        print("Entry pick w/ result: " + week_pick[0] + " " + week_pick[2])
        entry.SetLastPickResult(week_pick[2])
        if (entry.NumStrikes() == 0):
          print("Entry survived: " + str(entry.AllPicks()))
        else:
          print("Entry lost: " + str(entry.AllPicks()))
    print("")
    print("Number of entries left: " + str(self.RemainingEntries()))
    print("")

    