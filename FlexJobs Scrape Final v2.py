import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

total_jobs = []

def extract_description(soup):
  descriptions = soup.select('.job-description')
  for i, description in enumerate(descriptions):
    joblist[i]['description'] = description.get_text(strip=True)

for x in range(1, 4):
  joblist = []
  url = 'https://www.flexjobs.com/search?location=&search=data+science&page='
  r = requests.get(url + str(x))
  soup = BeautifulSoup(r.content,'html.parser')
  content = soup.find_all('div', class_ = 'col-md-12 col-12')

  for item in content:
    title = item.find('a').text.strip()
    jobage = item.find('div', class_ = 'job-age').text.strip()
    salary = ''
    jobtype = item.find('a', class_ = 'job-title job-link').text.strip()
    location = item.find('div', class_ = 'col pe-0 job-locations text-truncate').text.strip()

    job = {
        'title' : title,
        'jobage' : jobage,
        'salary': salary,
        'description': '',        
        'jobtype' : jobtype,
        'location' : location
    } 
    joblist.append(job)

  extract_description(soup)
  total_jobs.extend(joblist)
  print('jobs found in this iteration:', len(joblist))  

  time.sleep(2)

df = pd.DataFrame(total_jobs)

print(df.head())

df.to_csv('flexjobs.csv')
