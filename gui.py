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
                              size=(40, 30),  key='-WEBSITE LIST-')]


layout_pageinfo_mentions = [
    [sg.Listbox(values=[], enable_events=True,
                size=(40, 20), key="-PAGEINFO MENTIONS-")],
    [sg.Multiline(size=(40, 10), key='textbox')]]

layout_pageinfo_links = [
    [sg.Listbox(values=[], enable_events=True,
                size=(40, 30), key="-PAGEINFO LINKS-")]]

first_column_tab_group = [
    [sg.Text("hello there")],
    [sg.Input(key='_SEARCH PHRASE_')],
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


def runSearchClicked(search_phrase, depth_of_search):
    crawler = Crawler()

    results = crawler.look_for_links(search_phrase, depth_of_search)
    print("I searched ", results,
          "links and found  pages")

    return results


def startGUI(executor):

    queue_1 = []
    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()

        if event == 'OPEN':
            print('open')
        # Start search
        if event == "OK":
            th = threading.Thread(
                target=runSearchClicked, args=(values['_SEARCH PHRASE_'], 5))
            th.start()

        if event == sg.WIN_CLOSED:
            break

        # show webpage info in the right layout
        if event == "-WEBSITE LIST-":
            selected_page_url = values["-WEBSITE LIST-"][0]
            if (results):
                selected_webpageinfo = results.webpage_dict[selected_page_url]
                window['-PAGEINFO MENTIONS-'].update(
                    selected_webpageinfo.mentions)
                window['-PAGEINFO LINKS-'].update(
                    selected_webpageinfo.links_found)

            print(selected_page_url)
            print(selected_webpageinfo.links_found)

        # show selected mention in textbox
        if event == '-PAGEINFO MENTIONS-':
            window['textbox'].update(values['-PAGEINFO MENTIONS-'])

    window.close()
