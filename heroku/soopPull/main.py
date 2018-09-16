from soopPull.getLinks import *
from soopPull.getTextFromLinks import *


class puller(object):
    """
    Combines the link getting and text pulling into one

    :baseUrl: url without any link addons
    :urlType: 'numbered' or 'crawled'
    :linkRegex: the regex pattern to find relative links --> appended to baseUrl
    """

    def __init__(self,
                 baseUrl,
                 urlType='numbered',
                 startNum=None,
                 endNum=None,
                 linkBase=None,
                 linkRegex=None,
                 *args,
                 **kwargs
                 ):
        super(puller, self).__init__(*args, **kwargs)
        self.baseUrl = baseUrl
        self.urlType = urlType
        self.startNum = startNum
        self.endNum = endNum
        self.linkBase = linkBase
        self.linkRegex = linkRegex

    def pull(self):
        """Pull text based on urlType
        :returns: DF with id | lxml | url | text

        """

        # ie use the numbered link generator

        if self.urlType == 'numbered':

            # build the links
            linkLister = numberedLinks(
                baseUrl=self.baseUrl,
                startNum=self.startNum,
                endNum=self.endNum
            )

            links = linkLister.get_links()

        if self.urlType == 'crawled':
            linkLister = crawlLinks(
                baseUrl=self.baseUrl,
                linkBase=self.linkBase,
                linkRegex=self.linkRegex
            )

            links = linkLister.get_links()

        textGetter = textScraper(links)
        df = textGetter.get_text_from_link_list()

        return df
