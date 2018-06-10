import time
import requests
import soopProcess
import soopPull

# this will change for sure
ROOT_URL = "http://127.0.0.1:8000"

# put this in env variable pls
AUTH_STR = "Token 4847d6ca5fb338bd0f35531c4609a0d1bf67b5a6"



msu = soopProcess.processor(
    'http://calendar.msu.montana.edu/events/',
    startNum=26500,
    endNum=26505,
    urlType='numbered',
)


bozeMag = soopProcess.processor(
    baseUrl='http://bozemanmagazine.com/events',
    linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
    urlType='crawled',
    today=True,
)

msuData = msu.process(
    whenTag='dd',
    locationTag='dd',
    locationRegex='^(?!.*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))',
    descTag='main',
    descClass='col-sm-8',
    important_weight=100,
    num_sentences=2
)

bozeMagData = bozeMag.process(
    whenTag='p',
    whenClass='date',
    descTag='div',
    descClass='description',
    # locationTag='address',
    # locationClass='location_text',
    important_weight=100,
    num_sentences=2
)

# msuData.append(otherData).reset_index(drop=True)
allData = msuData.append(bozeMagData).reset_index(drop=True)
# allData.to_csv('data.csv')

DATA = allData.to_dict('index')

with requests.session() as client:
    for row in DATA:
        client.post(
            ROOT_URL + '/api/soops/',
            data=DATA[row],
            headers= {'Authorization': AUTH_STR}
        )
