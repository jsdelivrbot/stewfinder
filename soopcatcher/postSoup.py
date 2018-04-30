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
    startNum=26477,
    endNum=26485,
)


bozeMag = soopProcess.processor(
    baseUrl='http://bozemanmagazine.com/events',
    linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
    urlType='crawled',
    today=True,
    important_weight=100,
    num_sentences=2

)


msuData = msu.process()

bozeMagData = bozeMag.process()

# msuData.append(otherData).reset_index(drop=True)
allData = msuData.append(bozeMagData).reset_index(drop=True)
print(allData.details)

DATA = allData.to_dict('index')

with requests.session() as client:
    for row in DATA:
        client.post(
            ROOT_URL + '/api/soops/',
            data=DATA[row],
            headers= {'Authorization': AUTH_STR}
        )
