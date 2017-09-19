import numpy as np
import matplotlib.pylab as plt
import pandas as pd

from config import BLOCKED_VALENCE_RANGE

labmt = pd.read_csv('labMT.txt', sep='\t')
happiness_dict = { word:v for word, v in zip(labmt.word, labmt.happiness_average)
                   if v <= BLOCKED_VALENCE_RANGE[0] or v >= BLOCKED_VALENCE_RANGE[1] }

def map_happiness_vals(d):
    if isinstance(d,dict):
        r = []
        for k,v in d.items():
            h = happiness_dict.get(k, None)
            if h is not None:
                r += [h,]*v
        if len(r) == 0:
            return None
        else:
            return r

import itertools
import scipy.stats

def get_sentiment_df(lyric_df, grp_col):
    def f(grp):
        r = [v for l in grp.happiness_values.tolist() for v in l]
        if len(r):
            return np.array(r)
        else:
            return None

    r = lyric_df.groupby(grp_col).apply(f)
    r = r.dropna()
    return r 

def get_sentiment_values(lyric_df, grp_col):
    r = get_sentiment_df(lyric_df, grp_col)
    return r.apply(np.mean), r.apply(scipy.stats.sem) 


def get_allwords_df(lyrics_df):
    print("Creating words dataframe (this will take a while)")
    def f():
        for index, row in lyrics_df.iterrows():
            for k, v in row.WordCount.items():
                h = happiness_dict.get(k, None)
                if h is not None:
                    yield from [[index, k, h],]*v
    allwords = list(f())
    allwords_df = pd.DataFrame.from_records(allwords, columns=['chordIx','word','happiness'])
    allwords_df['word'] = allwords_df.word.astype('category')
    allwords_df = allwords_df.merge(lyrics_df, 'left', left_on='chordIx', right_index=True)
    print("Done")
    return allwords_df


def get_most_popular(metadata_df, plot_col, K=None, CUTOFF=500):
    vcounts = metadata_df[plot_col].value_counts()
    if K is not None:
        most_popular = vcounts.iloc[0:K].index.values
    else:
        most_popular = vcounts[vcounts>CUTOFF].index.values
    return most_popular

