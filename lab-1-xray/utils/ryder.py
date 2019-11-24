import requests
import random
import os
import time
import sys

mysfits = [
            '0e37d916-f960-4772-a25a-01b762b5c1bd',
            '2b473002-36f8-4b87-954e-9a377e0ccbec',
            '33e1fbd4-2fd8-45fb-a42f-f92551694506',
            '3f0f196c-4a7b-43af-9e29-6522a715342d',
            '4e53920c-505a-4a90-a694-b9300791f0ae',
            'a68db521-c031-44c7-b5ef-bfa4c0850e2a',
            'a901bb08-1985-42f5-bb77-27439ac14300',
            'ac3e95f3-eb40-4e4e-a605-9fdd0224877c',
            'b41ff031-141e-4a8d-bb56-158a22bea0b3',
            'b6d16e02-6aeb-413c-b457-321151bb403d',
            'c0684344-1eb7-40e7-b334-06d25ac9268c',
            'da5303ae-5aba-495c-b5d6-eb5c4a66b941'
]

if 'ENDPOINT' in os.environ:
    x = os.environ['ENDPOINT']    
elif (sys.version_info > (3,0)):
    x = input("Enter an ENDPOINT:PORT combination [port is optional]: ")
else: 
    x = raw_input("Enter an ENDPOINT:PORT combination [port is optional]: ")

if (x.startswith('http')):
    URL = x
else:
    URL = "http://"+x

for n in range(1200):
    r = requests.post(URL+"/mysfits/%s/like" % mysfits[random.randint(0,11)])
    print("Request %s returned: %s" % (n,r))
    time.sleep(0.20)
