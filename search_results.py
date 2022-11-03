class SearchResults:

    def __init__(self, pages_searched, links_found):
        self.pages_searched = pages_searched
        self.links_found = links_found

    def display(self):
        print("Roll No.: %d \npages_searched: %s" %
              (self.links_found, self.pages_searched))
