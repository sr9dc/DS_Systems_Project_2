import pandas as pd
import requests

import schedule
import time


times_pulled = 0
times_max = 60

id = 0

def pull():
    r = requests.get('https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi')
    
    global times_pulled, id

    id+=1
    
    factor = r.json(['factor'])
    
    d = {'ID' : [id], 'factor': [1, 2], 'col2': [3, 4]}
    
    