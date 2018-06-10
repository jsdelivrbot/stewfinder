import pandas as pd
import time
import re
import datefinder

class featureExtractor(object):
    """
    Pull out features (title, location, time) from the lxml
    """
    def __init__(self, urlTextFoodDF, 
                 whenTag=None, locationTag=None, descTag=None,
                 whenClass=None, descClass=None, locationClass=None,
                 whenRegex='.*', locationRegex='.*'):
        super(featureExtractor, self).__init__()
        self.df = urlTextFoodDF

        self.whenTag = whenTag
        self.descTag = descTag
        self.locationTag = locationTag

        self.descClass = descClass
        self.whenClass = whenClass
        self.locationClass = locationClass

        self.whenRegex = whenRegex
        self.locationRegex = locationRegex
        
    def find_title(self, row):
        try:
            title = row.title.string
            return title

        except Exception:
            return None

    def apply_title(self):
        """Add a title column to the df
        :returns: TODO

        """
        df = self.df

        titleSeries = df.lxml.apply(lambda x: self.find_title(x))

        return titleSeries

    def find_date(self, row):
        if list(datefinder.find_dates(row, strict=True)):
            return list(datefinder.find_dates(row, strict=True))[0].strftime('%-m/%-d/%Y')
        else:
            return None

    def apply_date(self):
        df = self.df
        
        # catch possible lack of date found
        dateSeries = df.text.apply(
            lambda x: self.find_date(x)
        )

        return dateSeries

    def find_when(self, row):
        # apply the first 40 charcters of the tag / class combo of the event time
        # details (If they exist) -- strip off whitespace and add an elipsis for

        try:
            r = re.compile(self.whenRegex)

            when = [x.text[0:40] for x in row.find_all(
                self.whenTag, {"class": self.whenClass})]

            when = list(filter(r.search, when))

            when = when[0].strip() + '...'

            # when = (
                # row.find(
                    # self.whenTag, 
                    # {"class": self.whenClass}).text[0:40]
            # ).strip() + '...'

            return when

        except Exception:
            return None

    # this is stupidly named, it should be apply_time().. go figure
    def apply_when(self):
        df = self.df
        whenTag = self.whenTag
        whenClass = self.whenClass

        whenSeries = df.lxml.apply(
            lambda x: self.find_when(x)
        )

        return whenSeries

    def find_desc(self, row):
        try:
            desc = row.find(
                self.descTag, {"class": self.descClass}).text
            return desc

        except Exception:
            return None

    def apply_desc(self):
        # will replace the "text" column and apply summarized later
        df = self.df
        descTag = self.descTag
        descClass = self.descClass

        descSeries = df.lxml.apply(
            lambda x: self.find_desc(x)
        )

        return descSeries

    def find_location(self, row):
        try:
            r = re.compile(self.locationRegex)

            location = [x.text for x in row.find_all(
                self.locationTag, {"class": self.locationClass})]

            location = list(filter(r.search, location))

            location = location[0]

            return location

        except Exception:
            return None


    def apply_location(self):
        df = self.df
        locationTag = self.locationTag
        locationClass = self.locationClass

        locationSeries = df.lxml.apply(
            lambda x: self.find_location(x)
        )

        return locationSeries


    def extract_features(self):

        df = self.df

        # extract title
        title = self.apply_title()
        df = df.assign(title=title)

        #extract date
        day = self.apply_date()
        df = df.assign(day=day)

        #extract when
        df = df.assign(when=None)
        if self.whenTag:
            when = self.apply_when()
            df = df.assign(when=when)

        # exctract description
        #df.text already exists from soopPull.getTextFromLinks
        if self.descTag:
            desc = self.apply_desc()
            df = df.assign(text=desc)

        df=df.assign(location=None)
        if self.locationTag:
            location = self.apply_location()
            df = df.assign(location=location)


        return df
