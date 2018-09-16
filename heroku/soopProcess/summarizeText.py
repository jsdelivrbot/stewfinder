from sumyrizer import *


class textSummarizer(object):
    """
    Takes a df and adds a summary column
    """

    def __init__(self,
                 inputDF,
                 num_sentences=1,
                 num_words=3,
                 stopwords='sumyrizer/stopwords.txt',
                 important_words='sumyrizer/important_words.txt',
                 *args,
                 **kwargs
                 ):

        super(textSummarizer, self).__init__()

        self.inputDF = inputDF
        self.textSum = smy.summarizer(
            text_type='pre_proc',
            num_sentences=num_sentences,
            num_words=num_words,
            stopwords=stopwords,
            important_words=important_words,
            *args, **kwargs)

    def summarize_row(self, text):
        try:
            words, sentences = self.textSum.summarize([text])

            return ' '.join(sentences.sentences)

        except Exception as e:
            # sometimes it throws a link with no text, that is sad panda
            pass

    def summarize_df(self):
        df = self.inputDF
        summary = df.text.apply(lambda x: self.summarize_row(x))

        df = df.assign(details=summary)

        # validate the df to remove rows with no text
        df = df.loc[df['text'].values != None]

        return df
