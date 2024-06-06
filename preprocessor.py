import re
import pandas as pd

def preprocess_Data(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # Extract dates using regex
    dates_pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [APM]{2}'
    dates = re.findall(dates_pattern, data)
    
    # Extract messages using regex
    messages_pattern = r'(?<= - ).*'
    messages = re.findall(messages_pattern, data)

    # Remove dates from messages
    messages = [re.sub(dates_pattern, '', msg).strip() for msg in messages]
    # Remove system messages (like "created group" or "You were added") that might be causing the discrepancy
    messages = [msg for msg in messages if not re.match(r'\+\d{2} \d{10}', msg.split(':')[0])]

    # Handling mismatch in lengths
    if len(dates) > len(messages):
        dates = dates[:len(messages)]
    elif len(messages) > len(dates):
        messages = messages[:len(dates)]
        
    df = pd.DataFrame({'user_message':messages,'message_Date':dates})
    #converting message_date time 
    df['message_Date'] = pd.to_datetime(df['message_Date'],format = "%m/%d/%y, %I:%M %p")
    df.rename(columns={"message_Date":"date"},inplace=True)
    # df.head()
    
    # Function to split user and message
    def split_user_message(row):
        if ':' in row:
            user, message = row.split(':', 1)
            return pd.Series([user.strip(), message.strip()])
        else:
            return pd.Series([None, row.strip()])

    # Apply function to DataFrame
    df[['user', 'message']] = df['user_message'].apply(split_user_message)

    # Drop the original user_message column
    df.drop(columns=['user_message'], inplace=True)

    # Extract user and message lists
    user_list = df['user'].tolist()
    message_list = df['message'].tolist()
    
    
    df['Year']=df['date'].dt.year
    df['Month']=df['date'].dt.month_name()
    df['month_number'] = df['date'].dt.month
    df['Day']=df['date'].dt.date
    df['hour']=df['date'].dt.hour
    df['minutes']=df['date'].dt.minute
    df['day_name']=df['date'].dt.day_name()
    df['only_date']=df['date'].dt.date
    
    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
            
    df['period']=period
    return df

    