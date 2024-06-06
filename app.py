import streamlit as st
import re 
import numpy as np
import pandas as pd
import preprocessor 
import stats 
from matplotlib import pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Text Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    
    df = preprocessor.preprocess_Data(data)
    # st.dataframe(df.head()) 
    
    
    # getting unique users
    user_unique = df['user'].unique().tolist()
    # user_unique.remove("group_notification")
    user_unique.insert(0, "All")
    
    
    # Create a dictionary to store the user and their corresponding message counts
    user_message_counts = {}

    # Iterate through the unique users and calculate the number of messages sent by each user
    for user in user_unique:
        message_count = df[df['user'] == user].shape[0]
        user_message_counts[user] = message_count

    # Sort the user_message_counts dictionary by the message counts in descending order
    sorted_user_message_counts = dict(sorted(user_message_counts.items(), key=lambda item: item[1], reverse=True))



    selected_user= st.sidebar.selectbox("Select User",sorted_user_message_counts.keys())
    
    if st.sidebar.button("Show Data"):
        st.write(df)
        # st.write(df.shape[0])
    
    if st.sidebar.button("Show Stats"):
        # st.write(df.describe())
        st.title("Whatsapp Text Analysis")

        total_messages , words , media_shared , links = stats.fetch_stats(selected_user,df)
        col1 , col2 , col3 , col4 = st.columns(4)
        
        
        with col1:
            st.markdown("<h4 style='text-align: center;'>Total Messages</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>{total_messages}</h1>", unsafe_allow_html=True)
    
        with col2:
            st.markdown("<h4 style='text-align: center;'>Total Words</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>{len(words)}</h1>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<h4 style='text-align: center;'>Total Media Shared</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>{media_shared}</h1>", unsafe_allow_html=True)

        with col4:
            st.markdown("<h4 style='text-align: center;'>Total Links Shared</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>{len(links)}</h1>", unsafe_allow_html=True)

        
        # monthly timeline 
        st.title("Monthly Timeline")    
        timeline=stats.monthly_timeline(selected_user,df)
        fig , ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=stats.daily_timeline(selected_user,df)
        fig , ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # activity map
        st.title("Activity Map")
        col1 , col2 = st.columns(2)
              
        
        with col1:
            st.header("Most Active Days")
            busy_Day = stats.week_activity_map(selected_user,df)    
            fig , ax = plt.subplots()
            ax.bar(busy_Day.index,busy_Day.values,color="orange")
            ax.set_xticklabels(busy_Day.index, rotation=45, ha='right')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Active Months")
            busy_month = stats.monthly_activity_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='red')
            ax.set_xticklabels(busy_month.index, rotation=45, ha='right')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            
        st.title("User Heatmap")        
        user_heatmap=stats.heat_map(selected_user,df)
        fig , ax = plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        #busy user
        if selected_user == "All":
            st.title("Busiest User")
            col1, col2 = st.columns(2)
            most_busy_users , new_df = stats.getting_most_busy_user(selected_user, df)

            fig, ax = plt.subplots()

            with col1:
                ax.bar(most_busy_users.index, most_busy_users.values)
                ax.set_xticklabels(most_busy_users.index, rotation=45, ha='right')

                st.pyplot(fig)
            with col2:
                st.write(new_df)

        # word cloud 
        
       
        df_word_cloud = stats.create_word_cloud(selected_user,df)
        st.title("Word Cloud")
        # st.write(df_word_cloud)
        fig , ax =  plt.subplots()
        ax.imshow(df_word_cloud, interpolation='bilinear')
        st.pyplot(fig)
        
        #most common words
        col1 , col2 = st.columns(2)
        with col2:
            most_common_words = stats.most_common_words(selected_user,df)
            st.title("Most Common Words")
            
            fig , ax =  plt.subplots()
            ax.bar(most_common_words[0].index, most_common_words[0].values)
            ax.set_xticklabels(most_common_words[0].index, rotation=45, ha='right')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col1:
            st.dataframe(most_common_words)
            
            
            
        
        #most common emojis
        col1 , col2 = st.columns(2)
        with col2:
            most_common_emojis = stats.most_common_emojis(selected_user,df)
            st.title("Most Common Emojis")
            most_common_emojis = most_common_emojis.head(10)
            fig , ax =  plt.subplots()
            ax.bar(most_common_emojis[0].index, most_common_emojis[0].values)
            ax.set_xticklabels(most_common_emojis[0].index, rotation=45, ha='right')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col1:
            st.dataframe(most_common_emojis)
            
            
        
                            
            
    