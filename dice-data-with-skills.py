# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:51 2023
​
@author: Melissa Bridges
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time
import logging

# disable logging for the page_load_metrics_update_dispatcher module
logging.getLogger('page_load_metrics_update_dispatcher').disabled = True

import warnings
warnings.filterwarnings("ignore", message="The argument 'infer_datetime_format' is deprecated and will be removed in a future version.")


urls = ['https://www.dice.com/jobs?q=data%20architect&countryCode=US&radius=30&radiusUnit=mi&pageSize=50&language=en&page=',
       'https://www.dice.com/jobs?q=data%20analyst&countryCode=US&radius=30&radiusUnit=mi&pageSize=50&language=en&page=',
       'https://www.dice.com/jobs?q=data%20engineer&countryCode=US&radius=30&radiusUnit=mi&pageSize=50&language=en&page=',
       'https://www.dice.com/jobs?q=data%20scientist&countryCode=US&radius=30&radiusUnit=mi&pageSize=50&language=en&page='
       ]

joblist = []  # initialize joblist outside the outer loop
# set your chrome driver path: for instance, mine was in C:/Program Files/Python311/chromedriver.exe
chrome_driver_path = os.path.join('C:', os.sep, 'Program Files', 'Python311', 'chromedriver.exe')

# Set Chrome options to run in headless mode
options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument('--headless')

# Initialize WebDriver with the Chrome options
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

for url in urls:

    for page in range(1,5):
        driver.get(f'{url}{page}')
        try:
            WebDriverWait(driver, 5).until(lambda s: s.find_elements(By.CLASS_NAME,"card"))
        except TimeoutException:
            print("TimeoutException: Element not found")

        soup = BeautifulSoup(driver.page_source, "lxml")
        job_links = soup.select("a.card-title-link")
        list_of_jobs = []  # create a new list to hold the jobs for this iteration
        
        for link in job_links:
            try:
                # get the url to the full description page
                desc_url = link['href']
                # go to the full description page
                driver.get(desc_url)
                time.sleep(5)
            except:
                pass

            try:
                # click on the "Read Full Description" button
                read_more_button = driver.find_element_by_css_selector('.collapse.show-more-less-btn')
                read_more_button.click()
            except:
                pass

            desc_soup = BeautifulSoup(driver.page_source, "lxml")
        
            # get job title
            try:
                title = desc_soup.select_one('h1[data-cy="jobTitle"]').text
            except:
                title = ''

            # get company name
            try:
                company = desc_soup.select_one('a[data-cy="companyNameLink"]').text
            except:
                company = ''

            # get location
            try:
                location = desc_soup.select_one('li[data-cy="companyLocation"]').text
            except:
                location = ''

            # get job type
            try:
                job_type = desc_soup.select_one('p[data-cy="employmentType"]').text
            except:
                job_type = ''

            # get salary
            try:
                salary = desc_soup.select_one('p[data-cy="compensationText"]').text
            except:
                salary = ''

            # get skill list
            skill_list = []

            try:
                # find the div element containing the skills
                skills_div = desc_soup.select_one('div[data-cy="skillsList"]')

                # extract the list of skills and join them as a string
                skill_list = ', '.join([skill.text for skill in skills_div.select('span.skill-badge')]).strip()
                print(skill_list)

            except AttributeError:
                print("Could not find skills section")
            
            # get job description
            # try:
            #     description = desc_soup.select_one('div#jobDescription > div[data-testid="jobDescriptionHtml"]').text
            # except:
            #     description = ''

            # get posted date
            try:
                posted_date = desc_soup.select_one('dhi-time-ago[classname="time-stamp"]').get('posted-date')
            except:
                posted_date = ''

            # get the date string in a standard format
            if posted_date:
                posted_date = posted_date.replace("Posted: ", "").strip()
                if posted_date:
                    posted_date = pd.to_datetime(posted_date, infer_datetime_format=True, errors='coerce').strftime('%m-%d-%Y')

            job = {
                'title' : title,
                'company' : company,
                # 'description' : description,
                'skills' : skill_list,
                'location' : location,
                'posted_date' : posted_date,
                'type' : job_type,
                'salary' : salary
            }
            joblist.append(job) # append the current job dictionary to the list of jobs

            for url in urls:
                search_term = url.split('=')[1].split('&')[0].replace('%20', ' ')
            
    print(f"Web scrape for {search_term} is complete. Moving onto the next.")

df = pd.DataFrame(joblist)
print(df.head(10))
df.to_csv('dice_data_test-fullDesc.csv')
driver.close()