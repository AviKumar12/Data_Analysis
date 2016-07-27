import requests
import json
import pandas as pd
api_key = 'xxxxxx'
url1 = "https://api.fullcontact.com/v2/company/lookup.json?domain="


def whois(dom):

 url = url1 +str(dom)
 headers={'Content-Type': 'application/json','X-FullContact-APIKey':'xxxxxx'}
 r = requests.get(url,headers = headers)
 return json.loads(r.text)

data = pd.read_csv('brand_website.csv')
brand=  data.brand
channel =[]
brand_id =[]
url =[]
username =[]
brand_url =[]
social_network_username =[]

for brand in brand :
  k =  whois(brand)
  print k.keys()
  #print len(k['socialProfiles'])
  # print k['socialProfiles'][0]
  # if len(k.keys())>0:
  #    for kk in k.keys():
  #        print k[kk]

  try:
      for i in range(len(k['socialProfiles'])):
          try:
              channel.append(k['socialProfiles'][i]['typeName'])
              try:
                  brand_id.append(str(k['socialProfiles'][i]['id']))
              except:
                  brand_id.append('N/A')
              try:
                  link= str(k['socialProfiles'][i]['url'])
                  lis_in = link.split("/")
                  url.append(lis_in[-1])
              except:
                  url.append('N/A')
              try:
                  username.append(k['socialProfiles'][i]['username'])
              except:
                  username.append('N/A')
              brand_url.append(brand)
          except:
              pass
  except:
      pass
          
  
try:
   columns = ['brand_url','channel_name', 'brand_id', 'url', 'username']
   df = pd.DataFrame(columns = columns)
except:
   pass
try:
   df['brand_url'] = pd.Series(brand_url)
except:
   pass
try:
   df['channel_name'] = pd.Series(channel)
except:
   pass    
try:
   df['brand_id'] = pd.DataFrame(brand_id)
except:
   pass    
try:
   df['url'] = pd.DataFrame(url)
except:
   pass    
try:
   df['username'] = pd.DataFrame(username)
except:
   pass
      
     
# url = df.url
# for url in url:
#     link = url
#     lis_In = link.split("/")
#     social_network_username.append(lis_In[-1])
# 
# try:
#     df['social_network_username'] =
#       

df.to_csv('brand_ingestion.csv')
  
