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
        self.links_to_be_searched = []
        self.priority_links_to_be_searched = []
        self.reslt_dictionary = dict()

    def resume_search(self):
        self.result_handler.resume()
        try:
            search_results = self.look_at_links_from_list()
        except Exception as e:
            print('Problem while parsing: ', e)
            search_results = None

    def __init__(self,  search_phrase, depth_of_search, result_handler):
        self.links_to_be_searched = []
        self.priority_links_to_be_searched = []
        self.depth_of_search = depth_of_search
        self.search_phrase = search_phrase
        self.result_handler = result_handler
        self.reslt_dictionary = dict()

    def look_at_links_from_list(self,):

        # use chrome driver
        driver = createChromeDriver(headless=True)

        # iterate over links queued inside list of links and create bsobj
        for i in range(0, self.depth_of_search):

            # Stop search if stop flag is called
            if self.result_handler.stopFlag == True:
                empty_search_before_stop()
                break

            if self.result_handler.pauseFlag == True:
                break

            if (len(self.priority_links_to_be_searched) == 0 and len(self.links_to_be_searched) == 0):
                print
                ('No links left to crawl.')
                break

            # if there are no priority links, search in non-priority links
            if (len(self.priority_links_to_be_searched) == 0 and len(self.links_to_be_searched) > 0):
                print('no priority links')
                current_webpage_url = self.links_to_be_searched.pop()
            else:
                if (len(self.priority_links_to_be_searched) > 0):
                    current_webpage_url = self.priority_links_to_be_searched.pop()

            mentions = []
            links_on_webpage = []

            try:
                driver.get(current_webpage_url)
                bsobj = soup(driver.page_source)
            except Exception as e:
                print('Error encountered:', e)
                continue

            # find all mentions of the reference

            for pargagraph in bsobj.find_all(lambda tag: len(tag.find_all()) == 0 and self.search_phrase.lower() in tag.text.lower()):
                mentions.append(pargagraph.getText())

            # find all links in page
            for link in bsobj.find_all('a',  attrs={'href': re.compile("^https://")}):
                if 'href' in link.attrs:
                    url = link.attrs['href']
                    links_on_webpage.append(url)

                    # if it is a priority link
                    if (len(mentions) > 0):
                        self.priority_links_to_be_searched.append(url)
                    else:
                        # if this is not a priority link
                        self.links_to_be_searched.append(url)

            # if page mentions phrase at least once
            if (len(mentions) > 0):

                # add webpage info to dict of all webpages
                webpageinfo = WebpageInfo(
                    current_webpage_url, mentions, links_on_webpage)

                self.reslt_dictionary[current_webpage_url] = webpageinfo
                self.result_handler.append(self.reslt_dictionary)

    def beginSearch(self):

        self.links_to_be_searched.append(
            "https://www.google.com/search?q="+self.search_phrase.replace(' ', '+'))

        self.resume_search()
