import traceback
import pandas as pd
import requests
import json
import os
class DataGen:
    def cricket_api_data_live_matches(self):
        # response=requests.get('https://api.cricapi.com/v1/currentMatches?apikey=c415b5df-c28a-412f-ab7c-c40ba0e4c224&offset=0')
        # if response.status_code==200:
        #     data=(response.json())
        f = open(os.path.join('data','data.json'))
        data = json.load(f)
        df=pd.DataFrame(columns=['Match','Vanue','Match Type','Status'])
        matchArr=[]
        vanueArr=[]
        typeArr=[]
        statusArr=[]
        for k in data['data']:
                try:
                    a,b,c=k['name'],k['venue'],k['matchType']
                    matchArr.append(k['name'])
                    vanueArr.append(k['venue'])
                    typeArr.append(k['matchType'])
                    if k['matchStarted']==True and k['matchEnded']==True:
                         statusArr.append('Finished')
                    elif k['matchStarted']==True and k['matchEnded']==False:
                         statusArr.append('Live') 
                    else:
                         statusArr.append('Upcoming')
                except:
                     traceback.print_exc()
                     continue
        df['Match']=matchArr
        df['Vanue']=vanueArr
        df['Match Type']=typeArr
        df['Status']=statusArr
        # print(df)
        return df
        



