import os
import time
from datetime import datetime, timedelta

import requests

import soopProcess
import soopPull

ROOT_URL = os.environ.get('SOOP_URL')
AUTH_STR = os.environ.get('SOOP_AUTH')

# to do a day that's not today
tmrw = datetime.today() + timedelta(days=2)
tmrwFormatted = datetime.strftime(tmrw, '%Y/%m/%d')
eventDay = datetime.strftime(tmrw, '%-m/%-d/%Y')

bozeMag = soopProcess.processor(
    baseUrl='http://bozemanmagazine.com/events/calendar/' + tmrwFormatted,
    linkRegex='/' + tmrwFormatted + '.*',
    urlType='crawled',
    linkBase='http://bozemanmagazine.com/events',
    day=eventDay,
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
allData.outUrl.to_csv('bozemag2tmrw.csv')

DATA = allData.to_dict('index')

with requests.session() as client:
    for row in DATA:
        client.post(
            ROOT_URL + '/api/soops/',
            data=DATA[row],
            headers={'Authorization': AUTH_STR}
        )
