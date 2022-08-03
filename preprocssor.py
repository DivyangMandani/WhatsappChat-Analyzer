import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    msg=re.split(pattern,data)[1:]
    date=re.findall(pattern,data)

    data=pd.DataFrame({'message':msg,'date_time':date})
    data['date']=data['date_time'].str.split(',').str.get(0)
    data['time']=data['date_time'].str.split(',').str.get(1).str.split(' ').str.get(1)
    #data['timezone']=data['date_time'].str.split(',').str.get(1).str.split(' ').str.get(2)


    data['date']=pd.to_datetime(data['date'])
    data['time']=pd.to_datetime(data['time'])
    
    data.drop('date_time',axis=1,inplace=True)


    users=[]
    msge=[]

    for msg in data['message']:
        entry=re.split('([\w\W]+?):\s',msg)
        
        if entry[1:]:
            users.append(entry[1])
            msge.append(entry[2])
        else:
            users.append('Group Notification')
            msge.append(entry[0])

    data['user']=users
    data['msg']=msge
    data.drop('message',axis=1,inplace=True)
    data['year']=data['date'].dt.year
    data['month']=data['date'].dt.month_name()
    data['only_date']=data['date']
    data['date']=data['date'].dt.day
    data['month_num']=data['time'].dt.month
    data['minute']=data['time'].dt.minute
    data['hour']=data['time'].dt.hour
    data['day_name'] = data['only_date'].dt.day_name()
    data.drop(columns=['time'],inplace=True)
    
    period = []
    for hour in data[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    data['period'] = period

    return data
