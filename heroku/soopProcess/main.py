import soopPull
from soopProcess.extractFeatures import *
from soopProcess.summarizeText import *
from soopProcess.validateText import *


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
                 linkBase=None,
                 day=None
                 ):
        super(processor, self).__init__()

        self.baseUrl = baseUrl
        self.urlType = urlType
        self.startNum = startNum
        self.endNum = endNum
        self.linkBase = linkBase
        self.linkRegex = linkRegex
        self.day = day

        # build input Df using the soopPull module and the information above
        self.inputDF = self.build_input_DF()

    def build_input_DF(self):
        # use the soopPull module
        getter = soopPull.puller(
            self.baseUrl,
            self.urlType,
            self.startNum,
            self.endNum,
            self.linkBase,
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

    def build_featured_DF(self, inputDf,
                          whenTag, descTag, locationTag,
                          whenClass, descClass, locationClass):
        # from extractFeatures

        extractor = featureExtractor(
            inputDf,
            whenTag=whenTag, descTag=descTag, locationTag=locationTag,
            whenClass=whenClass, descClass=descClass, locationClass=locationClass
        )

        featuredDF = extractor.extract_features()

        return featuredDF

    def build_text_summarizer(self, inputDF, *args, **kwargs):
        # then build the summarizer
        summarizer = textSummarizer(inputDF, *args, **kwargs)
        summarizedDF = summarizer.summarize_df()

        # and return it

        return summarizedDF

    def check_links(self):
        inputDF = self.build_input_DF()

        return inputDF.outUrl

    def process(self,
                whenTag=None, descTag=None, locationTag=None,
                whenClass=None, descClass=None, locationClass=None,
                *args, **kwargs):

        df = self.inputDF

        # build validated DF using inputDF
        validatedDF = self.build_validated_DF(df)

        # build the feature extractor
        featuredDF = self.build_featured_DF(
            validatedDF,
            whenTag=whenTag,
            descTag=descTag,
            locationTag=locationTag,
            whenClass=whenClass,
            descClass=descClass,
            locationClass=locationClass
        )

        # pass *args and **kwargs to the summarizer
        summarizedDF = self.build_text_summarizer(
            featuredDF,
            *args,
            **kwargs
        )

        df = summarizedDF

        if self.day:
            df = df.assign(day=self.day)

        return df
