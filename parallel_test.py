from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, wait

mesh_results = {}  # list for holding mesh suggestions

# ask user for keywords and parse into list
query = input("What keywords would you like to search for?\n")
keyword_list = query.split(" ")

# browser setup


mesh_url = 'https://meshb.nlm.nih.gov/MeSHonDemand'


def visit_site(keyword):
    def init_browser():
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        return Browser('chrome', **executable_path, headless=False)

    browser = init_browser()
    browser.quit()
    return keyword


futures = []
with ThreadPoolExecutor() as executor:
    for i in range(0, len(keyword_list)):
        futures.append(
            executor.submit(visit_site, keyword_list[i])
        )

wait(futures)

for future in futures:
    print(future)
