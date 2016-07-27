import pandas as pd
import json
import time
from datetime import date
import dateutil

#data = json.loads('E:\ggevent.log')
fiLe = open('E:\ggevent.log', "r")
userString = raw_input("Enter a string name to search: ")
important =[]
for line in fiLe.readlines():
    important.append(json.loads(line))
    
df =pd.DataFrame(important)
timestamp, game_id, ai5, debug, random, sdkv, event, ts = [], [], [], [], [], [], [], []
for i in range(len(df)):
    timestamp.append(str(df['bottle'][i][u'timestamp']))
    game_id.append(str(df['bottle'][i][u'game_id']))
    ai5.append(str(df['headers'][i][u'ai5']))
    debug.append(str(df['headers'][i][u'debug']))
    random.append(str(df['headers'][i][u'random']))
    sdkv.append(str(df['headers'][i][u'sdkv']))
    event.append(str(df['post'][i][u'event']))
    ts.append(str(df['post'][i][ u'ts']))
    
columns = ['timestamp', 'game_id', 'ai5', 'debug', 'random', 'sdkv', 'event', 'ts']
df_1 = pd.DataFrame(columns = columns)
df_1['timestamp'] = pd.Series(timestamp)
df_1['game_id'] = pd.DataFrame(game_id)
df_1['ai5'] = pd.DataFrame(ai5)
df_1['debug'] = pd.DataFrame(debug)
df_1['random'] = pd.DataFrame(random)
df_1['sdkv'] = pd.DataFrame(sdkv)
df_1['event'] = pd.DataFrame(event)
df_1['ts'] = pd.DataFrame(ts)

ai5_unique = df_1['ai5'].unique()

d = df_1.groupby(ai5)
f = list(d)
print f[0]
wrong_list =[]
for i in range(len(f)):
    if len(f[i][1]) == 1: 
        wrong_list.append(f[i]) 

for i in range(len(wrong_list)):
    f.remove(wrong_list[i])
#for _id in ai5_unique:

session_time = []
hash_id = []
session_num = []
for i in range(len(f)):
        #try:
    count = 0
    session = 0
    indx = f[i][1].index.tolist()
    for j in indx:
        if f[i][1]['ai5'][j] == f[i][0] and f[i][1]['event'][j] == 'ggstart' and count ==0:
            stack = []
            iter = []
            count = count + 1
            stack.append(f[i][1]['ts'][j])
            iter.append(count)
        elif f[i][1]['ai5'][j] == f[i][0] and f[i][1]['event'][j] == 'ggstart' and count == 1:
            count = 0
            count = count +1
            stack.append(f[i][1]['ts'][j])
            iter.append(count) 
        elif f[i][1]['ai5'][j] == f[i][0] and f[i][1]['event'][j] == 'ggstop' and count == 1:
            count = 0
            count = count - 1
            stack.append(f[i][1]['ts'][j])
            iter.append(count)
        elif f[i][1]['ai5'][j] == f[i][0] and f[i][1]['event'][j] == 'ggstop' and count == -1:
            count = 0
            count = count -1
            stack.append(f[i][1]['ts'][j])
            iter.append(count)
        elif f[i][1]['ai5'][j] == f[i][0] and f[i][1]['event'][j] == 'ggstart' and count == -1:
            next_event = dateutil.parser.parse(time.strftime('%m/%d/%Y %H:%M:%S', (time.gmtime(int(f[i][1]['ts'][j])/1000.))))
            next_event_time = (next_event.hour)*3600 + (next_event.minute)*60 + (next_event.second)
            previous_event = dateutil.parser.parse(time.strftime('%m/%d/%Y %H:%M:%S', (time.gmtime(int(stack[-1])/1000.))))
            previous_event_time = (previous_event.hour)*3600 + (previous_event.minute)*60 + (previous_event.second)
            first_event = dateutil.parser.parse(time.strftime('%m/%d/%Y %H:%M:%S', (time.gmtime(int(stack[0])/1000.))))
            first_event_time = (first_event.hour)*3600 + (first_event.minute)*60 + first_event.second
            #session_time.append(stack[-1] - stack[0])
            #hash_id.append(_id)
            
            if (next_event_time - previous_event_time) > 30:
                session_time.append(previous_event_time - first_event_time)
                hash_id.append(f[i][0])
                session_num.append(session +1)
                count = 0
                stack = []
                iter = []
                count = count + 1
                stack.append(f[i][1]['ts'][j])
                iter.append(count)
            else:
                count = 0
                #stack = []
                #iter = []
                count = count + 1
                session = session
                stack.append(f[i][1]['ts'][j])
                iter.append(count)
            
        elif f[i][1]['ai5'][j] == f[i][0] and f[i][1]['event'][j] == 'ggstop' and count ==0:
            pass
        else:
            pass
                    
auth_ = []
for i in range(len(session_time)):
    if session_time[i] >= 60:
        auth_.append('valid')
    else:
        auth_.append('invalid')
        
session_time = pd.DataFrame(session_time)
hash_id = pd.DataFrame(hash_id)
auth_ = pd.DataFrame(auth_)
submission = pd.concat([session_time, hash_id, auth_], axis=1)


    