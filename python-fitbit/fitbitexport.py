# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 20:18:23 2018

@author: lina9
"""

import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
CLIENT_ID = '22D8PQ'
CLIENT_SECRET = '372683b0cf55de775fb181a4d85bd849'
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))
fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=yesterday2, detail_level='1sec')
time_list = []
val_list = []
for i in fit_statsHR['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])
heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})
heartdf.to_csv('C:/Users/lina9/Anaconda2/Scripts/python-fitbit/Heart/heart'+ \
               yesterday+'.csv', \
               columns=['Time','Heart Rate'], header=True, \
               index = False)
fit_statsSl = auth2_client.sleep(date='today')
stime_list = []
sval_list = []
for i in fit_statsSl['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
fit_statsSum = auth2_client.sleep(date='today')['sleep'][0]
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list,
					 'Date':fit_statsSum['dateOfSleep'],
					 'MainSleep':fit_statsSum['isMainSleep'],
					 'Efficiency':fit_statsSum['efficiency'],
					 'Duration':fit_statsSum['duration'],
					 'Minutes Asleep':fit_statsSum['minutesAsleep'],
					 'Minutes Awake':fit_statsSum['minutesAwake'],
					 'Awakenings':fit_statsSum['awakeCount'],
					 'Restless Count':fit_statsSum['restlessCount'],
					 'Restless Duration':fit_statsSum['restlessDuration'],
					 'Time in Bed':fit_statsSum['timeInBed']})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
sleepdf.to_csv('C:/Users/lina9/Anaconda2/Scripts/python-fitbit/Sleep/sleep' + \
               today+'.csv', \
               columns = ['Time','State','Date','MainSleep','Efficiency','Duration','Minutes Asleep','Minutes Awake','Awakenings','Restless Count','Restless Duration','Time in Bed','Interpreted'],header=True, 
               index = False)