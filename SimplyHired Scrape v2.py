import requests
from bs4 import BeautifulSoup
import pandas as pd


job_titles = []
company_names = []
job_locations = []
job_descriptions = []
salaries = []

# Define the URL of the search results page
urls = ['https://www.simplyhired.com/search?q=data+engineer&l=United+States',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsAAQALAAAAAAAAAAAAAAACABC%2B6gEARCrcA3GiNAuIYjRhuxCsmzn%2F8zuv8FivUA6bl7J6N2tsGA%3D%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsAAgAWAAAAAAAAAAAAAAACABC%2B6gEBAQg%2BWbZkHeUWdvE3T5X2wdJrN0%2Fe4Rj4mIZQlBMVTGiLKvsIgaHlNcusz1x0XooM%2F9g66Lwm4%2Bo%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsAAwAhAAAAAAAAAAAAAAACABC%2B6gEBAQoQPpDoE%2Btp5zHJtt%2FpBx5u19hcT0rLJxhI%2Fw1rVRX7e%2Fbofang%2FZoVuz9aqfw36r8tIhZGyUX%2BlBPwybJyXNmP9cQEcuqnaUKEPBuy',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsABAAsAAAAAAAAAAAAAAACABC%2B6gEBAQpzPMTfWRqHyG5iyQXjiovphvTRyidieQBcvm7yonY68BpBrx1KeLTB4GyM%2BPjpcNKqVGW5zBvy8jmiLOBtoivkee7BIVPqwux%2Bje8nIo98Ou5NhDingBwQvdhkvZIep8g%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsABQA3AAAAAAAAAAAAAAACABC%2B6gECAQoWBw5iauwrhB5gr5%2BMX4enejwQPoyewGf2Rwa03hvcTNoaqnoU8C9iR1SS67fZsqi3o5E02SPFK%2F7WyKtpoXCCWdArHhjAj6YjxA52%2BIjmoK0j1W2YO1lYqnMnHeUoKrQ93pdjsIahX%2Fh5NT8PxO8%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsABgBCAAAAAAAAAAAAAAACABC%2B6gECAQoWBwnToRo0qyxWMS2%2FRPyLJgnBreS%2FUXl1LRARLZMxUldZoMDL1MHkIK6oF3d6%2FM6bDkCSpLeDTJZRZl95tjfH4mTdBFN6R5TneDX2%2BHZRtrWd5L0MuVvJKi8paCNy54u%2FhGBIgvh9G0v44F7fcRs3x0f9IjLOzFQWyy0%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsABwBNAAAAAAAAAAAAAAACABC%2B6gECAQoWBwUCd5qZBvs38U%2FSdDIStk14x3eUtHXfZnIo%2FbldOOdsxC2lsi9t%2BHxZ1Hf%2FLBrlRaP9cuKI1XurSuPo%2BCAKZBZYGl68CYLVEs0Kt3fcf2Dxgi7E9U8FcAvsNZK%2FW17faFIIzUeXsd9nbViVXCRPDZ%2BYlhouGLK%2F2mV3tHqjJn56vywLaw%3D%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsACABYAAAAAAAAAAAAAAACABC%2B6gEBARITzN1iI3K7MhZQN4vdT8Q0isNzmy1PrRJHyuvPXZo2bSGaMWd2KZdahJVFWUER9AYhODgDjQOKJVHUypdjIULC3Njf%2FnTwa%2FIJC54SwHf%2Bxs44jUWaG%2FuqTn5hKDvBykiDynOpTYoO62LvXcV3fW%2Faigym7Dw6wpgIy5fgPmi5WghxqoK%2BT8UZakE09KP3ljo%3D',
        'https://www.simplyhired.com/search?q=data+engineer&l=United+States&cursor=AAsACQBjAAAAAAAAAAAAAAACABC%2B6gECARdqCAP3s9uSSS0pJ3Wxok1mu7WZoy8EAEQSQnqJQfnMxlhDkpf4CI3Id2vNPmn%2FzCayH%2B8Cp7laMX%2B0uu9hrPSMPrYM%2FTIUIDCvJZAWKNw%2FrQsUQE1X9cMR27Z8cPyvKXiKl0prFKIa3dSuN3%2B8saTUXyQoxm%2Fpfki4%2F9OqVaRZ%2Bn5U8GB9tFaZdu2kB%2FOEFm%2Bsem4u773x5l8%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsAAQALAAAAAAAAAAAAAAACABPLJAEAJfikoMJg6IFiXmMytwFSy9jq%2FuRXZSps7r8LnOn8FbA%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsAAgAWAAAAAAAAAAAAAAACABPLJAEAB12S%2BorKyKmtJ6GF9I%2BbXCJ%2BZGRpAAvsq%2B9JTRzCkny11TMTTCsJOKrZfDkvCMNeZKbDfjw%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsAAwAhAAAAAAAAAAAAAAACABPLJAEBAQcUygXHm0YJyTZQZs7YYpCieXzRId%2BRCrUhU1PuhzmVgYdCktUo8DP4yMF42GzFppiOjsbArgipyMZnxgEsyeT%2BYe2577vRCQ%3D%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsABAAsAAAAAAAAAAAAAAACABPLJAEBAQduFDJ5KOM5ZZgJrXOixuIJPsNDgfByEl%2Bt5f%2BqI1xbKSAiSMVD%2Fdb%2FEh2o%2B4vgGCGGDtK1DIoTNiGcaokiPnkLFgL3vzWG64xKT39Mp3Rsrezo8L5LZC0gFIk%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsABQA3AAAAAAAAAAAAAAACABPLJAECAQ8sBgSsp2bxgyOoYdOoIkxK%2FE4A9KuHixr63Tj7%2FO%2BzLTCA0FAAdIVe7KTbwz5D%2FbCvBDlcr7vC4sadM4ZR7vO5xTKOnP6FG1wFGJAQb4XEmj4J8a6cpG%2Fko2XW%2FmxpUxXovXMu7qxO9GlzhQ%3D%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsABgBCAAAAAAAAAAAAAAACABPLJAECAQ8sDAMxYHjvrI8CXuYrEBiRlDW0uC%2FXdhYCqiBhbDb0A5gfKvO5Y62upXStL4idOpuEY59gauobM2Ejf%2F3EZwsQJ8sj5jTLekPq0YAQSlQmIqcprZ8PrYBBO1pIQWjtI8t%2FpRz2HLGlSbN66kj6sut7DyNqElUX1Q%3D%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsABwBNAAAAAAAAAAAAAAACABPLJAECAQ8oDk%2FB4SjU226ItCQAcUK5EYoGY6u4LoSolXl9ZNjl3ZUarqPb8E1TfnPZfro7ZyCriuOEx40R7GcXpNxsEMawRf2lATdWxXNoCApolj3mZmD1%2Fnttd24CAms6qMslAZOQAqgBUCBax09WZrEJIT4qZ8Y4psUVPig3OndmXfXkQexV',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsACABYAAAAAAAAAAAAAAACABPLJAECARMoDArRyrcpvOUKG7J4qnk3zPRvOmikYUbXBn90cnp4FXLJx6Einyvnvu3MJO0frJ4Pma8YL68GYXofpRJQF2JChxWO3oYrjf0ukd1mt7rUG%2BeFH4i4LLCSk%2FKDt6TedCqSDtDpL6grrjaZaQK6DE4lOHN08MQfXCnVbQk3yLopW5FA%2FsWWSx2SCHc4aqBp0mU%3D',
        'https://www.simplyhired.com/search?q=data+analyst&l=United+States&cursor=AAsACQBjAAAAAAAAAAAAAAACABPLJAECARMoDAdj6XLcB9FUy7CKqrEdzFK%2FFqMZqpGh5bYTZD5Pef%2FgyaGi8LqmnigfJU3Uheoc%2BscBvsXeJpeAbbozs5o4cQ5UqDzzechAxyMamjxaAuTnVHiEMDDbcuLBqR61ZAjNrgeJ1EjkcLUNJD5mvb6LenBtbiXCnmSV9D3jOP4VpdQJEa2dB6iJ9H%2Fw0D2zgozkiaKV13Xl3u9h%2FE8%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsAAQALAAAAAAAAAAAAAAACABL5hAEAAa4UYU3OVwKyEDdWz1hdew%2B35Gryq1YnJgaDRA%3D%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsAAgAWAAAAAAAAAAAAAAACABL5hAEBAQsHDJRfFbKxma%2BIvAsZ%2B49GbJiIR2EL%2BE%2FjuhBTpuOHKpfjlbwWZ2PDYkrQm1ba9RSb5bhgBJU%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsAAwAhAAAAAAAAAAAAAAACABL5hAECAQsYBgrSAgz5dtWCt%2BM9NPtfDiSldtpP6e3IKfBwJm%2FNTSVkG5YYeBEyZJd9aOrhT0MYcEjnHW3xCzAgK%2FV1KLmvWPG%2FoZkeWw%3D%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsABAAsAAAAAAAAAAAAAAACABL5hAEBARIrBHixl5xe21w1Sq4VFeqaTI%2Ben7jBtke2XUofkjL3qa0DnetpN%2BkcjYt9U6PKVYBsfsVF%2BtVJtIVtco9cquG6YWTJwi7h4t3nN1xJoBrzDZv1fzPm6WA%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsABQA3AAAAAAAAAAAAAAACABL5hAEBARMAsWBENZAgj05%2Fg6wPS5fAwXAs1Vy7oIHKrYhjiLtHycX7nq40ddv82UCaHhWGLb60PcVBj%2FuHGTvK6N9NAIHfWE0NUNbzp1AUEdKIlD0MDyZMFjkYwFeCF31Gm%2FIlY3%2BV8zU7OBuN2JfV',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsABgBCAAAAAAAAAAAAAAACABL5hAECARMqCHgqdkx5MSJHzumXaAvuSzOXgJICG1o8ok9yylVJngEOwmrJi6RwRcGIS0W9AEEd9I%2FjBKV6Mz7j3GNPr9ZuMEMkszvTK5%2Fu8kcDxXENLnKnauZlVtYMh2eY51h7HcV5q%2Fb8ub05k9hUq77POykCkr4QD5npiQ%3D%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsABwBNAAAAAAAAAAAAAAACABL5hAECARMqCAVl%2Fly%2FFe0WYJMFslr32ujKoWfIjNf5OLTHLaipXBnhICvb8W9WXAOzRRSp3%2BLS3por1aJfpCq%2FqOsI5PjgC35nmFqm%2BPVRekDQMVwgGrKvpOd1kRWEG3o8An7UrpQ5VbNVYCtirGelvIldbKiwKKo2ErGurkyY0tBnWpOEvxERoqJ%2FVqE%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsACABYAAAAAAAAAAAAAAACABL5hAECARMqDBNDqM33ei2wu6F33rqoDFP5cXCu5iWKowDywtWLo8FFqOgZ4BoMxcqcpYu%2B%2F%2Flqmp2SeN9MwP%2FfYLR3GINww7biXKhLGb8wI4FmILtOmD1IN5rxfOOwGdLm1Gu7JGcH5my1Pc2EUpOA93EmQ6FGsq1aCmyJUZ%2BHR0goP32SnCuadsksvw0I5Wz91PxRZqJwjQ%3D%3D',
        'https://www.simplyhired.com/search?q=data+architect&l=United+States&cursor=AAsACQBjAAAAAAAAAAAAAAACABL5hAEDARMqD4QBBxyMWdtgqaBx0Kfh4JoTG35jvBhLklcENpSNQyeYk%2BhjU6M1v9Je5hl%2Bb8TS6k0ydTBlLdEXIHL615llkNFmHN6e16SzZ5GhnJWgXdDe16A%2BVEUPkwFGMXXAtkQegGEsWwUllSDEBNAzwAE6a3cVloeaQw124DuDH%2B%2Fkfv5Bnx0wrRvn6g7RrMjRpp36eCNiAiL58FlFMCux',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsAAQALAAAAAAAAAAAAAAACABBTnQEAB0Me9IAbrRHqIaAgEp8MUoDfOfaLqrcbLlLmcyMHpORO',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsAAgAWAAAAAAAAAAAAAAACABBTnQEBAQcbdIpSlHQJ%2BreOTnXsXpmd235EVraRkio2CnWqV%2FhP74xOXUnKoKXobtsTqYiQ%2F1iDCT1L',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsAAwAhAAAAAAAAAAAAAAACABBTnQECAQcgBgTPNLFbVmqEH5nZQ%2BS4RXZxjhphFJzt8YYpJmQIsioPD6WTVflPbA49loKjyig3cNEVbuB9Y0skTLa2ydvqV%2F4GrQ%3D%3D',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsABAAsAAAAAAAAAAAAAAACABBTnQEBAQcAsnRxTxhNQRyOjpzIoZLwXOjW2ERvS8UB14Z9sELDQ2IWHJZFZp5tyforoXTdYXRqx1lBWdbICgo6kw%2BfCisj%2FVEL5V%2BhngRxSounE%2FuEwq%2BwYCDRWQ%3D%3D',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsABQA3AAAAAAAAAAAAAAACABBTnQEBAQ9Cm5T4IU3cz%2F5Xfr8scNOJw5z97Prm6neCw%2BnRRGRZEtWQnskQ%2BequJ7Es08ywAdsn1oiBJ5sSFVhS2%2BcfahW8cpqp6%2FccUiJ%2BaNmPcKHpNq6zAyr5XF53bqzGuMEkCw%3D%3D',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsABgBCAAAAAAAAAAAAAAACABBTnQECAQ8iBwivH23%2BqCkOAfVU6pUnRoFLihHWa1N%2FXCqyB722YJt5XWpHRPmTBfsCmlH1ywctKLDRiitUDI1Ejharu0WT%2FcndtQvmav3wY%2BFaxYLG26VBLBvxRuYfh3Gdk8wZoXyHbIAVIkh%2FvWsRLQEgbA%3D%3D',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsABwBNAAAAAAAAAAAAAAACABBTnQECAQ8gCAOrN9RjruxSOvWoHZC%2FmIGsmuCGa9rJJ%2FxSRsyRXiviN8XN4xG3OAiFK7HFzQe5Pgr9kuhTkyrNQW3TieiHSfm%2FisbP3LyL2a0QHams%2BtMpEWwWBuyHGpacicOS1BbR4%2FtkxQYNZUQS7ul9k057tKUPTpVXJXZb6GOLW38v',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsACABYAAAAAAAAAAAAAAACABBTnQEBARgeVpv%2FkADjAQpiJoJRk1%2BL4mHVHBzmAQrfW%2Faq16qN2e%2FbQmzaRx1C642DOeVK0fCiCNRiykyhkPu39NnG6GHAk%2BJn9x1VXDNU%2BgmzYqGI%2Fo%2BXD221ZdF7Phu3%2B0Cr9QjIE49yWZejgqaJA18DgeKsYWbOEYF7CJzHEyWJ8ELinzWAdvAySE6g4RQ%3D',
        'https://www.simplyhired.com/search?q=data+scientist&l=United+States&cursor=AAsACQBjAAAAAAAAAAAAAAACABBTnQEBARgDlPsgQOzc%2FlzBaBPAv6ta66FC3%2FXBv4g8sEv9rCvMfmAyNSkPJOmh4F8n4PwLjSRDo0BSqYWJ8TaqdIuyJ07n2WoDgvLMCO5Nmvf1SApi%2F8%2FbNfBd7nyWRZkCIN7M68IH3jABkdA3dLcbPRx7DbKvjBBUvi8uxn4%2FpEA%2Bd2OsayCMfpl6uvOrMXJbE%2Fe9m4A%3D']


