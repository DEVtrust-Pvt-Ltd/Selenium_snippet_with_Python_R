# Importing required dependencies
import time
import pandas as pd
import os
import pickle
import undetected_chromedriver as uc
from Team_transaction import Team_transaction
from reservations import Reservation
import yaml

credentials = yaml.load(open('./credentials.yml','r'),Loader=yaml.FullLoader)

def load_data(pkl_file):
    Reservation(pkl_file)
    path=os.getcwd()
    directory="Reservations_csv"
    path1=os.path.join(path,directory)
    file = os.listdir(directory)
    path2=os.path.join(path1,file[0])
    df=pd.read_csv(path2)
    cnf_code=list(df['Confirmation code'])

    options = uc.ChromeOptions()
    options.headless=True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get('https://www.air.co.in/login')
    ################################################## Loading cookies through pickle file and adding it to driver #########################################################################
    cookies = pickle.load(open(pkl_file, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    ########################################################################## Data Extraction #############################################################################################
    try:
        driver.maximize_window()
        ls=[]
        for i in cnf_code:
            time.sleep(10)
            driver.get(f'https://www.air.co.in/hosting/reservations/details/{i}?confirmationCode={i}&print=true')
            time.sleep(20)
            dic={}

            ############################################################################## Guest payouts ###################################################################################
            
            try:
                listings=driver.find_element("xpath","//div[@class='_zdxht7']/child::div[@class='_1yl0x8a']").text
            except:
                listings=''
           
            try:
                no_guest=driver.find_element("xpath","//div[@class='_zdxht7']/child::div[@class='_1yl0x8a']/child::span[@class='ll4r2nl dir dir-ltr']").text.split('\n')[1].split('guest')[0]
            except:
                no_guest=''
            
            try:
                guest_stay_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_GUEST_PAYIN_LINE_ITEM_1']/child::div/child::div[@class='_12kj5um']/child::span").text
            except:
                guest_stay_total='$0'
            
            try:
                guest_cleaning_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_GUEST_PAYIN_LINE_ITEM_2']/child::div/child::div[@class='_12kj5um']/child::span").text
            except:
                 guest_cleaning_total='$0'
           
            try:
                guest_service_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_GUEST_PAYIN_LINE_ITEM_3']/child::div/child::div[@class='_12kj5um']/child::span").text
            except:
                guest_service_total='$0'
           
            try:
                guest_occupancy_taxes_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_GUEST_PAYIN_LINE_ITEM_4']/child::div/child::div[@class='_12kj5um']/child::span").text
            except:
                guest_occupancy_taxes_total='$0'
            
            try:
                guest_gross_bill_cost=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_GUEST_PAYIN_TOTAL']/child::div/child::div[@class='_12kj5um']/child::span").text
            except:
                guest_gross_bill_cost='$0'
            

        ################################################################################### Host payouts ###############################################################################################

            try:
                host_stay_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_HOST_PAYOUT_LINE_ITEM_1']/child::div/child::div[@class='_12kj5um']/child::span[@class='_11ry7lz']").text
            except:
                host_stay_total='$0'
            
            try:
                host_service_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_HOST_PAYOUT_LINE_ITEM_3']/child::div/child::div[@class='_12kj5um']/child::span[@class='_11ry7lz']").text[1:]
            except:
                host_service_total='$0'
           
            try:
                host_gross_total=driver.find_element("xpath","//div[@data-plugin-in-point-id='PAYMENT_HOST_PAYOUT_TOTAL']/child::div/child::div[@class='_12kj5um']/child::span[@class='_11ry7lz']").text
            except:
                host_gross_total='$0'
            
        
            dic['listing']=listings
            dic['number_of_guest']=no_guest
            dic['guest_room_fee']=guest_stay_total
            dic['guest_cleaning_fee']=guest_cleaning_total
            dic['guest_service_fee']=guest_service_total
            dic['guest_occupancy_taxes_cost']=guest_occupancy_taxes_total
            dic['guest_total_cost']=guest_gross_bill_cost
            dic['host_room_cost']=host_stay_total
            dic['host_service_fee']=host_service_total
            # dic['host_resort_fee']=host_resort_fee
            dic['host_total_cost']=host_gross_total

            ls.append(dic)

        data=pd.DataFrame(ls)
        data1=pd.concat([df,data],axis=1)

        team_directory='Team_transactions'
        team_local=os.getcwd()
        team_path_local=os.path.join(team_local,team_directory)
        team_path_local=[os.path.join(team_path_local,i) for i in os.listdir('Team_transactions')]
        df1=pd.read_csv(team_path_local[0])
        df1=df1[df1['Type']=='Reservation']
        df1=df1.reset_index()
        df1=df1[['Confirmation Code','air Account ID','Resort fee']]
        df1.rename(columns={'Confirmation Code':'confirmation_code','air Account ID':'air_account_id','Resort fee':'host_resort_fee'},inplace=True)

        data1=data1.drop(columns=['Listing','# of adults','# of children','# of infants','Contact'])
        data1.rename(columns={'Confirmation code':'confirmation_code','Status':'status','Guest name':'guest_name','Start date':'check_in',
        'End date':'checkout','# of nights':'total_nights','Booked':'booking_date','Listing':'listing','Earnings':'earnings'},inplace=True)
        data2=pd.merge(data1,df1,on='confirmation_code',how='left')
        return data2
        
    
    except:
        print('Runtime error')


if __name__=='__main__':
    pkl_file= credentials['user_cookies']['cookies_user1']
    Team_transaction(pkl_file)
    Reservation(pkl_file)
    load_data(pkl_file)


