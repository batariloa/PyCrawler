from search_results import SearchResults
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
from langdetect import detect
from webpageinfo import WebpageInfo
import requests
from urllib.parse import urljoin


import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Crawler():

    def look_at_links_from_list(self, number_of_links, links_to_be_searched, search_phrase, event_list):

        options = webdriver.ChromeOptions()

        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        webpage_dict = dict()
        priority_links_to_be_searched = []

        # iterate over links queued inside list of links and create bsobj
        for i in range(0, number_of_links):

            # if there are no priority links, search in non-priority links
            if (len(priority_links_to_be_searched) == 0 and len(links_to_be_searched) > 0):
                print('no priority links')
                current_webpage_url = links_to_be_searched.pop()
            else:
                if (len(priority_links_to_be_searched) > 0):
                    current_webpage_url = priority_links_to_be_searched.pop()

            mentions = []
            links_on_webpage = []

            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}

            driver.get(current_webpage_url)
            bsobj = soup(driver.page_source)

            # find all mentions of the reference

            for pargagraph in bsobj.find_all(lambda tag: len(tag.find_all()) == 0 and search_phrase.lower() in tag.text.lower()):
                mentions.append(pargagraph.getText())

            # find all links in page
            for link in bsobj.find_all('a',  attrs={'href': re.compile("^https://")}):
                if 'href' in link.attrs:
                    url = link.attrs['href']
                    links_on_webpage.append(url)

                    # if it is a priority link
                    if (len(mentions) > 0):
                        priority_links_to_be_searched.append(url)
                    else:
                        # if this is not a priority link
                        links_to_be_searched.append(url)

            # if page mentions phrase at least once
            if (len(mentions) > 0):

                # add webpage info to dict of all webpages
                webpageinfo = WebpageInfo(
                    current_webpage_url, mentions, links_on_webpage)

                webpage_dict[current_webpage_url] = webpageinfo
                event_list.append(webpage_dict)

            print('Priority list: ', priority_links_to_be_searched)
        results = SearchResults(webpage_dict)

        return results

    def look_for_links(self, search_phrase, depth_of_search, queue_of_results):

        lista_linkova = [
            "https://www.google.com/search?q="+search_phrase.replace(' ', '+')+"&oq=gors&aqs=chrome.0.35i39j46i175i199i512j69i57j46i67j0i67j46i512j46i175i199i512j69i61.1204j0j7&sourceid=chrome&ie=UTF-8"]

        try:
            search_results = self.look_at_links_from_list(
                depth_of_search, lista_linkova, search_phrase, queue_of_results)
        except Exception as e:
            print('Problem while parsing: ', e)
            search_results = None
        print(lista_linkova)
        return search_results
