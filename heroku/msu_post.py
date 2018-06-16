import os
import time

import requests

import soopProcess
import soopPull

ROOT_URL = os.environ.get('SOOP_URL')
AUTH_STR = os.environ.get('SOOP_AUTH')


# for prod
startNum = 23500
endNum = 30100

# this has the goat raising event for testing
# startNum = 26500
# endNum = 26510

numList = list(range(startNum, endNum, 3))

for indx, val in enumerate(numList):
    curStart = numList[indx - 1]
    curEnd = numList[indx]

    msu = soopProcess.processor(
        'http://calendar.msu.montana.edu/events/',
        startNum=curStart,
        endNum=curEnd,
        urlType='numbered',
    )

    msuData = msu.process(
        whenTag='dd',
        descTag='main',
        descClass='col-sm-8',
        important_weight=100,
        num_sentences=2
    )

    allData = msuData
    allData.outUrl.to_csv('data.csv')

    DATA = allData.to_dict('index')

    with requests.session() as client:
        for row in DATA:
            client.post(
                ROOT_URL + '/api/soops/',
                data=DATA[row],
                headers={'Authorization': AUTH_STR}
            )


# msu = soopProcess.processor(
# 'http://calendar.msu.montana.edu/events/',
# startNum=23500,
# endNum=30005,
# urlType='numbered',
# )


# bozeMag = soopProcess.processor(
# baseUrl='http://bozemanmagazine.com/events',
# linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
# urlType='crawled',
# today=True,
# )


# bozeMag = soopProcess.processor(
# baseUrl='http://bozemanmagazine.com/events',
# linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
# urlType='crawled',
# today=True,
# important_weight=100,
# num_sentences=2

# )

# bozeMagData = bozeMag.process(
# important_weight=100,
# num_sentences=2
# )

# msuData.append(otherData).reset_index(drop=True)
# allData = msuData.append(bozeMagData).reset_index(drop=True)
