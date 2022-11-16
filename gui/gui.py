import PySimpleGUI as sg

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools
import threading

from crawl_core.crawl import Crawler

import tkinter
from util.result_handler import ResultHandler

import pyperclip

from gui.button_functions import runSearchClicked, resumeClicked, openLinkInBrowser, updatePageInfo, stopClicked, pauseClicked
from gui.layout import layout

from my_enum.gui_variables import WindowVariables as wv


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
        if event == wv.start:
            if (values[wv.input_depth_of_search].isnumeric() and int(values[wv.input_depth_of_search]) > 0 and len(values[wv.input_search_phrase]) > 0):
                crawler = Crawler(
                    str(values[wv.input_search_phrase]), int(values[wv.input_depth_of_search]), result_handler)
                th = threading.Thread(
                    target=runSearchClicked, args=(crawler, window))
                th.start()

        if event == wv.stop:
            stopClicked(result_handler, window)

        if event == wv.pause:
            pauseClicked(result_handler, window)

        if event == wv.resume:
            th = threading.Thread(
                target=resumeClicked, args=(crawler, window))
            th.start()

        # show selected webpage info in the right layout
        if event == wv.list_of_websites:

            if (values[wv.list_of_websites]):
                selected_page_url = values[wv.list_of_websites][0]

                selected_webpageinfo = result_handler.current_result[
                    selected_page_url]

                updatePageInfo(window, selected_webpageinfo)
        # show selected mention in textbox
        if event == wv.list_of_page_mentions:
            mentions = values[wv.list_of_page_mentions]
            if (len(mentions) > 0):
                window[wv.textbox].update(mentions[0])

        # clicked copy to clipboard
        if event == wv.btn_copy_to_clipboard:
            current_link_selected = values[wv.list_of_page_links][0]
            if (current_link_selected):
                pyperclip.copy(current_link_selected)

        # clicked open link in browser
        if event == wv.btn_open_link_in_browser:
            current_link_selected = values[wv.list_of_page_links][0]
            openLinkInBrowser(current_link_selected)

    window.close()
