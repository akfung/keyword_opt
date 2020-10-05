'''
Web scraper for MeSH on demand page to extract MeSH terms from given terms
'''

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import time, sleep

mesh_results = {}  # list for holding mesh suggestions

# ask user for keywords and parse into list
query = input("What keywords would you like to search for?\n")
keyword_list = query.split(",")

# browser setup


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)


mesh_url = 'https://meshb.nlm.nih.gov/MeSHonDemand'

browser = init_browser()


browser.visit(mesh_url)  # visit mesh on demand url

# loop through keywords
for keyword in keyword_list:
    keyword_list = []  # list to hold results for given keyword
    # find text field and fill in terms
    browser.find_by_id('MODEntry').fill(keyword)
    browser.click_link_by_id('runMOD')  # click search button

    # wait for results to load
    element_indicator = '.col-xs-3 .ng-scope'
    is_not_present = browser.is_element_not_present_by_css(
        element_indicator)

    print(f'Searching for: {keyword}')
    start_time = time()  # record start time
    while is_not_present:
        sleep(1)  # wait 1 sec before checking for results again
        is_not_present = browser.is_element_not_present_by_css(
            element_indicator)
        # break the loop if loading takes longer than 15 seconds to load
        if time() - start_time > 15:
            break
    stop_time = time()  # record end time
    # indicate results loaded with processing time
    print(
        f'Finished searching for {keyword}\nTime elapsed: {stop_time - start_time} seconds')

    splinter_results = browser.find_by_css("div .col-xs-3")
    soup = bs(splinter_results.html, "html.parser")
    results = soup.find_all('a')

    # loop to add all results to the keyword_list
    for result in results:
        keyword_list.append(result.text)

    mesh_results[keyword] = keyword_list

    browser.reload()  # refresh browser before starting search for next keyword

print(mesh_results)

browser.quit()  # close browser
