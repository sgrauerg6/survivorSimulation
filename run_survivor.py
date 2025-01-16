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
surviving_entries = 0
surviving_entries_weighted = 0
for f in range(3, 17):
  survivor_season = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]), f, False)
  survivor_season_weighted = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]), f, True)
  for i in range(num_weeks):
    surviving_entries = survivor_season.ProcessWeek()
    surviving_entries_weighted = survivor_season_weighted.ProcessWeek()
  print("Num favorities selected from: " + str(f))
  print("Survivoring entries: " + str(surviving_entries))
  print("Survivoring entries weighted selections: " + str(surviving_entries_weighted))

