import os
import re

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import seaborn as sns
import tensorflow as tf
import tensorflow_hub as hub


def load_dir_data(directory):
    """load files from a directory into df

    :directory: path to dir that will be pulled
    :returns: df of the labelled data

    """
    data = {}
    data['sentence'] = []
    data['sentiment'] = []

    for file_path in os.listdir(directory):
        with tf.gfile.GFile(os.path.join(directory, file_path), 'r') as f:
            data['sentence'].append(f.read())

            # this pulls the first parenthesized subgroup IE the sentiment
            data['sentiment'].append(re.match("\d+_(\d+)\.txt",
                                              file_path).group(1))

    return pd.DataFrame.from_dict(data)


def load_dataset(directory):
    """merge positiv and negative examples, add polarity col & shuffle

    :directory: TODO
    :returns: TODO

    """
    pos_df = load_dir_data(os.path.join(directory, 'pos'))
    neg_df = load_dir_data(os.path.join(directory, 'neg'))

    pos_df['polarity'] = 1
    neg_df['polarity'] = 0

    return pd.concat([pos_df, neg_df]).sample(frac=1).reset_index(drop=True)


def download_and_load_datasets(force_download=False):
    """downloads and processes the files

    :force_download: TODO
    :returns: TODO

    """

    dataset = tf.keras.utils.get_file(
        fname="aclImdb.tar.gz",
        origin="http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz",
        extract=True
    )

    train_df = load_dataset(
        os.path.join(
            os.path.dirname(dataset),
            "aclImdb",
            "train"))

    test_df = load_dataset(
        os.path.join(
            os.path.dirname(dataset),
            "aclImdb",
            "test"))

    return train_df, test_df


# reduce the logging output
tf.logging.set_verbosity(tf.logging.ERROR)


# load the data into a format that doesn't suck
train_df, test_df = download_and_load_datasets()
print(train_df.head())


# train on whole set with no limit on training epochs
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=train_df,
    y=train_df['polarity'],
    num_epochs=None,
    shuffle=True
)

# predict on whole training set
predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df,
    train_df['polarity'],
    shuffle=False
)

# also will predict on the entire testing set
predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
    test_df,
    test_df['polarity'],
    shuffle=False
)

# turn the text into a feature column of words
embedded_text_feature_column = hub.text_embedding_column(
    key='sentence',
    module_spec='https://tfhub.dev/google/nnlm-en-dim128/1'
)

# use a deep neural net classifier
estimator = tf.estimator.DNNClassifier(
    hidden_units=[500, 100],
    feature_columns=[embedded_text_feature_column],
    n_classes=2,
    optimizer=tf.train.AdagradOptimizer(learning_rate=.003)
)


# default batch size is 128, so 128,000 training samples.. ~5 epochs
estimator.train(input_fn=train_input_fn, steps=1000)

train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)

print("Training set accuracy: {accuracy}".format(**train_eval_result))
print("Test set accuracy: {accuracy}".format(**test_eval_result))


'''
this model will achieve 75-80% accuracy on the testing set.. that's not bad but
it could be improved with transfer learning. For more info, see this site:
https://www.tensorflow.org/tutorials/text_classification_with_tf_hub

it includes an example of how to retrain the nnlm-en-dim128 module in order to
get the testing set accuracy up to almost 90%
'''
