import requests

from schedule import every, repeat, run_pending
import time

import pandas as pd

from dynamo_pandas import put_df, get_df, keys
import boto3


times_pulled = 0
times_max = 60

id = 0

@repeat(every().minute.at(":10"))
def pull():
    r = requests.get('https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi')
    
    global times_pulled, id

    id+=1
    
    factor = r.json()['factor']
    pi = r.json()['pi']
    time = r.json()['time']
    
    d = {'ID' : [id], 'factor': [factor], 'pi' : [pi], 'time': [time]}
    
    df = pd.DataFrame(data=d, index=[id])
    
    print(df)
    
    put_df(df, table="DS3002_Project2")
    
    times_pulled+=1
    
    return 0


while times_pulled < times_max:
    run_pending()

    