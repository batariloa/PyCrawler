import PySimpleGUI as sg

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import threading

from crawl import Crawler

import tkinter
from search_results import SearchResults
from EventListGUI import EventList


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
                sg.Input("5", key='_DEPTH OF SEARCH_', size=(15, 5))]])],

    [sg.Button("OK")],
    layout_websites,
    [sg.Button("OPEN")]
]


layout_pageinfo = [[sg.Text("Page URL: "), sg.Text("None", key='-CURRENT URL-', size=(50, 1))],
                   [sg.HSeparator()],
                   [sg.Text("Number of links found: "), sg.Text(
                       "0", key='-WEBPAGE LINKS FOUND-')],

                   [sg.HSeparator()],

                   [sg.Text("Number of mentions found: "), sg.Text(
                       "0", key='-WEBPAGE MENTIONS FOUND-')],
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


def runSearchClicked(search_phrase, depth_of_search, queue_of_results):

    crawler = Crawler()

    results = crawler.look_for_links(
        search_phrase, depth_of_search, queue_of_results)

    return results


def startGUI():
    current_result = None
    window = sg.Window("Demo", layout)
    queue_of_results = EventList(window)

    while True:
        event, values = window.read()

        if event == "OK":
            th = threading.Thread(
                target=runSearchClicked, args=(str(values['_SEARCH PHRASE_']), int(values['_DEPTH OF SEARCH_']), queue_of_results))
            th.start()

        if event == sg.WIN_CLOSED:
            break

        if event == "-WEBSITE LIST-":

            # show webpage info in the right layout
            if (values['-WEBSITE LIST-']):
                selected_page_url = values["-WEBSITE LIST-"][0]
                selected_webpageinfo = queue_of_results[-1][
                    selected_page_url]
                window['-PAGEINFO MENTIONS-'].update(
                    selected_webpageinfo.mentions)
                window['-PAGEINFO LINKS-'].update(
                    selected_webpageinfo.links_found)
                window['-CURRENT URL-'].update(selected_webpageinfo.webpage)
                window['-WEBPAGE LINKS FOUND-'].update(
                    len(selected_webpageinfo.links_found))
                window['-WEBPAGE MENTIONS FOUND-'].update(
                    len(selected_webpageinfo.mentions))

                print(selected_page_url)
                print(selected_webpageinfo.links_found)

        # show selected mention in textbox
        if event == '-PAGEINFO MENTIONS-':

            mentions = values['-PAGEINFO MENTIONS-']
            if (len(mentions) > 0):
                window['textbox'].update(mentions[0])

    window.close()
