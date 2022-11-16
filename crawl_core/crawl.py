from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
from langdetect import detect
from model.webpageinfo import WebpageInfo
import requests
from urllib.parse import urljoin


from util.driver_util import createChromeDriver


class Crawler():

    def empty_search_before_stop(self):
        self.link_non_priority_queue = []
        self.link_priority_queue = []
        self.result_dictionary = dict()

    def resume_search(self):
        self.result_handler.resume()
        try:
            search_results = self.look_at_links_from_list()
        except Exception as e:
            print('Problem while parsing: ', e)
            search_results = None

    def __init__(self,  search_phrase, depth_of_search, result_handler):
        self.link_non_priority_queue = []
        self.link_priority_queue = []
        self.depth_of_search = depth_of_search
        self.search_phrase = search_phrase
        self.result_handler = result_handler
        self.result_dictionary = dict()

    def look_at_links_from_list(self,):

        # use chrome driver
        driver = createChromeDriver(headless=True)

        # iterate over links queued inside list of links and create bsobj
        for i in range(0, self.depth_of_search):

            # Initiate fresh list of mentions and links on the current webpage
            mentions = []
            links_on_webpage = []

            # Stop search if stop flag is activated
            if self.result_handler.stopFlag == True:
                self.empty_search_before_stop()
                break

            # Pause search if pause flag is activated
            if self.result_handler.pauseFlag == True:
                break

            # Check if both non-priority and priority lists are empty
            if (len(self.link_priority_queue) == 0 and len(self.link_non_priority_queue) == 0):
                print
                ('No links left to crawl.')
                break

            # if there are no priority links, search in non-priority links

            if (len(self.link_priority_queue) > 0):
                current_webpage_url = self.link_priority_queue.pop(
                    0)
            elif (len(self.link_priority_queue) == 0 and len(self.link_non_priority_queue) > 0):
                print('no priority links')
                current_webpage_url = self.link_non_priority_queue.pop(0)

            # Open current webpage in webdriver
            try:
                driver.get(current_webpage_url)
                bsobj = soup(driver.page_source, 'html.parser')
            except Exception as e:
                print('Error encountered:', e)
                continue

            # find all mentions of the reference on the current webpage
            for pargagraph in bsobj.find_all(lambda tag: len(tag.find_all()) == 0 and self.search_phrase.lower() in tag.text.lower()):
                mentions.append(pargagraph.getText())

            # find all links in page
            for link in bsobj.find_all('a',  attrs={'href': re.compile("^https://")}):
                if 'href' in link.attrs:
                    url = link.attrs['href']
                    links_on_webpage.append(url)

                    # if the searched phrase is found on the current page at least once, add all found links to the priority queue
                    if (len(mentions) > 0):
                        self.link_priority_queue.append(url)
                    else:
                        # if no mentions are found, add the link to the non-priority queue
                        self.link_non_priority_queue.append(url)

            # if page mentions phrase at least once
            if (len(mentions) > 0):

                # add webpage info to dict of all webpages
                webpageinfo = WebpageInfo(
                    current_webpage_url, mentions, links_on_webpage)

                # add the current webpage info to the result dictionary
                self.result_dictionary[current_webpage_url] = webpageinfo
                # tell the result handler to append the new results to the GUI
                self.result_handler.append(self.result_dictionary)

    def beginSearch(self):

        self.link_non_priority_queue.append(
            "https://www.google.com/search?q="+self.search_phrase.replace(' ', '+'))

        self.resume_search()
