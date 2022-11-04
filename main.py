from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import asyncio
from crawl import Crawler

from langdetect import detect

from search_results import SearchResults


loop = asyncio.new_event_loop()


async def main():
    crawler = Crawler()

    print('Crawler variables ', crawler.links_found)
    results = await crawler.look_for_links("Prdonja")
    print("I searched ", results.pages_searched,
          "links and found ", results.links_found, " pages")
    print('Sentences where its mentioned, ', results.sentences)


loop.run_until_complete(main())
