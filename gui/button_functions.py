from my_enum.gui_variables import WindowVariables as wv
from util.driver_util import createChromeDriver

import time


def runSearchClicked(crawler, window):

    window[wv.start].update(disabled=True)
    window[wv.stop].update(disabled=False)
    window[wv.pause].update(disabled=False)
    setStatusToCrawling(window)

    results = crawler.beginSearch()
    setStatusToDone(window)
    window[wv.start].update(disabled=False)
    window[wv.stop].update(disabled=True)
    window[wv.pause].update(disabled=True)


def resumeClicked(crawler, window):
    setStatusToCrawling(window)
    window[wv.start].update(disabled=True)
    window[wv.pause].update(disabled=False)
    window[wv.stop].update(disabled=False)
    window[wv.resume].update(disabled=True)
    crawler.resume_search()
    setStatusToDone(window)
    window[wv.start].update(disabled=False)
    window[wv.stop].update(disabled=True)
    window[wv.pause].update(disabled=True)


def stopClicked(result_handler, window):
    result_handler.stop()
    window[wv.stop].update(disabled=True)
    window[wv.start].update(disabled=False)
    window[wv.resume].update(disabled=True)
    window[wv.pause].update(disabled=True)
    setStatusToDone(window)


def pauseClicked(result_handler, window):
    result_handler.pause()
    window[wv.resume].update(disabled=False)
    window[wv.pause].update(disabled=True)
    window[wv.stop].update(disabled=False)


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


def setStatusToCrawling(window):
    window[wv.text_status].update('Crawling..')


def setStatusToDone(window):
    window[wv.text_status].update('Done.')
