import os
import time

import requests

import soopProcess
import soopPull

ROOT_URL = os.environ.get('SOOP_URL')
AUTH_STR = os.environ.get('SOOP_AUTH')

# to do a day that's not today
# tmrw = datetime.today() + timedelta(days=1)
# tmrwFormatted = datetime.strftime(tmrw, '%Y/%m/%d')

# not really sure how this happened.... it shouldn't be this
# bozeMag = soopProcess.processor(
    # baseUrl='http://bozemanmagazine.com/events',
    # linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
    # urlType='crawled',
    # today=True,
# )

bozeMag = soopProcess.processor(
    baseUrl='http://bozemanmagazine.com/events/calendar/' + time.strftime('%Y/%m/%d'),
    linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
    urlType='crawled',
    linkBase='http://bozemanmagazine.com/events',
    today=True,
)


bozeMagData = bozeMag.process(
    whenTag='p',
    whenClass='date',
    descTag='div',
    descClass='description',
    important_weight=100,
    num_sentences=2
)

allData = bozeMagData
allData.outUrl.to_csv('data.csv')

DATA = allData.to_dict('index')

with requests.session() as client:
    for row in DATA:
        client.post(
            ROOT_URL + '/api/soops/',
            data=DATA[row],
            headers={'Authorization': AUTH_STR}
        )
