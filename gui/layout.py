import PySimpleGUI as sg
from my_enum.gui_variables import WindowVariables as wv


layout_websites = [sg.Listbox(values=[], enable_events=True,
                              size=(50, 30),  key=wv.list_of_websites)]


layout_pageinfo_mentions = [
    [sg.Listbox(values=[], enable_events=True,
                size=(50, 20), key=wv.list_of_page_mentions)],
    [sg.Multiline(size=(50, 10), key='textbox')]]

layout_pageinfo_links = [
    [sg.Listbox(values=[], enable_events=True,
                size=(50, 30), key=wv.list_of_page_links),
     ], [sg.Button("Copy to clipboard", key=wv.btn_copy_to_clipboard),
         sg.Button("Open link in browser", key=wv.btn_open_link_in_browser)]]

first_column_tab_group = [
    [sg.Column([[sg.Text("Search phrase:")], [
               sg.Input(key=wv.input_search_phrase, size=(35, 5))]]),
     sg.Column([[sg.Text("Depth of search:")], [
                sg.Input("5", key=wv.input_depth_of_search, size=(15, 5))]])],

    [sg.Button("Start", size=(15, 1)), sg.Button("Stop", size=(15, 1)),
     sg.Button("Pause", size=(15, 1)), sg.Button("Resume", size=(15, 1))],
    layout_websites,
    [sg.Text('Waiting..', key=wv.text_status)]
]


layout_pageinfo = [[sg.Text("Page URL: "), sg.Text("None", key=wv.text_current_url, size=(50, 1))],
                   [sg.HSeparator()],
                   [sg.Text("Number of links found: "), sg.Text(
                       "0", key=wv.number_of_links_found)],

                   [sg.HSeparator()],

                   [sg.Text("Number of mentions found: "), sg.Text(
                       "0", key=wv.number_of_mentions_found)],
                   [sg.TabGroup([
                       [sg.Tab('Mentions', layout_pageinfo_mentions,
                               tooltip='Details', key=wv.list_of_page_mentions)],
                       [sg.Tab('Links found', layout_pageinfo_links,
                               tooltip='Details')]

                   ])]]
second_column = layout_pageinfo

layout = [[
    sg.Column(first_column_tab_group),
    sg.VSeparator(),
    sg.Column(second_column)
]]
