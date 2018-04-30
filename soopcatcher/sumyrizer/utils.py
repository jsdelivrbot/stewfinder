
# coding: utf-8

# In[1]:


from string import punctuation
from bs4 import BeautifulSoup
from math import ceil

import pandas as pd
import requests

# In[2]:


# keep periods for sentence parsing
punct = {'!': ' ',
         '"': ' ',
         ',': ' ',
         '#': ' ',
         '$': ' ',
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
         '-': '',}

punctuator = str.maketrans(punct)


def print_full(x):
    '''
    print all rows in a Df
    '''
    pd.set_option('display.max_rows', len(x))
    display(x)
    pd.reset_option('display.max_rows')


def str_chunks(l, n):
    """Yield n successive chunks from l."""
    for i in range(0, len(l), ceil(len(l) / n)):
        yield ' '.join(l[i:i + ceil(len(l) / n)].split())


def list_chunks(l, n):
    """Yield n successive chunks from l."""
    for i in range(0, len(l), ceil(len(l) / n)):
        yield ' '.join(l[i:i + ceil(len(l) / n)])


def least_squares(x, y, n):
        sq = (1 / n) * ((x - y)**2)
        return sq

# In[3]:

def get_text_from_file(filepath, chunks=None):
    if chunks is None:
        with open(filepath, "r") as infile:
            text = infile.read()
            return text.translate(punctuator)
        
    with open(filepath) as infile:
        text = infile.read().splitlines()
        text = [x.translate(punctuator) for x in text]
        text = [x for x in list_chunks(text, chunks)]
        return text


def get_text_from_url(url, chunks=None):
    '''This method will retrive the text from a url
    :url: a url path from which to read and strip tags

    If you find that it carries a lot of html tags, then
    inspect the element and add it to the list of extracted
    tags. If you only wish to remove a certain class of an
    element, follow the example with div.hidden-print
    '''

    # request and read the url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    # throw out the bad tags
    [s.extract() for s in soup(
        ['pre', 'style', 'script', 'nav', '[document]',
         'head', 'title'])]

    # throw out the bad classes

    for div in soup.find_all("div", {'class':'hidden-print'}):
        div.decompose()

    # get the text that's left
    text = soup.get_text().translate(punctuator)

    if chunks is not None:
        text = [x for x in str_chunks(text, chunks)]

    return text


def pretty_print(df, col=None, *args, **kwargs):
    if col is None:
        outline = ' '.join(df)
        print('please select a colum: ', outline)
        return outline

    outline = ' '.join(df[col])
    print(outline, *args, **kwargs)
    return outline


def true_mean(startCol, endCol, df):
    valSum = df.values[:, startCol:endCol+1].sum()  
    valCount = (df.values[:, startCol:endCol+1] != 0).sum()
    return valSum / valCount


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', 9999)
    display(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
