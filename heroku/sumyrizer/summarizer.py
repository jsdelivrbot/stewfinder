from sklearn.feature_extraction.text import TfidfVectorizer
from math import ceil


from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


import itertools
import pandas as pd
import numpy as np

# import all utility functions
from sumyrizer.utils import *

class summarizer():

    '''
    ATTRIBUTES:
    
    :location:                      file/path/ or www.url.com

    :text_type:                     "url", "file", or "pre_proc" 
                                    (a pre-processed string)

    :text:                          a list of strings to analyze
    :chunks:                        number of sections to segment

    :num_words:                     number of words to keep
    :num_sentences:                 number of sentences to keep
    
    :minimum:                       minimum word frequency cutoff
    :maximum:                       maximum word frequency cutoff
    :min_word_length:               minimum number of letters for important words
    :max_word_length:               maximum number of letters for important words
    :stopwords:                     a file of words to ignore (IE names in a meeting)

    
    For all weights, 0 corresponds to no change, negative corresponds
    to negative weighting and positive corresponds to positive weighting

   -------------------------------------------------------------- 
    
    :position_weight:               how heavily to weight the text document location
    :length_weight:                 how heavily to weight the length of the word
    :capital_weight:                how heavily to weight number of capital letters


   -------------------------------------------------------------- 
    
    METHODS:
    
    Most go from string list ----> DF
    However, text getters go from string list ----> string list
    
    :get_text:                      preprocess / segment text from url or file
    :get_chunks:                    returns the number of segments (IE chunks)

    :build_words:                   build words into a DF using TfidfVectorizer
    :build_sentences:               will keep all sentences AND stopwords

    :build_least_squares:           return the cross-correllation matrix  
    :merge_text:                    merge several segments (IE related)
    :correllate_cols:               build segments intelligently for input text

    :get_2_min_chunks:              placeholder method for marker file

    :weight_capitals:               weight based on number of capital letters
    :weight_word_length:            weight based on word length
    :weight_position:               weight based on position in page

    :combine_weights:               apply all weights to their segments
    :filter_data:                   drop out values v. big and v. small weights

    :summarize_words:               filter, clip, and return important words
    :summarize_sentences:           rank and return top sentences
    :summarize:                     do everything above in a sensible way


   -------------------------------------------------------------- 

    USAGE:


        FROM URL
        import summarizer as smy

        atlantic = smy.summarizer(
            location='https://www.theatlantic.com/entertainment/archive/2015/02/the-best-sentence-in-atlantic-history/384741/', 
            text_type='url',
            stopwords='stopwords.txt',
            position_weight=.5,
            capital_weight=.3,
            num_words=15,
            num_sentences=1
        )
        
        words, sentences = atlantic.summarize()

   -------------------------------------------------------------- 

        FROM FILE
        import summarizer as smy

        transcription = smy.summarizer(
            'transcription.txt', 
            'file', 
            stopwords='stopwords.txt', 
            min_word_length=2
        )

   -------------------------------------------------------------- 

        FROM NEITHER
        import summaryzer as smy

        smyrizer = smy.summarizer(num_words=1)

        words, sentences = smyrizer.summarize(
            ["tweaking parameters can vastly alter the results."]
        )

   -------------------------------------------------------------- 

        GOOD LUCK

   -------------------------------------------------------------- 
    '''

    def __init__(
        self, location=None, text_type=None, proc_str=None,
        num_words=10, num_sentences=5, minimum=.1, maximum=.9, 
        position_weight=1, length_weight=1, capital_weight=1, 
        min_word_length=3, max_word_length=20, stopwords=None,
        important_words=None, important_weight=1):


        self.minimum = minimum
        self.maximum = maximum
        self.num_words = num_words
        self.num_sentences = num_sentences

        self.position_weight = position_weight
        self.length_weight = length_weight
        self.capital_weight = capital_weight
        self.important_weight = important_weight

        self.min_word_length = min_word_length
        self.max_word_length = max_word_length

        self.location = location
        self.text_type = text_type

        self.important_words = None
        if important_words is not None:
            with open(important_words) as infile:
                self.important_words = infile.read().splitlines()

        self.stopwords = None
        if stopwords is not None:
            with open(stopwords) as infile:
                self.stopwords = infile.read().splitlines()

        self.proc_str = proc_str
        self.text = self.get_text()
        self.chunks = self.get_chunks()


    def get_text(self):
        '''
        :returns: list of intelligently segmented text
        '''

        if self.text_type == 'url':
            print('getting url')

            # method from utils
            text = get_text_from_url(self.location, chunks=self.get_2_min_chunks())
            return self.correllate_cols(text)


        if self.text_type == 'file':
            print('getting file')

            # method from utils
            text = get_text_from_file(self.location, chunks=self.get_2_min_chunks())
            return self.correllate_cols(text)

        if self.text_type == 'pre_proc':
            # print('getting pre-processed string')
            return [self.proc_str]
            

        return None

    def get_chunks(self):
        '''
        :returns: integer number of segments in text
        '''

        if self.text is None:
            return 1

        return len(self.text)


    def get_2_min_chunks(self):
        '''PLACEHOLDER METHOD
        :returns: 20 (assuming a ~1hr meeting)
        '''
        return 20


    def build_least_squares(self, text=None, use_idf=True, norm=None, *args, **tfidfargs):
        '''
        :returns: an upper triangular df with cross correllation values
        '''

        # method from utils
        least_squares_vec = np.vectorize(least_squares)

        # don't let params get passed to this one
        words_df = self.build_words(text, min_df=.05, max_df=.9, norm=None)

        # only the meeting segments
        segs_df = words_df.drop('words', axis=1)

        # empty df to hold the results
        squares_df = pd.DataFrame(index=segs_df.columns, columns=segs_df.columns)

        #populate the df with the least squares
        for row, col in itertools.combinations(segs_df.columns, 2):
            corr = np.sum(least_squares_vec(segs_df[row], segs_df[col], n=len(segs_df)))
            squares_df.loc[row, col] = corr
            #df.loc[col, row] = corr
        
        return squares_df


    def merge_text(self, startCol, endCol, text=None):
        '''
        :startCol: the column to begin merging
        :endCol: the column to cease merging

        :returns: list of strings that has merged columns from the original ~2
        minute text segments
        '''
        if text is None:
            text = self.text
        return [' '.join(text[startCol: (endCol + 1)])]


    def correllate_cols(self, text=None, *args, **tfidfargs):
        '''This method is usually called by get_text() don't call it manually
        unless you know what you're doing.  
        
        :text: generally passed from get_text()
        :returns: list of fully merged strings
        '''

        # build statistics 
        squares_df = self.build_least_squares(text, *args, **tfidfargs)
        squares_mean = np.mean(np.mean(squares_df))
        squares_std = np.mean(np.std(squares_df))

        thresh_max = squares_mean + 1.5 * squares_std # 86% confidence for uncorrellated
        thresh_min = squares_mean - squares_std # 66% confidenced for correllated


        # we want to default splitting a meeting into ~6 min chunks or 3 little chunks
        counter = 0
        counterMax = self.get_2_min_chunks() // 4
        startCol = 0
        endCol = 1
        mergedText=[]
        
        while endCol < len(squares_df.columns):

            mean = np.mean(np.mean(pd.DataFrame(squares_df.values[:, startCol:endCol])))
            std = np.mean(np.std(pd.DataFrame(squares_df.values[:, startCol:endCol])))

            if mean > thresh_max:
                mergedText += self.merge_text(startCol, endCol, text)
                print('uncorrellated, breaking', 'start col: ', 
                      startCol, " end col: ", endCol, 'mean: ', mean, ' std: ', std,)

                startCol = endCol
                counter = 0

            if (mean < thresh_min):
                print('maybe correllated, continuing', 'start col: ', 
                      startCol, " end col: ", endCol, 'mean: ', mean, ' std: ', std,)

                counter = 0
                # startCol = endCol

            if counter == counterMax:
                print('dunno, splitting anyway', 'start col: ', 
                      startCol, " end col: ", endCol, 'mean: ', mean, ' std: ', std,)

                mergedText += self.merge_text(startCol, endCol, text)
                startCol = endCol
                counter = 0


            counter += 1
            endCol += 1

        # merge the final text block
        mergedText += self.merge_text(startCol, endCol, text)

        print('higher -> uncorr: ', thresh_max)
        print('lower -> corr: ', thresh_min)

        return mergedText
    

    def build_words(self, text=None, *args, **tfidfargs):
        '''Applies TfidfVectorizer and drops stopwords
        
        :text: typically self.text

        :returns: a df with words and counts (typically normalized)
        '''
        if text is None:
            text = self.text

        # get words / counts
        vec = TfidfVectorizer(lowercase=False,
                             stop_words=self.stopwords,
                             *args, **tfidfargs)

        X = vec.fit_transform(text)

        # put them in a DF
        words_df = pd.DataFrame(
            X.toarray(), 
            columns = vec.get_feature_names())

        # rotate it for cosmetics
        words_df = words_df.transpose()

        # fix the index
        words_df.index = words_df.index.set_names(['words'])
        words_df = words_df.reset_index()

        # remove digit-only "words" the ~ negates selection
        words_df = words_df[~words_df['words'].str.isdigit()]

        # This is probably not necessary
        words_df = words_df.drop_duplicates('words')

        # Drop really long and really short words
        words_df = words_df[words_df['words'].apply(
                lambda x: 
                    (len(x) >= self.min_word_length) &
                    (len(x) <= self.max_word_length)
            )]

        return words_df


    def build_sentences(self, text=None):
        '''Tokenize sentences and build out segment / weight columns

        :text: typically self.text

        :returns: a DF with all sentences from the document
        '''
        if text is None:
            text = self.text
        
        # nltk expects a string
        text_string = ''.join(text)

        # it's able to tokenize into sentences
        sentences = sent_tokenize(
            text_string.replace('\n',' ').replace('\t',' ').replace('\r', ' ')
        )

        # we want these and an index to know which segment they belong to
        sentences_df = pd.DataFrame(sentences, columns=['sentences'])
        sentences_df['segIndex'] = pd.Series(0, index=sentences_df.index)

        # setting the index
        chunk_length = ceil(len(sentences_df) / self.chunks)

        # string so that it may be used to select segments
        for i in range(0, len(sentences_df), chunk_length):
            sentences_df.loc[i: i + chunk_length, ('segIndex')] = \
                int(ceil(i / chunk_length))

        # lastly, build a weight column to use later
        sentences_df['weight'] = pd.Series(0, index=sentences_df.index)
            
        return sentences_df.drop_duplicates('sentences')
    
    
    def weight_capitals(self, text=None, *args, **tfidfargs):
        '''capital_weight > 0 will weight capital letters more heavily

        :text: typically self.text
        
        :returns: a df with a column titled 'capital' that is normalized 
        and weighted by the number of capital letters 
        '''
        
        if self.capital_weight == 0:
            return self.build_words(text, *args, **tfidfargs)

        # build the words
        words_df = self.build_words(text, *args, **tfidfargs)

        # build the weights
        weights = pd.Series(
            self.capital_weight * words_df['words'].apply(

                # CAse --> 1*true + 1*true + 1*false + 1*false
                lambda x: sum(1 for letter in x if letter.isupper())
            ), index=words_df.index)

        # and, normalizing
        if max(weights) != 0:
            weights *= self.capital_weight / max(weights)

        words_df['capital'] = weights

        return words_df
    
    
    def weight_page_position(self, text=None, *args, **tfidfargs):
        """ self.position_weight > 0 will weight top of document more heavily

        :text: typically self.text
        
        :returns: a df with a column 'page_pos' that weights page position
        
        *a note on the algorithm:
        Things that appear earlier in the document have lower sentence index
        but we want them to be weighted more heavily because they are more likely
        to contain interesting bits of information
        """
        
        if self.position_weight == 0:
            return self.weight_capitals(text, *args, **tfidfargs)
            
        # build sentences and words
        words_df = self.weight_capitals(text, *args, **tfidfargs)
        sentences_df = self.build_sentences(text)
        

        # build weights (recall lower sentence index -> more important)
        weights = pd.Series(
            [

                # an array of same length as number of sentences
                # [5*false, 4*false, 3*true, 2*true, 1*false].sum()
                (
                    # 5 - [0, 1, 2, 3, 4]
                    (len(sentences_df) - sentences_df.index.values) *
                 
                    # [false, false, true, true, false]
                    sentences_df['sentences'].str.contains(
                        words_df['words'][value])
                ).sum()
                
                for value in words_df.index
            ], 

            index = words_df.index
        )

        # normalize the weights later
        weights *= self.position_weight / max(weights)
        
        words_df['page_pos'] =  weights       
        return words_df
    
        
    def weight_word_length(self, text=None, *args, **tfidfargs):
        ''' self.length_weight > 0 will weight longer words more heavily

        :text: typically self.text
        
        :returns: a df with 'len_wight' which is weighted by word length
        '''
        if text is None:
            text = self.text
            
        if self.length_weight == 0:
            return self.weight_page_position(text, *args, **tfidfargs)
        
        # build weights (longer words weighted more)
        words_df = self.weight_page_position(text, *args, **tfidfargs)

        weights = pd.Series(
            [
                len(words_df['words'][x])
                for x in words_df.index
            ], index=words_df.index
        )
        
        # and normalizing later
        weights *= self.length_weight / max(weights)
        # weights *= self.length_weight 

        words_df['len_weight'] = weights
        return words_df
    
        
    def weight_important_words(self, text=None, *args, **tfidfargs):
        ''' self.length_weight > 0 will weight longer words more heavily

        :text: typically self.text
        
        :returns: a df with 'len_wight' which is weighted by word length
        '''
        if text is None:
            text = self.text
            
        if (self.important_weight == 0) or (self.important_words is None):
            return self.weight_word_length(text, *args, **tfidfargs)
        
        # build weights (longer words weighted more)
        words_df = self.weight_word_length(text, *args, **tfidfargs)

        weights = pd.Series(
            [
                any(y == words_df['words'][x]
                for y in self.important_words)

                for x in words_df.index
            ], index=words_df.index
        )
        
        # and normalizing later
        # weights *= self.important_weight / max(weights)
        weights *= self.important_weight

        words_df['important_weight'] = weights

        return words_df
            

    def combine_weights(self, text=None, *args, **tfidfargs):
        ''' merge the weighted params into the segments
        
        :returns: a df with all of the parameters combined into the segments
        weights. Also, renormalized.
        '''
            
        words_df = self.weight_important_words(text, *args, **tfidfargs)

        words_df['sum'] = words_df.drop(
            'words', axis=1).sum(axis=1)

        # segments are given number col names
        segs = words_df[[x for x in range(self.chunks)]]

        # if not seg or 'words'... must be param
        params = words_df.drop(list(segs.columns) + ['words'], axis=1)

        # must be product to avoid making 0 --> !0
        weights = words_df[list(params.columns)].sum(axis=1)

        # specify the axis or things break
        words_df[list(segs.columns)] = \
            words_df[list(segs.columns)].multiply(weights, axis=0)


        # and lastly, normalizing everything
        words_df[list(segs.columns) + ['sum']] /= \
            words_df[list(segs.columns) + ['sum']].max(axis=0)


        return words_df

    def filter_data(self, text=None, *args, **tfidfargs):
        ''' Drop out words with weights below the cutoff

        :returns: a df without unimportant words
        '''
            
        # filter out unimportant words
        words_df = self.combine_weights(text, *args, **tfidfargs) 

        # use full meeting normalized weight to clip
        # this could also be done by using Tf_Idf's min_df and max_df
        words_df = words_df[
            (words_df['sum'] <= self.maximum) &
            (words_df['sum'] >= self.minimum)]
        
        return words_df
        

    def summarize_words(self, text=None, *args, **tfidfargs):
        '''Format and return the words
        :text: typically self.text

        :returns: a df with the most important words from each segment -- note
        that the weights are used to generate this df but dropped before
        presenting it
        '''
        words_df = self.filter_data(text, *args, **tfidfargs)
        results_df = pd.DataFrame()

        # IE for every chunk
        for x in range(self.chunks):
            results = words_df.sort_values(x, ascending=False)['words']
            results = results.reset_index(drop=True)

            results_df[x] = results

        # only hold the required number of words
        results_df = results_df[:self.num_words]

        return results_df
    
    def summarize_sentences(self, text=None, *args, **tfidfargs):
        '''Format and return the sentences
        :text: typically self.text

        :returns: a df with the most important sentences from each segment -- note
        that the weights are used to generate this df but dropped before
        presenting it
        '''

        if text is None:
            text = self.text

        words_df = self.combine_weights(text, *args, **tfidfargs)
        sentences_df = self.build_sentences(text, *args, **tfidfargs)


        # IE for sentence 0 being "The quick brown fox"
        # sentence 1 being "jumps over the lazy dog"
        # only 1 chunk
        # & words being [the, quick, brown, fox, jumps, over, lazy, dog]
        # then we would get back

        # [0, 2, 3, 4, 5, 6, 7]
        for word_index in words_df.index.values:
            
            # for the first chunk, [0]
            for chunk_number in range(self.chunks):
                # consider word 0 --> it is "the"
                # [true, true]
                sentence_has_word = sentences_df.loc[ 
                    sentences_df['segIndex'] == chunk_number,  
                    ('sentences')].str.contains(words_df.loc[word_index, 'words'])
                
                # IE weight of "the" would be .032
                word_weight = words_df.loc[word_index, chunk_number]
                
                # [.032, .032]
                sentence_weight = word_weight * sentence_has_word
                
                # [.032, .032] and then loop again with "quick"
                sentences_df.loc[sentences_df['segIndex'] == chunk_number, 
                    'weight'] += sentence_weight
        

        
        
        # return the sentences in the order that they appeared
        for chunk_number in range(self.chunks):

            sentences_df = sentences_df.drop(
                sentences_df.loc[sentences_df['segIndex'] == chunk_number].sort_values(
                    'weight', ascending=False)[self.num_sentences:].index
            )

        return sentences_df
        
    def summarize(self, text=None, *args, **tfidfargs):
        '''Do everything all at once. Usually a good option.

        :text: could be self.text or any arbitrary string list

        :returns: a tuple of df's containing (words, sentences)
        '''
            
        word_summary = self.summarize_words(text)
        sentence_summary = self.summarize_sentences(text)
        
        
        return word_summary, sentence_summary
        
