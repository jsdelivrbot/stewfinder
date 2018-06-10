import pandas as pd

foodWords = set([
    "reception",
    "icecream",
    "bbq",
    "barbecue",
    "pizza",
    "snacks",
    "refreshments",
    "breakfast",
    "lunch",
    "free",
    "dinner",
    "will be served",
    "will be serving",
    'potluck',
    'coffee',
    'cookies',
    'yummy'
])


stopWords = set([
    'red tractor',
    'cost is $',
    'cost $',
    'baby bistro',
    'international travel health and safety',
    'montana sourced lunch special',
    'study abroad drop',
])


class textValidator(object):
    """
    Scan text for food words and decide whether an event contains food

    requires a DF with id | url | text to scan
    """
    def __init__(self, urlTextDF):
        super(textValidator, self).__init__()
        self.urlTextDF = urlTextDF


    def validate_food_string(self, text):
        """Scan a single string for matches

        :returns: an array of food word matches
        """

        # do a case insensitive search on text by enforcing lower case
        textLowered = text.lower()

        # check for stopWord phrases
        if any(x in textLowered for x in stopWords):
            return list()

        textLowered = textLowered.split()
        textLowered = set(textLowered)


        # check for foodwords
        foodWordsPresent = set.intersection(foodWords, textLowered)

        return list(foodWordsPresent)


    def validate_food_df(self):
        """Scan the entire textDF for food matches

        :returns: a DF with:
            id | url | text | [food, items]
        """

        # pull out the text as a pandas Series and validate each row
        textSeries = self.urlTextDF.loc[:, 'text']
        textSeries = textSeries.apply(lambda x: self.validate_food_string(x))

        # put the food into its own column as a list
        urlTextFoodDF = self.urlTextDF
        urlTextFoodDF['food'] = textSeries

        # filter out the rows with no food
        # urlTextFoodDF = urlTextFoodDF.loc[
            # urlTextFoodDF.food.apply(lambda x: len(x)) > 0]

        return urlTextFoodDF
