import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

total_jobs = []

def extract_description(soup):
  # Extract job descriptions from each job listing and append to joblist dictionary
  descriptions = soup.select('.job-description')
  for i, description in enumerate(descriptions):
    joblist[i]['description'] = description.decode_contents()

# Loop through first two pages of FlexJobs search results
for x in range(1, 3):
  joblist = []
  url = 'https://www.flexjobs.com/search?location=&search=data+science&page='
  r = requests.get(url + str(x))
  soup = BeautifulSoup(r.content,'html.parser')

  # Find all job listings on the page
  content = soup.find_all('div', class_ = 'col-md-12 col-12')

  # Loop through each job listing and extract relevant information
  for item in content:
    title = item.find('a').text.strip()

    # Job age not used in this version, but left in for reference
    jobage = item.find('div', class_ = 'job-age').text.strip()

    # Salary not available in job listing, so set to blank
    salary = ''

    jobtype = item.find('a', class_ = 'job-title job-link').text.strip()

    location = item.find('div', class_ = 'col pe-0 job-locations text-truncate').text.strip()

    # Create dictionary for job and append to joblist
    job = {
        'title' : title,
        'jobage' : jobage,
        'salary': salary,        
        'jobtype' : jobtype,
        'location' : location
    } 
    joblist.append(job)

  # Extract job descriptions for each job listing
  extract_description(soup)

  # Append joblist for this page to the total_jobs list
  total_jobs.extend(joblist)

  # Print number of jobs found in this iteration
  print('jobs found in this iteration:', len(joblist))  

  # Wait 2 seconds to avoid overloading server with requests
  time.sleep(2)

# Create pandas dataframe with all job listings and save to CSV file
df = pd.DataFrame(total_jobs)
df.to_csv('flexjobs.csv')
