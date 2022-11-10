def runSearchClicked(crawler, window):

    window['-STATUS-'].update('Crawling..')
    results = crawler.beginSearch()
    window['-STATUS-'].update('Done.')


def resumeClicked(crawler, window):
    window['-STATUS-'].update('Crawling..')
    crawler.resume_search()
    window['-STATUS-'].update('Done.')
