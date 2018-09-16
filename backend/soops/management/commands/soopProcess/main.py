import sys
sys.path.append('..')

from soops.management.commands.soopProcess.extractFeatures import *
from soops.management.commands.soopProcess.validateText import *
from soops.management.commands.soopProcess.summarizeText import *

import soops.management.commands.soopPull as soopPull

class processor(object):
    """
    Main processor class for soup, combines extraction, validation, and
    summarization

    :baseUrl: url without any link addons
    :urlType: 'numbered' or 'crawled'
    :linkRegex: the regex pattern to find relative links --> appended to baseUrl
    """
    def __init__(self, 
                 baseUrl, 
                 urlType='numbered', 
                 startNum=None, 
                 endNum=None, 
                 linkRegex=None,
                 today=False,
                 *args,
                 **kwargs
                ):
        super(processor, self).__init__()

        self.baseUrl = baseUrl
        self.urlType = urlType
        self.startNum = startNum
        self.endNum = endNum
        self.linkRegex = linkRegex
        self.today = today

        # build input Df using the soopPull module and the information above
        self.inputDF = self.build_input_DF()

        # build validated DF using inputDF
        self.validatedDF = self.build_validated_DF(self.inputDF)

        # build the feature extractor
        self.featuredDF = self.build_featured_DF(self.validatedDF)

        # pass *args and **kwargs to the summarizer
        self.textSum = self.build_text_summarizer(
            self.featuredDF,
            *args, 
            **kwargs
        )


    def build_input_DF(self):
        # use the soopPull module
        getter = soopPull.puller(
            self.baseUrl,
            self.urlType,
            self.startNum,
            self.endNum,
            self.linkRegex
        )

        # return the unvalidated df
        inputDF = getter.pull()
        
        return inputDF

    def build_validated_DF(self, inputDF):
        # build the validator from validateText
        validator = textValidator(inputDF)
        validatedDF = validator.validate_food_df()

        # return validated df
        return validatedDF

    def build_featured_DF(self, inputDf):
        # from extractFeatures
        extractor = featureExtractor(inputDf)
        featuredDF = extractor.extract_features()

        return featuredDF

    def build_text_summarizer(self, inputDF, *args, **kwargs):
        # then build the summarizer
        summarizer = textSummarizer(inputDF, *args, **kwargs)

        # and return it
        return summarizer

    def check_links(self):
        inputDF = self.build_input_DF()

        return inputDF.outUrl
        

    def process(self):
        df = self.featuredDF

        summary = self.textSum.summarize_df().loc[:, 'details']
        df = df.assign(details=summary)

        if self.today == True:
            df = df.assign(day=time.strftime('%-m/%-d/%Y'))

        return df



