# class to run data scraping to get consensus picks for each week

import requests
import bs4
import csv

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
  
  def __init__(self):
      pass

  def RetrieveTeamRankings(self, year, week):
      '''URL = "https://www.teamrankings.com/nfl/ranking/predictive-by-other?date=" + date_str
      print(URL)
      req = requests.get(URL)
      soup = bs4.BeautifulSoup(req.text, 'html.parser')
      table = soup.find_all('table')[0]
      rows = table.find_all('tr')
      headers = []
      cells = rows[0].find_all('th')
      for cell in cells:
        headers.append(cell.text.split()[0])
      team_rankings_csv = "team_rankings_" + str(year) + "_" + str(week) + ".csv"
      with open(team_rankings_csv, 'w', newline='',encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers[1:3])
        for row in rows[1:]:
          data_out = []
          cells = row.find_all('td')
          data_out.append((cells[1].text.split('%')[0]).split(" (")[0])
          #data_out.append(cells[0].text.split()[0])
          #for i in range(1, len(headers)):
          data_out.append(cells[2].text.split('%')[0])
          writer.writerow(data_out)'''
      # get team rankings picks for week
      team_rankings_file = "team_rankings_" + str(year) + "_" + str(week) + ".csv"
      with open(team_rankings_file, newline='') as f:
        reader = csv.reader(f)
        team_rankings_data = list(reader)
      team_rankings = {}
      headers_row = team_rankings_data[0]
      min_ranking = 0
      max_ranking = 0
      for row in team_rankings_data[1:]:
        try:
          min_ranking = min(min_ranking, float(row[1]))
          max_ranking = max(max_ranking, float(row[1]))
        except:
          pass
      diff_max_min_ranking = max_ranking - min_ranking
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
