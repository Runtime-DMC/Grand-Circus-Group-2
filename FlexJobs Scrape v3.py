import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find_all('div', class_='joblisting-row')

    job_data = []
    for item in content:
        title = item.find('a', class_='job-title').text.strip()

        salary = item.find('span', class_='salary-text')
        salary = salary.text.strip() if salary else 'Not found'

        job_type = item.find('span', class_='jobtype-text')
        job_type = job_type.text.strip() if job_type else 'Not found'

        location = item.find('span', class_='location-text')
        location = location.text.strip() if location else 'Not found'

        job = {
            'title': title,
            'salary': salary,
            'job_type': job_type,
            'location': location
        }
        job_data.append(job)

    return job_data

options = webdriver.ChromeOptions()
options.add_argument('--headless')

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
total_jobs = []

for x in range(1, 2):
    url = f'https://www.flexjobs.com/search?location=&search=data+science&page={x}'
    driver.get(url)
    
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'joblisting-row'))
        )
    except:
        print(f'Page {x} failed to load.')
        break

    total_jobs.extend(extract_data(driver))
    time.sleep(2)

driver.quit()

print('Total jobs found:', len(total_jobs))

df = pd.DataFrame(total_jobs)
print(df.head())
df.to_csv('C:/Users/battl/Documents/GitHub/Grand-Circus-Group-2/flexjobs.csv', index=False)

