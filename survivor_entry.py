# class corresponding to entry in survivor NFL game
# entry consists of team pick each week and winning team of game
# with team that is picked

class SurvivorEntry:
  
  def __init__(self):
    self.picks_results = []
    self.strikes = 0
  
  def AddPick(self, pick):
    self.picks_results.append([pick, 'UNKNOWN'])
  
  def SetLastPickResult(self, result):
    # add result of last pick, where result corresponds to winning team
    # or "TIE" if game is a tie
    self.picks_results[-1][1] = result
    # get number of strikes with current result added
    self.strikes = self.NumStrikes()

  # returns number of "wrong picks" where picked team loses
  # typically in a game of NFL survivor an entry is out once there is one
  # strike, but there are variations that allow multiple strikes 
  # tie is not considered a strike by default but can be set to be
  def NumStrikes(self, tie_is_strike = False):
    strikes = 0
    for pick_result in self.picks_results:
      if tie_is_strike and pick_result[1] == "TIE": strikes != 1
      elif not tie_is_strike and pick_result[1] == "TIE": pass
      elif pick_result[0] != pick_result[1]: strikes += 1
    return strikes
  
  def AllPicks(self):
    picks = []
    for pick_result in self.picks_results:
      picks.append(pick_result[0])
    return picks
  
  def PicksResults(self):
    return self.picks_results

  def PickUsed(self, pick):
    return pick in self.AllPicks()
    