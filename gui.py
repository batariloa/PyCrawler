import PySimpleGUI as sg

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import asyncio
from crawl import Crawler

from langdetect import detect

from search_results import SearchResults


layout_websites = [
    [sg.Listbox(values=[], enable_events=True,
                size=(40, 20), key="-WEBSITE LIST-")]]

first_column_tab_group = [
    [sg.Text("hello there")],
    [sg.Button("OK")],
    [sg.TabGroup([[sg.Tab('websites', layout_websites, tooltip='Details')]])],
    [sg.Button("OPEN")]
]

second_column = [[sg.Text("hello")],
                 ]

layout = [[
    sg.Column(first_column_tab_group),
    sg.VSeparator(),
    sg.Column(second_column)
]]


async def runSearchClicked():
    crawler = Crawler()

    print('Crawler variables ', crawler.links_found)
    results = await crawler.look_for_links("Prdonja")
    print("I searched ", results.pages_searched,
          "links and found ", results.links_found, " pages")
    print('Sentences where its mentioned, ', results.sentences)
    return results


async def startGUI():

    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()

        if event == "OK":
            results = await runSearchClicked()
            window["-WEBSITE LIST-"].update(results.links_found)

        if event == sg.WIN_CLOSED:
            break

        if event == "OPEN":
            print(values["-WEBSITE LIST-"])

    window.close()
