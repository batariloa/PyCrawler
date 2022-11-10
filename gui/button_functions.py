from my_enum.gui_variables import WindowVariables as wv
from util.driver_util import createChromeDriver

import time


def runSearchClicked(crawler, window):

    window[wv.text_status].update('Crawling..')
    results = crawler.beginSearch()
    window[wv.text_status].update('Done.')


def resumeClicked(crawler, window):
    window[wv.text_status].update('Crawling..')
    crawler.resume_search()
    window[wv.text_status].update('Done.')


def openLinkInBrowser(link):

    if (link):
        driver = createChromeDriver(headless=False)

    driver.get(link)


def updatePageInfo(window, selected_webpageinfo):

    window[wv.list_of_page_mentions].update(
        selected_webpageinfo.mentions)

    window[wv.list_of_page_links].update(
        selected_webpageinfo.links_found)

    window[wv.text_current_url].update(
        selected_webpageinfo.webpage)

    window[wv.number_of_links_found].update(
        len(selected_webpageinfo.links_found))

    window[wv.number_of_mentions_found].update(
        len(selected_webpageinfo.mentions))

    print(selected_webpageinfo.links_found)
