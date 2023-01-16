# Import required dependencies
from Team_transaction import Team_transaction
from reservations import Reservation
from reservations_scrape import load_data
import os
import boto3
from io import StringIO
import pandas as pd
from datetime import datetime
import glob2
import yaml

############################################ loading .yml file for importing credentials ###########################################
credentials = yaml.load(open('./credentials.yml','r'),Loader=yaml.FullLoader)

def clean_dir():
    
    directory_name='Reservations_csv\*'
    local=os.getcwd()
    path_local=os.path.join(local,directory_name)
    files = glob2.glob(path_local)
    for file in files:
        os.remove(file)

def clean_dir1():
    
    directory_name='Team_transactions\*'
    local=os.getcwd()
    path_local=os.path.join(local,directory_name)
    files = glob2.glob(path_local)
    for file in files:
        os.remove(file)

def account_id():

    team_directory='Team_transactions'
    team_local=os.getcwd()
    team_path_local=os.path.join(team_local,team_directory)
    team_path_local=[os.path.join(team_path_local,i) for i in os.listdir('Team_transactions')]
    df1=pd.read_csv(team_path_local[0])
    account_id=str(df1['Airbnb Account ID'].iloc[0])
    return account_id

######################## Creating Session With Boto3 #########################################

def reservation_dump(pkl_file):

    Reservation(pkl_file)
    current_time=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    if len(os.listdir("Reservations_csv"))== 0:
        
        session = boto3.Session(
        aws_access_key_id=credentials['aws_credentials']['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_credentials']['aws_secret_access_key']
        )
    
        s3_res = session.resource('s3')
        csv_buffer = StringIO()
        bucket_name = credentials['aws_credentials']['bucket_name']
        df=load_data(pkl_file)
        df.to_csv(csv_buffer,index=False,sep="|")
        s3_res.Object(bucket_name,account_id()+'_reservations_'+current_time+'.csv').put(Body=csv_buffer.getvalue())
    
    else:
        
        session = boto3.Session(
        aws_access_key_id=credentials['aws_credentials']['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_credentials']['aws_secret_access_key']
        )

        s3_res = session.resource('s3')
        csv_buffer = StringIO()
        bucket_name = credentials['aws_credentials']['bucket_name']
        df=load_data(pkl_file)
        df.to_csv(csv_buffer,index=False,sep="|")
        s3_res.Object(bucket_name,account_id()+'_reservations_'+current_time+'.csv').put(Body=csv_buffer.getvalue())



if __name__=='__main__':
    pkl_file= credentials['user_cookies']['cookies_user1']
    Team_transaction(pkl_file)
    reservation_dump(pkl_file)
    clean_dir1()
    