for count, url in enumerate(urls):
  # Send a request to the website and get the response
  url = urls[count]

  # Send a GET request to the URL and store the response in a variable
  response = requests.get(url)

  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, 'html.parser')
  
  # Find all the job postings on the page
  job_postings = soup.find_all('li', {'class': 'css-0'})
  #print(job_postings)
  
  # Loop through the job postings and extract the relevant information
  for job_posting in job_postings:
    job_title = job_posting.find('a', {'class': 'chakra-button css-12bkbc3'}).text.strip()
    company_name = job_posting.find('span', {'class': 'css-lvyu5j'}).text.strip()
    job_description = job_posting.find('p', {'class': 'chakra-text css-jhqp7z'}).text.strip()
    job_location = job_posting.find('span', {'class': 'css-1t92pv'}).text.strip()
    try:
      salary = job_posting.find('p', {'class': 'chakra-text css-1ejkpji'}, {'data-testid': 'searchSerpJobSalaryEst'}).text.strip()
      #print(salary)
    except AttributeError:
      salary=None
    
    job_titles.append(job_title)
    company_names.append(company_name)
    job_descriptions.append(job_description)
    job_locations.append(job_location)
    salaries.append(salary)
    
    # Print the information for each job posting
    #print(job_title)
    #print(company_name)
    #print(job_location)
    #print(job_description)
    #print('\n')

df = pd.DataFrame(
{'job_title': job_titles,
  'company_name': company_names,
  'job_description': job_descriptions,
  'job_location': job_locations,
  'salary': salaries
})

df.to_csv('simplyhiredjobs.csv', index=True)
print('Done!')