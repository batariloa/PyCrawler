from search_results import SearchResults
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools


class Crawler():

    def __init__(self):
        self.links_searched = 0
        self.links_found = 0
        self.sentences = []

    async def look_at_links_from_list(self, number_of_links, list_of_links, search_phrase):

        # iterate over links queued inside list of links and create bsobj
        for item in itertools.islice(list_of_links, number_of_links):
            req = Request(
                url=item,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            webpage = urlopen(req).read()
            bsobj = soup(webpage, 'lxml')

            print(item)

            # find all mentions of the reference
            regex = re.compile(search_phrase + '[^.]*\.')
            all_text = bsobj.body
            for pargagraph in bsobj(text=regex):
                print(pargagraph)
                self.sentences.append(pargagraph)

            # find all links in page
            for link in bsobj.findAll('a', attrs={'href': re.compile("^https://")}):
                if 'href' in link.attrs:
                    url = link.attrs['href']

                    list_of_links.append(url)

                    # track number of found links
                    self.links_found = self.links_found+1

            # remove searched link
            list_of_links.remove(item)

            # track number of searched links
            self.links_searched = self.links_searched+1

        self.sentences = list(dict.fromkeys(self.sentences))
        results = SearchResults(links_searched, links_found, self.sentences)
        return results

    async def look_for_links(self, search_phrase):
        lista_linkova = ["https://www.google.com/search?q="+search_phrase+"&sxsrf=ALiCzsYL8JtmynQGBtmXe7TjyfuRMY_Wyg%3A1667407296962&source=hp&ei=wJ1iY5u0ONCkgAaulozQDQ&iflsig=AJiK0e8AAAAAY2Kr0GYSyjI6GwJxd7BmzkTtPhBaxJTU&ved=0ahUKEwiblISd-I_7AhVQEsAKHS4LA9oQ4dUDCAg&uact=5&oq=ketchup&gs_lp=Egdnd3Mtd2l6uAED-AEBMgQQLhhDMggQLhiABBjUAjIFEAAYgAQyCxAuGIAEGMcBGNEDMgUQABiABDIFEC4YgAQyBRAAGIAEMggQLhiABBjUAjIIEAAYgAQYyQMyBRAuGIAEwgIEECMYJ8ICBRAAGJECwgIEEAAYQ0jgDVAAWI8NcAB4AMgBAJABAJgBoAGgAbUGqgEDMC42&sclient=gws-wiz"]

        try:
            search_results = await self.look_at_links_from_list(10, lista_linkova, search_phrase)
        except Exception as e:
            print('Problem while parsing: ', e)
        print(lista_linkova)
        return search_results
