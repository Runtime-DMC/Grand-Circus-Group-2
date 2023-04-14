import requests
from bs4 import BeautifulSoup
import pandas as pd


job_titles = []
company_names = []
job_locations = []
job_descriptions = []
salaries = []

# Define the URL of the search results page
urls = [
    'https://www.simplyhired.com/search?q=data+engineer&l=',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsAAQALAAAAAAAAAAAAAAAB%2F81HwAEBAQYA%2FaeOErlvA31Jzpa%2BglbxLcmo1KEzrUhHJMe160YWCh0c',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsAAgAWAAAAAAAAAAAAAAAB%2F81HwAECAQYOBgPR07QMtFXrL1KXFGuj%2Bhs%2BQJbfgM91s%2FiAfQTVs4EBD%2BRnaeGD%2F%2FFdroqi3MkxEroMa04%3D',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsAAwAhAAAAAAAAAAAAAAAB%2F9F1gQEBAQ0JC6z1mZg2LQu61e5l3YC9O5RPTh5KaKBjPRLYySelcAZYkPz3ZqTM%2BRLFRRIRBTP%2BNZTUyayhMZjcGoEpmHs30O%2FMoG7SO3W6uw%3D%3D',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsABAAsAAAAAAAAAAAAAAAB%2F9MbRwECAQscCAZ7aKf%2BIZ16M%2BrDhAPUeVAAk5VoO5m%2BUQ3F5%2BORsjgA5IF9FMW3F1ePMVqeVN58EEMghHpvt%2Bx9Ed9hUUtGKFzTeiotLZLa4f0weIPI2h01Gf6d1K%2B3uw%3D%3D'
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsABQA3AAAAAAAAAAAAAAAB%2F9MbRwEBARF5u2OUqRcYO0%2B9cXBzKqnf9mt3uvBKRUSNSJNDwX17dSq6p3iuWt8ll63JU4s5qZC3ne5zYoiQr6a%2BbZuRhppjMuC2MSjTa4JSAe0U9URWplIktFBbyJ9YTbc7n6ZuKvsJ8puOnF0B',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsABgBCAAAAAAAAAAAAAAAB%2F9MbRwECAREwCwJGm0sF9QPj%2BWzqLBxXDkp68UnlE00ff%2FRau399KjQ2wCbAZPm8GvAFTOikToT9mddULhEVlVg5jbjbQedGQwdhcNHt%2BC1028YZm7Y7xwapxmSBmY%2BeWXbY5MyPKezxCN%2FgdWN%2B9R3bA%2F9tYuqK3hkQJE8%2B',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsABwBNAAAAAAAAAAAAAAAB%2F9MbRwECAREwCwj%2BQjfFh06uZp1L3XiFdjALfpLy740easB%2BQ5oc0qu1LcwfKC6pfj4cxaSTQzy0OXc0CJxDtSzQBZFdLfF5R7uiSnx5BRa9G1JRCHV17qjSmNWGtGBVUii4%2FdP%2FpWmI7dLVGzSwpko8l6ZPMM%2BL9zDbQWaQllNXTSoFfNNL0Zt2gFra%2BdFe',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsACABYAAAAAAAAAAAAAAAB%2F9MbRwECARIwDACKnfSC6%2FOTQDcTwWdYnqIm5I%2Bttm6C4EbpNsmaPs34RJTvmR5%2Fz1t96JXXppAqKfLm8MKu61ZnUhMUSI7T51E0vGp41OR5HCbWIfW5HRgkQEC90y4D6LUhiEbhgFO9wBsVVO0IxHRCPOIfEbY0Sag%2FS7xJjYU8PTbknQJI7hdtJNE9yz%2Fwa%2F5RasS%2FQC%2BJEAA%3D',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsACQBjAAAAAAAAAAAAAAAB%2F9MbRwEDARIwDEoGBZ%2BgVRZ6SHQWyHrFraJg6TR23rX3HIkBjaZ%2FvfalgU9EObBeRGYup%2ByolZ6uCNt2ob8FbXp%2FvqBYaF7L5X1cmZKm1lJaAORaIQ8j24UsO2ZLxhvmmnTo85TfTjStuMl8J%2Fv184AiRRBi2UYRsqlEPx%2BRdppr%2FDzyeuew6k2t4mmnKPCPrZp%2F6G%2FeJJLvHjDloB36AB%2B7Apns',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsACgBuAAAAAAAAAAAAAAAB%2F9MbRwEDARIwDEoHBuVF3cQBiceBUacTZj81CJSz4d5qxqaT4m6FWovoP2smT6ASr2NY0TCY5xHO%2FnSIECcSCMxYzOhPvEFTnVxdWCHrIeJMtTx75lEQUzHrwDczJKqfoWLYbVjt2hCBBBZgB%2BLiFDeVPcFOW7i%2Bu8dy2GQST1k6fLtQpIMKSAc20FxvtJSRrdrWDzYh6ZeiUOjBNzrCzehdSjSutoXjkwU6f9B%2BN3vooOM%3D',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsACwB5AAAAAAAAAAAAAAAB%2F9OPLwEDARIwDEoHA4PvifTEiES0IXk0%2FLQG329mkEYQ9hueptfR6LG2xNPo%2F%2Fc6jR8R9IkIR%2F79w7mZ%2F%2B7d4LE5up4KXOzzvDMCx%2FuQHcQWQspgc3IH5uUIQUYSUA08%2BY1%2B3c7O7WRk%2Fbd%2Fm5cXbi5i4ED9Kt9Y6hR35w9YQq0DaPnOo1EmcGxoTweI0UGnXQUtlh8YvvU67J%2BlPvqX9fDpLkjeqL2gutvmOdmFyfGX5BrhTR70qxVVb4EUhw%3D%3D',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsADACEAAAAAAAAAAAAAAAB%2F9MbRwEDARIwDEoHDy3Q8d7ChLOWRAx1%2FSxX%2F3KqVf4s6WVXC8g5y64yuMkFXoNusPb%2BNs6kfW8B8GmQL%2BSkI6mCmx%2FnykiftDKqeY5HAcCaXVSTS5%2FSciWcrsWW595k3Qzf1WlbLsXFjY7J5pqwC2A%2F%2B5zFiH%2BFV1lhKFGoE7ieTsAOz%2FdojKEsXl4sATLjXw9CYb5n2SqfaiQcfJHVHTrGluc%2FQRRLS6BTN%2BpGkcL9RofUI3iU0bcGPXc31MAnXwUz',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsADQCPAAAAAAAAAAAAAAAB%2F9MbRwEEARIwDBoKJA0G%2FPW%2FCvpWrAhBfFNCH9l46JyoeidthTJIKJiT6DtJcDA5ekzMpbzYxP18902tfHI1K2B%2BONrvpGQXvYTDGFXsfQl5IrATGSZNEdeqwXBucxkWZGgyw58yUV7lCmwh%2BEai9tLoJSO6eyRa%2BzpVLYgnrdMJBHq8Z0OI9CMKE7xnZwEx9jx1K3AAli2Y2htnNNgt%2FVAiS6S9lM9GCnhpBvoNEOfv%2BPR%2BpTtnEUib%2BQl9GcD3L7vzmiYuhFnd',
    'https://www.simplyhired.com/search?q=data+engineer&l=&cursor=AAsADgCaAAAAAAAAAAAAAAAB%2F9OPLwEFARYwDBwKJA1kBwVdOI3EjkcrqZyng1hyZQOfgesrsFu2qQmQrwF8Rjp%2F9yYzkW0G%2BLRCqFbk8rU7N91IMX7rPBLmTGYlxDYY5RQPYxJE2Nk3pNHK7gGJFInqJNdT3HHfan1ROKqo5OurnLxgoi1foM8Xxm3fM%2FpRT7zyEZa9qAB4vkPO5z38c87%2FwLsg2RkkjUVbmUOUQOO2qcuUSZVyg9TPr9NazCujFDpmshkZdW6wAw5nZhQlsmOqFAYAMuNBhc1bYnaHHKeNwA%3D%3D'
#page 15
]




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

# df.head(200)
#208 rows of data at 15 pages

df.to_csv('simplyhiredjobs.csv', index=False)