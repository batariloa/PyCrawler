import PySimpleGUI as sg


layout_websites = [sg.Listbox(values=[], enable_events=True,
                              size=(50, 30),  key='-WEBSITE LIST-')]


layout_pageinfo_mentions = [
    [sg.Listbox(values=[], enable_events=True,
                size=(50, 20), key="-PAGEINFO MENTIONS-")],
    [sg.Multiline(size=(50, 10), key='textbox')]]

layout_pageinfo_links = [
    [sg.Listbox(values=[], enable_events=True,
                size=(50, 30), key="-PAGEINFO LINKS-"),
     ], [sg.Button("Copy to clipboard", key="-COPY TO CLIPBOARD-"),
         sg.Button("Open link in browser", key="-OPEN LINK IN BROWSER-")]]

first_column_tab_group = [
    [sg.Column([[sg.Text("Search phrase:")], [
               sg.Input(key='_SEARCH PHRASE_', size=(35, 5))]]),
     sg.Column([[sg.Text("Depth of search:")], [
                sg.Input("5", key='_DEPTH OF SEARCH_', size=(15, 5))]])],

    [sg.Button("Start", size=(15, 1)), sg.Button("Stop", size=(15, 1)),
     sg.Button("Pause", size=(15, 1)), sg.Button("Resume", size=(15, 1))],
    layout_websites,
    [sg.Text('Waiting..', key='-STATUS-')]
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
