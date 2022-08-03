
import streamlit as st
import preprocssor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp chat Analyzer')

uploaded_file=st.sidebar.file_uploader('Choose a file')


if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocssor.preprocess(data)

    user=df['user'].unique().tolist()
    user.remove('Group Notification')
    user.sort()
    user.insert(0,"Overall")
    selected_user=st.sidebar.selectbox('Show Analysis with.... ',user)

    if st.sidebar.button('Show Analysis'):
        
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(helper.number_msg(selected_user,df))

        with col2:
            st.header('Total Words') 
            st.title(helper.number_words(selected_user,df)) 

        with col3:  
            st.header('Media Shared')
            st.title(helper.media(selected_user,df)) 

        with col4:
            st.header('Links Shared')
            st.title(helper.links(selected_user,df))  

        if selected_user=='Overall':
            st.title("Most Busy User")
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2) 
            with col1:                
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df) 
        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        st.title('Most Frequent Words') 
        most_common_words=helper.most_words(selected_user,df) 
        fig,ax=plt.subplots()
        ax.bar(most_common_words[0],most_common_words[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Monthly Timeline")
        timeline=helper.moth_wise_msg(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['msg'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['msg'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.most_busy_day(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 
        
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        

