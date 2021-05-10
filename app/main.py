import requests

from schedule import every, repeat, run_pending
import time

import pandas as pd

from dynamo_pandas import put_df, get_df, keys
import boto3

# Checker variables for scheduling
times_pulled = 0
times_max = 60

# Refers to the ID for minutes in DynamoDB
id = 0

# schedule library executes exactly when time is 10 seconds per each minute
@repeat(every().minute.at(":10"))
def pull():
    # requests library function to pull from the given API 
    r = requests.get('https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi')
    
    # Ensures that the values can be checked outside of function
    global times_pulled, id

    # ID minute count (1-60)
    id+=1
    
    # Extract JSON from API response and parse
    factor = r.json()['factor']
    pi = r.json()['pi']
    time = r.json()['time']
    
    d = {'ID' : [id], 'factor': [factor], 'pi' : [pi], 'time': [time]}
    
    # Create a pandas dataframe for easy DynamoDB inserts
    df = pd.DataFrame(data=d, index=[id])
    
    # Check functionality while running
    print(df)
    
    # dynamo-pandas library easy insert from pandas dataframe
    put_df(df, table="DS3002_Project2")
    
    # iterate to ensure while loop ends
    times_pulled+=1
    
    return 0

# Ensures the loop ends exactly by 60 minute mark 
while times_pulled < times_max:
    run_pending()

    