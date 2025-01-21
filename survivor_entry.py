# class corresponding to entry in survivor NFL game
# entry consists of team pick each week and winning team of game
# with team that is picked

from typing import List

# class corresponding to entry in survivor NFL game that consists of team pick
# each week and winning team of game with team that is picked
class SurvivorEntry:
  
  # initialize empty survivor entry that will contain picks and results for
  # each week
  def __init__(self):
    self.picks_results = []


  # add pick with unknown result to be added later
  # each pick_results element contains 2 strings w/ pick followed by result
  def AddPick(self, pick) -> None:
    self.picks_results.append([pick, 'UNKNOWN'])
  

  # add result of last pick, where result corresponds to winning team
    # or "TIE" if game is a tie
  def SetLastPickResult(self, result) -> None:
    self.picks_results[-1][1] = result


  # returns number of "wrong picks" where picked team loses
  # typically in a game of NFL survivor an entry is out once there is one
  # strike, but there are variations that allow multiple strikes 
  # tie is not considered a strike by default but can be set to be
  def NumStrikes(self, tie_is_strike = False) -> int:
    strikes = 0
    for pick_result in self.picks_results:
      if tie_is_strike and pick_result[1] == "TIE": strikes != 1
      elif not tie_is_strike and pick_result[1] == "TIE": pass
      elif pick_result[0] != pick_result[1]: strikes += 1
    return strikes
  

  # return all picks that have been used in survivor entry
  def AllPicks(self) -> List[str]:
    picks = []
    for pick_result in self.picks_results:
      picks.append(pick_result[0])
    return picks
  

  # return picks and results for every week of entry
  def PicksResults(self) -> List[List[str]]:
    return self.picks_results


  # check if input team has been used in survivor entry
  # return true if team has been used, false otherwise
  def PickUsed(self, pick) -> bool:
    return pick in self.AllPicks()
    