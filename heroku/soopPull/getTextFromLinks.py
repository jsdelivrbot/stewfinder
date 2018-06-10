import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

# keep periods for sentence parsing
# get rid of hyphens without spacing for txt summarization reasons
punct = {'!': ' ',
         '"': ' ',
         ',': ' ',
         '#': ' ',
         # '$': ' ',
         '%': ' ',
         '&': ' ',
         ')': ' ',
         '+': ' ',
         '/': ' ',
         ';': ' ',
         '=': ' ',
         '?': ' ',
         '[': ' ',
         ']': ' ',
         '_': ' ',
         '{': ' ',
         '}': ' ',
         '}': ' ',
         '\n':'',
         '\xa0':'',
         '-': '',}

punctuator = str.maketrans(punct)


class textScraper(object):
    """
    This class accepts a list of links. It will parse the text from all links
    it is passed and return a pandas DF where each row contains:

        id | url | text
    """
    def __init__(self, linkList):
        super(textScraper, self).__init__()
        self.linkList = linkList


    def get_raw_lxml(self, url):
        """Pull the raw lxml tags from a single link

        :url: the url to pull
        :returns: BeautifulSoup object

        """
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        return soup


    def get_lxml_and_text_from_url(self, url):
        """Pull the text from a single link

        :returns: string with text from link

        """

        # request and read the url
        soup = self.get_raw_lxml(url)
        lxml = soup

        # throw out the tags that don't tend to contain text
        [s.extract() for s in soup([
            'pre',
            'style',
            'script',
            'nav',
            'meta',
            'li'
            '[document]',])
             # 'head',
             # 'title'])
        ]

        # throw out the classes that don't contain text
        # for div in soup.find_all("div", {'class':'hidden-print'}):
            # div.decompose()

        removeClasses = re.compile(
            '.*email.*|.*phone.*|.*advertise.*|.*footer.*|.*muted.*|.*dropdown.*|.*nav.*|.*hidden.*|.*meta.*|.*logo.*|.*title.*|.*copyright.*' 
        )

        for thing in soup.find_all(
                True, {
                    'class': [
                        'dropdown-menu', 
                        'nav',
                        'subnav-logo',
                        'breadcrumb',
                        'meta',
                        'hidden'
                    ]
                }):

            thing.decompose()

        for thing in soup.find_all(
            True, {"class": removeClasses}
        ):
            thing.decompose()

        # get the text that's left
        text = soup.get_text().translate(punctuator)

        return lxml, text

    def get_text_from_link_list(self):
        """Pull the text from every link in the link list
        :returns: pandas DF with id | lxml | url | text
        """
        urlTextDF = pd.DataFrame(columns=['lxml', 'outUrl', 'text'])

        # read each url and add the text into the DF

        for url in self.linkList:
            # catch 404 errors
            try:
                lxml, text = self.get_lxml_and_text_from_url(url)

                # .append creates a new object every time IE must reassign
                urlTextDF = urlTextDF.append({
                    'lxml': lxml,
                    'outUrl': url,
                    'text': text
                }, ignore_index=True)

            except urllib.error.HTTPError:
                continue

        return urlTextDF
