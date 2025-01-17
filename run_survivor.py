from results_odds_all_seasons import ResultsOddsAllSeasons
from survivor_season import SurvivorSeason
from consensus_picks import ConsensusPicks
import sys 

# program takes in NFL season to use for survivor simulation and number of entries
#c_picks = ConsensusPicks()
# retrieve consenus picks for every year
#for year in range(2010, 2025):
#  num_weeks = 18
#  if (year < 2021): num_weeks = 17
#  for week in range(1, num_weeks + 1):
#    c_picks.RetrieveConsenusPicks(year, week)
#    print("Consensus picks done: " + str(year) + " " + str(week))
year = int(sys.argv[1])
print("YEAR: %d" % year)
print("Num entries: %d" % int(sys.argv[2]))
# NFL season had 17 weeks before 2021 and 18 weeks currently
num_weeks = 18
if (year < 2021): num_weeks = 17
surviving_entries = 0
surviving_entries_weighted = 0
'''for f in range(3, 17):
  survivor_season = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]), f, False, False)
  survivor_season_weighted = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]), f, True, False)
  survivor_season_consensus = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]), f, False, True)
  survivor_season_consensus_weighted = SurvivorSeason(int(sys.argv[1]), num_weeks, int(sys.argv[2]), f, True, True)'''
f = 7
for year in range(2010, 2025):
  survivor_season = SurvivorSeason(year, num_weeks, int(sys.argv[2]), f, False, False)
  survivor_season_weighted = SurvivorSeason(year, num_weeks, int(sys.argv[2]), f, True, False)
  survivor_season_consensus = SurvivorSeason(year, num_weeks, int(sys.argv[2]), f, False, True)
  survivor_season_consensus_weighted = SurvivorSeason(year, num_weeks, int(sys.argv[2]), f, True, True)
  num_weeks = 18
  if (year < 2021): num_weeks = 17
  for i in range(num_weeks):
    surviving_entries = survivor_season.ProcessWeek()
    surviving_entries_weighted = survivor_season_weighted.ProcessWeek()
    surviving_entries_consensus = survivor_season_consensus.ProcessWeek()
    surviving_entries_consensus_weighted = survivor_season_consensus_weighted.ProcessWeek()
  print()
  print("Year: " + str(year))
  print("Number of expected winners randomly selected from for each entry: " + str(f))
  print("Surviving entries w/ picks sorted by biggest favorites: " + str(surviving_entries))
  print("Surviving entries w/ picks sorted by biggest favorites (weighted): " + str(surviving_entries_weighted))
  print("Surviving entries w/ picks sorted by consensus selections: " + str(surviving_entries_consensus))
  print("Surviving entries w/ picks sorted by consensus selections (weighted): " + str(surviving_entries_consensus_weighted))

