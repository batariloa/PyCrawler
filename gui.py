import PySimpleGUI as sg

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import threading

from crawl import Crawler

import tkinter
from search_results import SearchResults


layout_websites = [sg.Listbox(values=[], enable_events=True,
                              size=(50, 30),  key='-WEBSITE LIST-')]


layout_pageinfo_mentions = [
    [sg.Listbox(values=[], enable_events=True,
                size=(50, 20), key="-PAGEINFO MENTIONS-")],
    [sg.Multiline(size=(50, 10), key='textbox')]]

layout_pageinfo_links = [
    [sg.Listbox(values=[], enable_events=True,
                size=(50, 30), key="-PAGEINFO LINKS-")]]

first_column_tab_group = [
    [sg.Column([[sg.Text("Search phrase:")], [
               sg.Input(key='_SEARCH PHRASE_', size=(35, 5))]]),
     sg.Column([[sg.Text("Depth of search:")], [
                sg.Input(key='_DEPTH OF SEARCH_', size=(15, 5))]])],

    [sg.Button("OK")],
    layout_websites,
    [sg.Button("OPEN")]
]


layout_pageinfo = [[sg.Text("Page URL: ")],
                   [sg.HSeparator()],
                   [sg.Text("Number of links found: ")],
                   [sg.TabGroup([
                       [sg.Tab('Mentions', layout_pageinfo_mentions,
                               tooltip='Details', key='-PAGEINFO MENTIONS-')],
                       [sg.Tab('Links found', layout_pageinfo_links,
                               tooltip='Details')]

                   ])]]
second_column = layout_pageinfo

layout = [[
    sg.Column(first_column_tab_group),
    sg.VSeparator(),
    sg.Column(second_column)
]]


def runSearchClicked(search_phrase, depth_of_search, window, queue_of_results):
    crawler = Crawler()

    results = crawler.look_for_links(search_phrase, depth_of_search)
    if (results.webpage_dict.keys()):
        window['-WEBSITE LIST-'].update(
            results.webpage_dict.keys())
        print("I searched ", results,
              "links and found  pages")

    queue_of_results.append(results)

    return results


def startGUI():

    queue_of_results = []
    current_result = None
    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()

        if event == 'OPEN':
            print('open')
            if (len(queue_of_results) > 0):
                print(queue_of_results)
        # Start search in separate thread
        if event == "OK":
            th = threading.Thread(
                target=runSearchClicked, args=(str(values['_SEARCH PHRASE_']), int(values['_DEPTH OF SEARCH_']), window, queue_of_results))
            th.start()

        if event == sg.WIN_CLOSED:
            break

        if event == "-WEBSITE LIST-":
            # if there is new data in the queue get it
            if (len(queue_of_results) > 0):
                current_result = queue_of_results.pop(
                )

        # show webpage info in the right layout
            if (values['-WEBSITE LIST-']):
                selected_page_url = values["-WEBSITE LIST-"][0]
                selected_webpageinfo = current_result.webpage_dict[selected_page_url]
                window['-PAGEINFO MENTIONS-'].update(
                    selected_webpageinfo.mentions)
                window['-PAGEINFO LINKS-'].update(
                    selected_webpageinfo.links_found)

                print(selected_page_url)
                print(selected_webpageinfo.links_found)

        # show selected mention in textbox
        if event == '-PAGEINFO MENTIONS-':

            mentions = values['-PAGEINFO MENTIONS-'][0]
            window['textbox'].update(mentions)

    window.close()
