import sys
sys.path.append('..')

import pandas as pd
import time
import datefinder

class featureExtractor(object):
    """
    Pull out features (title, location, time) from the lxml
    """
    def __init__(self, urlTextFoodDF):
        super(featureExtractor, self).__init__()
        self.df = urlTextFoodDF
        

    def get_title(self):
        """Add a title column to the df
        :returns: TODO

        """
        df = self.df

        titleSeries = df.lxml.apply(lambda x: x.title.string)

        return titleSeries

    def get_date(self):
        df = self.df
        
        # catch possible lack of date found
        dateSeries = df.text.apply(
            lambda x: 
                list(datefinder.find_dates(x, strict=True))[0].strftime('%-m/%-d/%Y')
                if list(datefinder.find_dates(x, strict=True))
                else None
        )

        return dateSeries

    def extract_features(self):

        df = self.df

        # extract title
        title = self.get_title()
        df = df.assign(title=title)

        #extract date
        day = self.get_date()
        df = df.assign(day=day)

        return df
