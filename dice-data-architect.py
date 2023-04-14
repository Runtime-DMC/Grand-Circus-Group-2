from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import os


url = 'https://www.dice.com/jobs?q=data%20architect&countryCode=US&radius=30&radiusUnit=mi&pageSize=100&language=en&page='

# download chromedriver for your OS from https://chromedriver.storage.googleapis.com/index.html?path=92.0.4515.43/ and set the path below
#driver = webdriver.Chrome('/Users/jayashree/Downloads/chromedriver_mac64/chromedriver')
chrome_driver_path = os.path.join('C:', os.sep, 'Program Files', 'Python311', 'chromedriver.exe')
driver = webdriver.Chrome(chrome_driver_path)
joblist = []

#for page in range(1,3):
for page in range(1,10):
    driver.get(f'{url}{page}')
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_elements(By.CLASS_NAME,"card"))
    except TimeoutException:
        print("TimeoutException: Element not found")
        #exit()


    soup = BeautifulSoup(driver.page_source, "lxml")
    jobs = soup.select("div.card.search-card")
    for job in jobs:
        title = ''
        company = ''
        location = ''
        description = ''
        posted_date = ''
        try:
            if(job.select('.card-title-link')[0]):
                title = job.select('.card-title-link')[0].text
            if(job.select('.card-company a')[0]):
                company = job.select('.card-company a')[0].text
            if(job.select('.search-result-location')[0]):
                location = job.select('.search-result-location')[0].text
            if(job.select('.card-description')[0]):
                description = job.select('.card-description')[0].text
            if(job.select('.posted-date')[0]):
                posted_date = job.select('.posted-date')[0].text
        except:
            pass

        job = {
            'title' : title,
            'company' : company,
            'description' : description,
            'location' : location,
            'posted_date' : posted_date
        }
        joblist.append(job)

df = pd.DataFrame(joblist)
print(df.head(10))
df.to_csv('dice_DataArchitect_2023.csv')
#driver.close()
