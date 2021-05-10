import pandas as pd
import requests

from schedule import every, repeat, run_pending
import time


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
    
    return 0


while True:
    run_pending()
    time.sleep(1)
    