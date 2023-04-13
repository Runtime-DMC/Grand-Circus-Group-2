from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import os

def init_driver():
    driver = webdriver.Chrome() # Use the appropriate driver for your browser
    driver.get("https://www.flexjobs.com/search?search=")
    return driver

def search_jobs(driver, job_title, start_date, end_date):
    search_box = driver.find_element(By.XPATH, "//input[@name='search']")
    search_box.clear()
    search_box.send_keys(job_title)
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "joblisting-title")))

    date_filter_xpath = "//select[@name='date_posted']/option"
    date_options = driver.find_elements(By.XPATH, date_filter_xpath)

    for option in date_options:
        option_value = option.get_attribute("value")
        if start_date <= option_value <= end_date:
            option.click()
            break

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "joblisting-title")))


def extract_job_details(job_listing):
    title = job_listing.find_element_by_css_selector("h5.joblisting-title").text.strip()
    location = job_listing.find_element_by_css_selector("span.joblisting-location").text.strip()
    link = job_listing.find_element_by_css_selector("a.joblisting-title").get_attribute("href")

    job_listing.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "job-details")))

    try:
        salary = driver.find_element_by_css_selector("span.joblisting-salary").text.strip()
    except:
        salary = "Not provided"

    skills = [skill.text.strip() for skill in driver.find_elements_by_css_selector("span.joblisting-skill")]

    return {
        'title': title,
        'location': location,
        'salary': salary,
        'skills': skills,
        'link': link
    }

def save_to_csv(job_details_list, output_file):
    headers = ['Title', 'Location', 'Salary', 'Skills', 'Link']

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for job in job_details_list:
            writer.writerow([
                job['title'],
                job['location'],
                job['salary'],
                ', '.join(job['skills']),
                job['link']
            ])

job_title = "Software Developer" # Change this to the desired job title
start_date = "2023-03-01"        # Change this to the desired start date
end_date = "2023-04-01"          # Change this to the desired end date
output_folder = "C:\\Users\\battl\\Documents\\GitHub\\Grand-Circus-Group-2"
output_file = os.path.join(output_folder, "job_listings.csv")

driver = init_driver()
search_jobs(driver, job_title, start_date, end_date)

job_listings = driver.find_elements_by_css_selector("div.joblisting-row")

job_details_list = []
for job_listing in job_listings:
    job_details = extract_job_details(job_listing)
    job_details_list.append(job_details)

save_to_csv(job_details_list, output_file)

driver.quit()