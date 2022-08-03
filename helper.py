from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import seaborn as sns

def number_msg(selected_user,df):

    if selected_user=='Overall':
        number_msg=df.shape[0]

        return number_msg

    else:
        number_msg=df[df['user']==selected_user].shape[0]

        return  number_msg   

def number_words(selected_user,df):

    if selected_user=='Overall':

        words=[]
        for i in df['msg']:
            words.extend(i.split())
        
        return len(words)

    else:
        words=[]
        for i in df[df['user']==selected_user]['msg']:
            words.extend(i.split())
        
        return len(words)  

def media(selected_user,df):
    if selected_user=='Overall':
        return df[df['msg']=='<Media omitted>\n'].shape[0]

    else:
        return df[df['user']==selected_user][df['msg']=='<Media omitted>\n'].shape[0]    

def links(selected_user,df):
    extractor=URLExtract()
    if selected_user=='Overall':
        links=[]
        for i in df['msg']:
            links.extend(extractor.find_urls(i))

        return len(links)

    else:
        links=[]
        for i in df[df['user']==selected_user]['msg']:
            links.extend(extractor.find_urls(i))

    return len(links)       

def most_busy_user(df):
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'user','user':'Percentage'})

    return df['user'].value_counts().head(5),new_df

def create_wordcloud(selected_user,df):
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    if selected_user=='Overall':
        df_wc=wc.generate(df['msg'].str.cat(sep=" "))

        return df_wc

    else:
        df_wc=wc.generate(df[df['user']==selected_user]['msg'].str.cat(sep=" "))

        return df_wc

def most_words(selected_user,df):
    if selected_user=='Overall':
        temp=df[df['user']!='Group Notification']
        temp=temp[temp['msg']!='<Media omitted>\n']

        L=[]
        for i in temp['msg']:
            L.extend(i.split())

        new_df=pd.DataFrame(Counter(L).most_common(20)).rename({'0':'Word','1':'Times Repeat'}) 

        return new_df

    else:
        df=df[df['user']==selected_user]
        temp=df[df['user']!='Group Notification']
        temp=temp[temp['msg']!='<Media omitted>\n']

        L=[]
        for i in temp['msg']:
            L.extend(i.split())

        new_df=pd.DataFrame(Counter(L).most_common(20)).rename({'0':'Word','1':'Times Repeat'}) 

        return new_df 

def moth_wise_msg(selected_user,df):
    if selected_user=='Overall':
        timeline=df.groupby(['year','month','month_num']).count()['msg'].reset_index()
        a=timeline.shape[0]
        time=[]
        for i in range(a):
            time.append((timeline['month'][i] + " - " + str(timeline['year'][i])))  

        timeline['time']=time

        return timeline

    else:
        df=df[df['user']==selected_user]
        timeline=df.groupby(['year','month','month_num']).count()['msg'].reset_index()
        a=timeline.shape[0]
        time=[]
        for i in range(a):
            time.append((timeline['month'][i] + " - " + str(timeline['year'][i])))  

        timeline['time']=time

        return timeline 

def daily_timeline(selected_user,df):
    if selected_user=='Overall':
        daily_timeline=df.groupby('only_date').count()['msg'].reset_index()

        return daily_timeline

    else:
        df=df[df['user']==selected_user]
        daily_timeline=df.groupby('only_date').count()['msg'].reset_index()

        return daily_timeline

def most_busy_day(selected_users,df):
    if selected_users=='Overall':
        df['day_name']=df['only_date'].dt.day_name()

        return df['day_name'].value_counts() 

    else:
        df=df[df['user']==selected_users]
        df['day_name']=df['only_date'].dt.day_name()

        return df['day_name'].value_counts() 

def month_activity(selected_user,df):
    if selected_user=='Overall':
        return df['month'].value_counts()

    else:
        df=df[df['user']==selected_user]
        return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='msg', aggfunc='count').fillna(0)

    return user_heatmap

