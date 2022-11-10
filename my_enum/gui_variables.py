from strenum import StrEnum


class WindowVariables(StrEnum):
    list_of_websites = "-WEBSITE LIST-"
    list_of_page_mentions = "-PAGEINFO MENTIONS-"
    list_of_page_links = "-PAGEINFO LINKS-"
    input_search_phrase = '_SEARCH PHRASE_'
    input_depth_of_search = '_DEPTH OF SEARCH_'
    btn_open_link_in_browser = '-OPEN LINK IN BROWSER-'
    btn_copy_to_clipboard = '-COPY TO CLIPBOARD-'
    number_of_links_found = 'NUMBER OF LINKS FOUND'
    number_of_mentions_found = 'NUMBER OF MENTIONS FOUND'
    text_current_url = "CURRENT URL"
    text_status = "STATUS"
