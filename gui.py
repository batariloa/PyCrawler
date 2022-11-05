import PySimpleGUI as sg

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import asyncio
from crawl import Crawler

import tkinter
from search_results import SearchResults


layout_websites = [
    [sg.Listbox(values=[], enable_events=True,
                size=(40, 20), key="-WEBSITE LIST-")]]

layout_context = [[sg.Text('yep')]]

first_column_tab_group = [
    [sg.Text("hello there")],
    [sg.Input(key='_SEARCH PHRASE_')],
    [sg.Button("OK")],
    [sg.TabGroup([
        [sg.Tab('websites', layout_websites,
                tooltip='Details', key='-TAB WEBSITES-')],
        [sg.Tab('Context', layout_context,
                tooltip='Details', key='-TAB CONTEXT-')]

    ])],
    [sg.Button("OPEN")]
]

second_column = [[sg.Text("hello")],


                 ]

layout = [[
    sg.Column(first_column_tab_group),
    sg.VSeparator(),
    sg.Column(second_column)
]]


async def runSearchClicked(search_phrase):
    crawler = Crawler()

    results = await crawler.look_for_links(search_phrase)
    print("I searched ", results.webpage_dict,
          "links and found  pages")

    return results


async def startGUI():

    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()

        if event == "OK":
            results = await runSearchClicked(values['_SEARCH PHRASE_'])
            window["-WEBSITE LIST-"].update(results.webpage_dict.keys())

        if event == sg.WIN_CLOSED:
            break

        if event == "OPEN":
            print(values["-WEBSITE LIST-"])

        if event == "-TAB WEBSITES-":
            print('lol')

    window.close()
