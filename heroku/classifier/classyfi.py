import os

import numpy as np
import pandas as pd
import psycopg2
import tensorflow as tf
import tensorflow_hub as hub

"""
this is a simple deep neural net model that uses predefined estimators in order
to predict whether an event will be desirable. At the moment it will converge
to roughly 80% accuracy... to get up to 90%, I'll probably have to build my own
estimator


for more info, see tensorflow/simple_tf_hub.py
"""

# first import the data get credentials in .env
dbname = os.getenv('dbname')
port = os.getenv('dbport')
username = os.getenv('dbuser')
password = os.getenv('dbpw')
host = os.getenv('dbhost')

# open a connection to the db
conn = psycopg2.connect(
    dbname=dbname,
    user=username,
    password=password,
    host=host,
    port=port
)

# pull in the data that contains votes
print('importing data...')
cur = conn.cursor()
cur.execute('SELECT * FROM soops_soop WHERE vote_score != 0')
columns = [colname[0] for colname in cur.description]
soops = cur.fetchall()
cur.close()


data = pd.DataFrame(soops, columns=columns)

# assign a polarity: 1 for events with a positive # of likes
# and 0 for events with a negative # of likes
data = data.assign(
    polarity=data.loc[:, 'vote_score']
    .apply(lambda x: int(x > 0))
)

# perform a random train/test split
print('splitting into train/test')
msk = np.random.randn(len(data)) < .8

train_df = data[msk]
train_df = train_df.loc[:, ['details', 'polarity']]

test_df = data[~msk]
test_df = test_df.loc[:, ['details', 'polarity']]


# train on whole set with no limit on training epochs
print('training on ', len(train_df), ' rows')
print('testing on ', len(test_df), ' rows')
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
    key='details',
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
