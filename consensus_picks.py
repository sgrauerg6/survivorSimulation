# class to run data scraping to get consensus picks for each week

import requests
import bs4
import csv

class ConsensusPicks:
  
  def __init__(self):
      pass

  def RetrieveConsenusPicks(self, year, week):
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
      consensus_picks_csv = "consensus_picks_" + str(year) + "_" + str(week) + ".csv"
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