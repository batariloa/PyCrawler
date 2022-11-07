from search_results import SearchResults
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
from langdetect import detect
from webpageinfo import WebpageInfo


class Crawler():

    def look_at_links_from_list(self, number_of_links, links_to_be_searched, search_phrase):

        webpage_dict = dict()

        # iterate over links queued inside list of links and create bsobj
        for current_webpage_url in itertools.islice(links_to_be_searched, number_of_links):

            mentions = []
            links_on_webpage = []
            req = Request(
                url=current_webpage_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            webpage = urlopen(req).read()
            bsobj = soup(webpage, 'lxml')

            print(current_webpage_url)

            # find all mentions of the reference

            for pargagraph in bsobj.find_all(lambda tag: search_phrase in tag.text if tag.text else False, recursive=False):
                print(pargagraph.getText())
                mentions.append(pargagraph.getText())

            # find all links in page
            for link in bsobj.findAll('a', attrs={'href': re.compile("^https://")}):
                if 'href' in link.attrs:
                    url = link.attrs['href']

                    links_on_webpage.append(url)
                    links_to_be_searched.append(url)

            # remove searched link
            links_to_be_searched.remove(current_webpage_url)

            # if page mentions phrase at least once
            if (len(mentions) > 0):
                # add webpage info to dict of all webpages
                webpageinfo = WebpageInfo(
                    current_webpage_url, mentions, links_on_webpage)

                print(webpageinfo.mentions)
                webpage_dict[current_webpage_url] = webpageinfo

        results = SearchResults(webpage_dict)

        return results

    def look_for_links(self, search_phrase, depth_of_search):

        lista_linkova = [
            "https://en.wikipedia.org/w/index.php?go=Go&search="+search_phrase+"&title=Special:Search&profile=advanced&fulltext=1&ns0=1"]

        try:
            search_results = self.look_at_links_from_list(
                depth_of_search, lista_linkova, search_phrase)
        except Exception as e:
            print('Problem while parsing: ', e)
            search_results = None
        print(lista_linkova)
        return search_results
