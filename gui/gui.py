import PySimpleGUI as sg

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import threading

from crawl_core.crawl import Crawler

import tkinter
from util.result_handler import ResultHandler

from util.driver_util import createChromeDriver
import pyperclip

from gui.button_functions import runSearchClicked, resumeClicked

from gui.layout import layout


def startGUI():
    current_result = None
    window = sg.Window("PyCrawl", layout)
    result_handler = ResultHandler(window)
    crawler = None

    while True:
        event, values = window.read()

        # close window
        if event == sg.WIN_CLOSED:
            break

        # start search in separate Thread
        if event == "Start":
            crawler = Crawler(
                str(values['_SEARCH PHRASE_']), int(values['_DEPTH OF SEARCH_']), result_handler)
            th = threading.Thread(
                target=runSearchClicked, args=(crawler, window))
            th.start()

        if event == "Stop":
            result_handler.stop()

        if event == "Pause":
            result_handler.pause()

        if event == "Resume":
            th = threading.Thread(
                target=resumeClicked, args=(crawler, window))
            th.start()

        if event == "-WEBSITE LIST-":

            # show webpage info in the right layout
            if (values['-WEBSITE LIST-']):
                selected_page_url = values["-WEBSITE LIST-"][0]
                selected_webpageinfo = result_handler.current_result[
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

        if event == '-COPY TO CLIPBOARD-':
            current_link_selected = values['-PAGEINFO LINKS-'][0]

            if (current_link_selected):
                pyperclip.copy(current_link_selected)

        if event == '-OPEN LINK IN BROWSER-':
            current_link_selected = values['-PAGEINFO LINKS-'][0]

            if (current_link_selected):
                driver = createChromeDriver()

            driver.get(current_link_selected)

    window.close()
