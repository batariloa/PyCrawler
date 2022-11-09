from webpageinfo import WebpageInfo


class SearchResults:

    def __init__(self, webpage_dict):
        self.webpage_dict = webpage_dict
        self.pages_searched = len(webpage_dict)

    def display(self):
        print("Roll No.: %d \npages_searched: %s" %
              (self.links_found, self.pages_searched))
