from results_odds_all_seasons import ResultsOddsAllSeasons
from survivor_season import SurvivorSeason
import sys 

# program takes in NFL season to use for survivor simulation and number of entries
year = int(sys.argv[1])
num_weeks = 18
print("YEAR: %d" % year)
print("Num entries: %d" % int(sys.argv[2]))
# NFL season had 17 weeks before 2021 and 18 weeks currently
num_weeks = 18
if (year < 2021): num_weeks = 17
survivor_season = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]))
for i in range(num_weeks):
  survivor_season.ProcessWeek()