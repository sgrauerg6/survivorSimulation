# class to run data scraping to get consensus picks for each week

import requests
import bs4
import csv
from typing import Dict

# class to run data scraping to get consensus picks for each week and to
# retrieve file path for consensus picks for week
class ConsensusPicks:

  # consensus picks folder directory
  kConsensusPicksDir = "Data/ConsensusPicks"

  # dictionary of team abbreviation used in consenus picks to abbreviation used in processing
  # only given if different from team abbreviation used in processing
  kConsPicksAbbrevToProcAbbrev = {
    "STL" : "LAR",
    "OAK" : "LVR",
    "LV" : "LVR",
    "SD" : "LAC",
    "WSH" : "WAS"
  }

  # get file path for consensus picks for given year and week
  @staticmethod
  def ConsensusPicksFilePath(year, week) -> str:
    return ConsensusPicks.kConsensusPicksDir + "/consensus_picks_" + str(year) + "_" + str(week) + ".csv"


  # get consensus picks for given year and week
  # returns dictionary of team to consensus pick percent for each team for week
  @staticmethod
  def ConsensusPicksForWeek(year, week) -> Dict[str, float]:
    consensus_picks_file = ConsensusPicks.ConsensusPicksFilePath(year, week)
    with open(consensus_picks_file, newline='') as f:
      reader = csv.reader(f)
      consensus_picks_data = list(reader)
    consensus_pick_team = {}
    column_num_average = 0
    headers_row = consensus_picks_data[0]
    for i in range(0, len(headers_row)): 
      if headers_row[i] == "Average":
        column_num_average = i
        break
    for row in consensus_picks_data[1:]:
      team = row[0]
      # adjust team abbreviation if needed to match team abbreviation used
      # in processing
      if team in ConsensusPicks.kConsPicksAbbrevToProcAbbrev:
        team = ConsensusPicks.kConsPicksAbbrevToProcAbbrev[row[0]]
      consensus_pick_team[team] = float(row[column_num_average])
    return consensus_pick_team


  # retrieve consensus survivor picks for week and year from web scraping and save to csv
  @staticmethod
  def RetrieveConsenusPicks(year, week) -> None:
      URL = "https://www.survivorgrid.com/picks/" + str(year) + "/" + str(week)
      print(URL)
      req = requests.get(URL)
      soup = bs4.BeautifulSoup(req.text, 'html.parser')
      table = soup.find_all('table')[0]
      rows = table.find_all('tr')
      headers = []
      cells = rows[0].find_all('th')
      for cell in cells:
        headers.append(cell.text.split()[0])
      consensus_picks_csv = ConsensusPicks.ConsensusPicksFilePath(year, week)
      with open(consensus_picks_csv, 'w', newline='',encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        for row in rows[1:]:
          data_out = []
          cells = row.find_all('td')
          data_out.append(cells[0].text.split()[0])
          for i in range(1, len(headers)):
            data_out.append(cells[i].text.split('%')[0])
          writer.writerow(data_out)