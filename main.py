from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import asyncio
from nltk import tokenize

from search_results import SearchResults


async def look_for_links(search_phrase):
    lista_linkova = ["https://www.google.com/search?q="+search_phrase+"&sxsrf=ALiCzsYL8JtmynQGBtmXe7TjyfuRMY_Wyg%3A1667407296962&source=hp&ei=wJ1iY5u0ONCkgAaulozQDQ&iflsig=AJiK0e8AAAAAY2Kr0GYSyjI6GwJxd7BmzkTtPhBaxJTU&ved=0ahUKEwiblISd-I_7AhVQEsAKHS4LA9oQ4dUDCAg&uact=5&oq=ketchup&gs_lp=Egdnd3Mtd2l6uAED-AEBMgQQLhhDMggQLhiABBjUAjIFEAAYgAQyCxAuGIAEGMcBGNEDMgUQABiABDIFEC4YgAQyBRAAGIAEMggQLhiABBjUAjIIEAAYgAQYyQMyBRAuGIAEwgIEECMYJ8ICBRAAGJECwgIEEAAYQ0jgDVAAWI8NcAB4AMgBAJABAJgBoAGgAbUGqgEDMC42&sclient=gws-wiz"]

    try:
        search_results = await look_at_links_from_list(10, lista_linkova, search_phrase)
    except Exception as e:
        print('Problem while parsing: ', e)
    print(lista_linkova)
    return search_results


async def look_at_links_from_list(number_of_links, list_of_links, search_phrase):

    sentences = []
    links_searched = 0
    links_found = 0

    for item in itertools.islice(list_of_links, number_of_links):
        req = Request(
            url=item,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read()
        bsobj = soup(webpage)

        print(item)

        # find all mentions of the reference
        regex = '[^.?!]*(?<=[.?\s!])'+search_phrase+'(?=[\s.?!])[^.?!]*[.?!]'
        for paragraph in bsobj.find_all('div'):
            print(paragraph.getText())
            for skubi in re.findall(regex, paragraph.getText()):
                print(skubi)
                sentences.append(skubi)

        # find all links in page
        for link in bsobj.findAll('a', attrs={'href': re.compile("^https://")}):
            if 'href' in link.attrs:
                list_of_links.append(link.attrs['href'])
                # track number of found links
                links_found = links_found+1

        # remove searched link
        list_of_links.remove(item)

        # track number of searched links
        links_searched = links_searched+1

    results = SearchResults(links_searched, links_found, sentences)
    return results


loop = asyncio.new_event_loop()


async def main():
    results = await look_for_links("eggs")
    print("I searched ", results.pages_searched,
          "links and found ", results.links_found, " pages")
    print('Sentences where its mentioned, ', results.sentences)


loop.run_until_complete(main())
