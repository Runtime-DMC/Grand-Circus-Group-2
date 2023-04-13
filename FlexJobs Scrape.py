import requests
from bs4 import BeautifulSoup
import csv
import os

def get_search_results(job_title, start_date, end_date):
    formatted_job_title = job_title.replace(' ', '+')
    url = f"https://www.flexjobs.com/search?search={formatted_job_title}&date_posted%5B%5D={start_date}&date_posted%5B%5D={end_date}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def extract_job_details(job_listing):
    title = job_listing.find('h5', class_='joblisting-title').text.strip()
    location = job_listing.find('span', class_='joblisting-location').text.strip()
    link = job_listing.find('a', class_='joblisting-title')['href']

    details_response = requests.get(link)
    details_soup = BeautifulSoup(details_response.text, "html.parser")

    try:
        salary = details_soup.find('span', class_='joblisting-salary').text.strip()
    except AttributeError:
        salary = "Not provided"

    skills = [skill.text.strip() for skill in details_soup.find_all('span', class_='joblisting-skill')]

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

soup = get_search_results(job_title, start_date, end_date)

job_listings = soup.find_all('div', class_='joblisting-row')

job_details_list = []
for job_listing in job_listings:
    job_details = extract_job_details(job_listing)
    job_details_list.append(job_details)

save_to_csv(job_details_list, output_file)
