from search_results import SearchResults
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
from langdetect import detect
from webpageinfo import WebpageInfo


class Crawler():

    def __init__(self):
        self.links_searched = 0

    async def look_at_links_from_list(self, number_of_links, links_to_be_searched, search_phrase):

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
            regex = re.compile(search_phrase + '[^.]*\.')
            all_text = bsobj.body
            for pargagraph in bsobj(text=regex):
                print(pargagraph)
                mentions.append(pargagraph)

            # find all links in page
            for link in bsobj.findAll('a', attrs={'href': re.compile("^https://")}):
                if 'href' in link.attrs:
                    url = link.attrs['href']

                    links_on_webpage.append(url)
                    links_to_be_searched.append(url)

            # remove searched link
            links_to_be_searched.remove(current_webpage_url)

            # add webpage info to dict of all webpages
            webpageinfo = WebpageInfo(
                current_webpage_url, mentions, links_on_webpage)

            print(webpageinfo.mentions)
            webpage_dict[current_webpage_url] = webpageinfo

        results = SearchResults(webpage_dict)

        return results

    async def look_for_links(self, search_phrase):

        lista_linkova = ["https://www.google.com/search?q="+search_phrase+"&sxsrf=ALiCzsYL8JtmynQGBtmXe7TjyfuRMY_Wyg%3A1667407296962&source=hp&ei=wJ1iY5u0ONCkgAaulozQDQ&iflsig=AJiK0e8AAAAAY2Kr0GYSyjI6GwJxd7BmzkTtPhBaxJTU&ved=0ahUKEwiblISd-I_7AhVQEsAKHS4LA9oQ4dUDCAg&uact=5&oq=ketchup&gs_lp=Egdnd3Mtd2l6uAED-AEBMgQQLhhDMggQLhiABBjUAjIFEAAYgAQyCxAuGIAEGMcBGNEDMgUQABiABDIFEC4YgAQyBRAAGIAEMggQLhiABBjUAjIIEAAYgAQYyQMyBRAuGIAEwgIEECMYJ8ICBRAAGJECwgIEEAAYQ0jgDVAAWI8NcAB4AMgBAJABAJgBoAGgAbUGqgEDMC42&sclient=gws-wiz"]

        try:
            search_results = await self.look_at_links_from_list(3, lista_linkova, search_phrase)
        except Exception as e:
            print('Problem while parsing: ', e)
            search_results = None
        print(lista_linkova)
        return search_results
