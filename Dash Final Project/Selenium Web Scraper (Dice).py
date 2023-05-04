# Seleium Web Scraper (Dice)

# Import all the necessary libraries
# You will need to pip install bs4, selenium, pandas, os, time, and logging
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

# Ignore warning about 'infer_datetime_format' argument being deprecated
# (this warning will be removed in a future version of Pandas)
import warnings
warnings.filterwarnings("ignore", message="The argument 'infer_datetime_format' is deprecated and will be removed in a future version.")


# Creates a new list that includes the base URLs to be scraped
# q=data%20architect is the search term (%20 is a space),&pageSize=50 indicates how many listings per page
# for future reference, if the full URL is 'https://www.dice.com/jobs?q=data%20architect&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=50&language=en&eid=S2Q_'
# you only need the part up to and including 'https://www.dice.com/jobs?q=data%20architect&countryCode=US&radius=30&radiusUnit=mi&page='
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
options.add_argument('--headless') # the code will NOT open a chrome browser; saves loading time

# Initialize WebDriver with the Chrome options
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# loop over each URL to scrape job postings for each job title
for url in urls:

    # loop over each page of search results
    for page in range(1,5):
        # load the search results page for the current job title and page number
        driver.get(f'{url}{page}')
        # wait for the job cards to load on the page; may need to add more time depending on your scraping needs
        try:
            WebDriverWait(driver, 5).until(lambda s: s.find_elements(By.CLASS_NAME,"card"))
        except TimeoutException:
            print("TimeoutException: Element not found")

        # parse the HTML content of the search results page using Beautiful Soup
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        # extract the job links from the search results page
        job_links = soup.select("a.card-title-link")
        list_of_jobs = []  # create a new list to hold the jobs for this iteration
        
        # loop over each job link and scrape the full job description
        for link in job_links:
            try:
                # get the url to the full description page
                desc_url = link['href']
                # navigate to the full job description page
                driver.get(desc_url)
                time.sleep(5)
            except:
                pass

            try:
                # click on the "Read Full Description" button to expand the job description
                read_more_button = driver.find_element_by_css_selector('.collapse.show-more-less-btn')
                read_more_button.click()
            except:
                pass

            # parse the HTML content of the full job description page using Beautiful Soup
            desc_soup = BeautifulSoup(driver.page_source, "lxml")
        
            # get job title; if it doesn't have one, it'll show as NaN
            try:
                title = desc_soup.select_one('h1[data-cy="jobTitle"]').text
            except:
                title = ''

            # get company name; if it doesn't have one, it'll show as NaN
            try:
                company = desc_soup.select_one('a[data-cy="companyNameLink"]').text
            except:
                company = ''

            # get location; if it doesn't have one, it'll show as NaN
            try:
                location = desc_soup.select_one('li[data-cy="companyLocation"]').text
            except:
                location = ''

            # get job type; if it doesn't have one, it'll show as NaN
            try:
                job_type = desc_soup.select_one('p[data-cy="employmentType"]').text
            except:
                job_type = ''

            # get salary; if it doesn't have one, it'll show as NaN
            try:
                salary = desc_soup.select_one('p[data-cy="compensationText"]').text
            except:
                salary = ''

            # get job description
            try:
                description = desc_soup.select_one('div#jobDescription > div[data-testid="jobDescriptionHtml"]').text
            except:
                description = ''

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

            # Creates a dictionary that contains all the info for a single job posting
            job = {
                'title' : title,
                'company' : company,
                'description' : description,
                'skills' : skill_list,
                'location' : location,
                'posted_date' : posted_date,
                'type' : job_type,
                'salary' : salary
            }
            joblist.append(job) # append the current job dictionary to the list of jobs

            # Creates a search_term variable that holds the current job title
            # being scraped from the 'urls' list
            for url in urls:
                search_term = url.split('=')[1].split('&')[0].replace('%20', ' ')
            
    # Prints out "Web scrape for 'search_term' is complete" in the command line
    print(f"Web scrape for {search_term} is complete.")

# converts the list of the job postings 'joblist' to a Pandas DataFrame
df = pd.DataFrame(joblist)
# writes the DF created in the previous step to a new CSV file called 'dice_webscrape.csv'
df.to_csv('dice_webscrape.csv')
# provides a summary of descriptive statistics for the numerical columns in the DataFrame
df.describe()
# prints the top 10 rows of the DF to the console for inspection
print(df.head(10))
# closes the Chrome Webdriver
driver.close()