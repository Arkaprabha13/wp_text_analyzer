from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji



extractor = URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user != "All":
        df = df[df['user']==selected_user]
    
    
    total_media_shared = df[df['message'] == '<Media omitted>'].shape[0]
    
    total_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    
    links=[]
    for messages in df['message']:
        links.extend(extractor.find_urls(messages))
    
    return total_messages,words,total_media_shared,links
    
    
    # if selected_user == "All":
        
    #     # getting number of messages
    #     total_messages = df.shape[0]
        
    #     #getting number of words
    #     words=[]
    #     for message in df['message']:
    #         words.extend(message.split())
        
    #     return total_messages, words
        
        
    # else:
    #     total_messages = df[df['user']==selected_user].shape[0]  
    #     words=[]
    #     df_of_selected_user = df[df['user']==selected_user]
    #     for message in df_of_selected_user['message']:
    #         words.extend(message.split())
        
    #     return total_messages,words
    # # if selected_user == "All":
    #     # total_messages = df.shape[0]
    
    
def getting_most_busy_user(selecected_user,df):
    x = df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"count":"Percent","user":"Phone_number"})
    return x , new_df

def create_word_cloud(selected_user,df):
    if selected_user != "All":
        df = df[df['user']==selected_user]
        
    
    word_cloud=WordCloud(width=700,height=400,background_color='white',max_words=50).generate(' '.join(df['message']))
    df_wc = word_cloud.generate(df['message'].str.cat(sep=' '))
    
    return df_wc


def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def most_common_emojis(selected_user, df):

    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    print("\n")
    print(selected_user)
    print("\n")
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    print("\n")
    print(emoji_df.shape)
    print("\n")
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != "All":
        df = df[df['user']==selected_user]
    
    monthly_timeline=df.groupby(['Year','month_number','Month']).count()['message'].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['Month'][i] + "-" + str(monthly_timeline['Year'][i]))
    monthly_timeline['time']=time

    return monthly_timeline


def daily_timeline(selected_user,df):
    if selected_user != "All":
        df = df[df['user']==selected_user]
    
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    
    if selected_user != "All":
        df = df[df['user']==selected_user]
    
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != "All":
        df = df[df['user']==selected_user]
    
    return df['Month'].value_counts()


def heat_map(selected_user,df):
    if selected_user != "All":
        df = df[df['user']==selected_user]
    activity_heatmap=df.pivot_table(index="day_name",columns="period",values="message",aggfunc='count').fillna(0)
    return activity_heatmap