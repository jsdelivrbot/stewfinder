import re

import requests

from bs4 import BeautifulSoup


class linkGetter(object):
    """
    Superclass for numbered and crawling link getters
    """

    def __init__(self, baseUrl, *args, **kwargs):
        """
        :baseUrl: The baseUrl from which numbering / crawling will be done
        """

        super(linkGetter, self).__init__()
        self.baseUrl = baseUrl

    def get_links(self, links=None):
        """
        basline method (subclasses should override this)
        :returns: an array of links
        """

        return links

    def validate_links(self):
        """Check links produced by get_links against the links which have
        already been scraped and added to the DB
        :returns: a filtered array of links

        """
        pass


class numberedLinks(linkGetter):
    """

    For use with sites that have a standard numbering on their event links
    system -- IE http://calendar.msu.montana.edu/events/<event #>
    """

    def __init__(self, baseUrl, startNum, endNum, *args, **kwargs):
        """
        :startNum: the first <event #> to scrape
        :endNum: the final <event #> to scrape
        """

        super(numberedLinks, self).__init__(baseUrl=baseUrl, *args, **kwargs)
        self.startNum, self.endNum = startNum, endNum

    def get_links(self):
        """produce a list of links between start and end numbers
        :returns: an array (list) of numbered full links

        """

        return [self.baseUrl + str(num)
                for num in range(self.startNum, self.endNum)]


class crawlLinks(linkGetter):
    """

    For use with sites that do not have a standard numbering on event links
    Supports regex crawling to avoid off topic links:
        IE http://www.bozemanevents.net/04/28/2018/hyalite-hill-climb/
        has pattern <baseUrl>/month/day/year/<event name>

    ***linkRegex should ONLY MATCH THE RELATIVE PATH as it will be
    concatenated with the rest of the url
    """

    def __init__(self, baseUrl, linkRegex='.*',
                 linkBase=None, *args, **kwargs):
        super(crawlLinks, self).__init__(baseUrl=baseUrl, *args, **kwargs)
        self.linkRegex = linkRegex
        self.linkBase = linkBase

    def get_links(self):
        """Produce a list of links branching out from the baseUrl
        :returns: an array of regex-matched links
        """

        # request page
        r = requests.get(self.baseUrl)

        # parse the page into tagged items
        soup = BeautifulSoup(r.text, "lxml")

        # pick out a list of all link tags
        # IE linkTags[0] is:
        # <a href="http://www.bozemanevents.net/">Home</a>
        linkTags = soup.find_all('a', href=True)

        # extract the links from the linkTags
        # IE links[0] is:
        # http://www.bozemanevents.net/
        links = [x['href'] for x in linkTags]

        # filter links based on the provided regex
        # IE on eventul, links like this drop out:
        # //movies.eventful.com/bozeman/browse
        # but links like this stay:
        # //eventful.com/bozeman/events/zoso-/E0-001-112140272-1
        links = [x for x in links
                 if re.search(self.linkRegex, x)]

        # extract the relative url from the link
        links = [re.findall(self.linkRegex, x)[0] for x in links]

        # concat the basUrl or the linkBase for complete link

        if self.linkBase:
            links = [self.linkBase + x for x in links]

            return list(set(links))

        links = [self.baseUrl + x for x in links]

        return list(set(links))
