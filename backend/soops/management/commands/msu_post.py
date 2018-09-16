from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

import time
import requests
from soops.management.commands import soopProcess
from soops.management.commands import soopPull

# this will change for sure
ROOT_URL = "http://stewfinder-backend.us-west-2.elasticbeanstalk.com"

# put this in env variable pls
AUTH_STR = "Token 1eefcbd33b05b8c56182ae2f953bdd7a33f367b4"


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        msu = soopProcess.processor(
            'http://calendar.msu.montana.edu/events/',
            startNum=26400,
            endNum=264-5,
            urlType='numbered',
            important_weight=100,
            num_sentences=2
        )


        # bozeMag = soopProcess.processor(
            # baseUrl='http://bozemanmagazine.com/events',
            # linkRegex='/' + time.strftime('%Y/%m/%d') + '.*',
            # urlType='crawled',
            # today=True,
            # important_weight=100,
            # num_sentences=2

        # )


        msuData = msu.process()

        # bozeMagData = bozeMag.process()

        # msuData.append(otherData).reset_index(drop=True)
        # allData = msuData.append(bozeMagData).reset_index(drop=True)
        allData = msuData

        DATA = allData.to_dict('index')

        with requests.session() as client:
            for row in DATA:
                client.post(
                    ROOT_URL + '/api/soops/',
                    data=DATA[row],
                    headers= {'Authorization': AUTH_STR}
                )
