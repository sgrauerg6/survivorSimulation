# class to run data scraping to get consensus picks for each week

import requests
import bs4
import csv
from typing import Dict

class TeamRankings:

  # dictionary of team names from team ranking to abbreviation used in processing
  kTeamRankingNameToAbbrev = {
    "Arizona" : "ARI",
    "Atlanta" : "ATL",
    "Baltimore" : "BAL",
    "Buffalo" : "BUF",
    "Carolina" : "CAR",
    "Chicago" : "CHI",
    "Cincinnati" : "CIN",
    "Cleveland" : "CLE",
    "Dallas" : "DAL",
    "Denver" : "DEN",
    "Detroit" : "DET",
    "Green Bay" : "GB",
    "Houston" : "HOU",
    "Indianapolis" : "IND",
    "Jacksonville" : "JAX",
    "Kansas City" : "KC",
    "Las Vegas" : "LVR",
    "LA Chargers" : "LAC",
    "LA Rams" : "LAR",
    "Miami" : "MIA",
    "Minnesota" : "MIN",
    "New England" : "NE",
    "New Orleans" : "NO",
    "NY Giants" : "NYG",
    "NY Jets" : "NYJ",
    "Philadelphia" : "PHI",
    "Pittsburgh" : "PIT",
    "San Francisco" : "SF",
    "Seattle" : "SEA",
    "Tampa Bay" : "TB",
    "Tennessee" : "TEN",
    "Washington" : "WAS"
  }

  # prefix of web address for team rankings
  kTeamRankingsURLPrefix = "https://www.teamrankings.com/nfl/ranking/predictive-by-other?date="

  # directory path of team rankings files
  kTeamRankingsDirPath = "Data/TeamRankings"

  # prefix of team rankings file name
  kTeamRankingsFileNamePrefix = "team_rankings_"


  # retrieve team rankings for given date from web
  # retrieved data is stored in csv file with file name including survivor week
  # and year 
  @staticmethod
  def RankingsWebToCsv(rankings_year : int, rankings_month : int, rankings_day : int, survivor_year : int, survivor_week : int) -> None:
    date_str = str(rankings_year) + "-" + str(rankings_month).zfill(2) + "-" + str(rankings_day).zfill(2)
    URL = TeamRankings.kTeamRankingsURLPrefix + date_str
    print(URL)
    req = requests.get(URL)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    headers = []
    cells = rows[0].find_all('th')
    for cell in cells:
      headers.append(cell.text.split()[0])
    team_rankings_csv = TeamRankings.kTeamRankingsFileNamePrefix + str(survivor_year) + "_" + str(survivor_week) + ".csv"
    with open(team_rankings_csv, 'w', newline='',encoding='utf-8') as outfile:
      writer = csv.writer(outfile)
      writer.writerow(headers[1:3])
      for row in rows[1:]:
        data_out = []
        cells = row.find_all('td')
        data_out.append((cells[1].text.split('%')[0]).split(" (")[0])
        data_out.append(cells[2].text.split('%')[0])
        writer.writerow(data_out)


  # get team rankings picks for week
  # return dictionary of team to ranking scaled between 0.0 and 1.0
  @staticmethod
  def RetrieveTeamRankings(year : int, week : int) -> Dict[str, float]:
    kTeamRankingColumnIdx = 1
    kTeamRankingRowStart = 1
    team_rankings_file = TeamRankings.kTeamRankingsDirPath + "/" + TeamRankings.kTeamRankingsFileNamePrefix + str(year) + "_" + str(week) + ".csv"
    with open(team_rankings_file, newline='') as f:
      reader = csv.reader(f)
      team_rankings_data = list(reader)

    # get min and max team ranking to use for scaling
    min_ranking = 0
    max_ranking = 0
    for row in team_rankings_data[kTeamRankingRowStart:]:
      try:
        min_ranking = min(min_ranking, float(row[kTeamRankingColumnIdx]))
        max_ranking = max(max_ranking, float(row[kTeamRankingColumnIdx]))
      except:
        pass
    diff_max_min_ranking = max_ranking - min_ranking

    # scale team rankings to be between 0 and 1
    # if not team ranking available or can't be read, set team ranking to 0.5
    team_rankings = {}
    for row in team_rankings_data[1:]:
      try:
        if diff_max_min_ranking != 0:
          ranking = (float(row[1]) - min_ranking) / diff_max_min_ranking
          team_rankings[TeamRankings.kTeamRankingNameToAbbrev[str(row[0])]] = ranking
        else:
          team_rankings[TeamRankings.kTeamRankingNameToAbbrev[str(row[0])]] = 0.5
      except:
        team_rankings[TeamRankings.kTeamRankingNameToAbbrev[str(row[0])]] = 0.5
    return team_rankings
