import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

total_jobs = []

def extract_job_information(job_listing):
    title = job_listing.find("a", class_="search-result-title").get_text(strip=True)
    location = job_listing.find("div", class_="search-result-location").get_text(strip=True)
    job_type = job_listing.find("div", class_="search-result-job-type").get_text(strip=True)

    return {
        'title': title,
        'location': location,
        'jobtype': job_type
    }

options = Options()
options.add_argument('--headless')
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

for x in range(1, 2):
    url = f'https://www.flexjobs.com/search?search=data+science&location=&page={x}'
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_listings = soup.find_all('div', class_='search-result')

    jobs_in_iteration = [extract_job_information(job_listing) for job_listing in job_listings]
    total_jobs.extend(jobs_in_iteration)
    print(f'jobs found in this iteration: {len(jobs_in_iteration)}')
    time.sleep(2)

driver.quit()

df = pd.DataFrame(total_jobs)
print(df.head())
df.to_csv('flexjobs.csv')
