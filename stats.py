from urlextract import URLExtract
import pandas as pd
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import emoji



extractor = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Total messages sent
    total_messages = df.shape[0]
    Words = []
    for message in df['message']:
        Words.extend(message.split())

    # Total meida files shared
    media_commited = df[df['message'] == '<Media omitted>']
    