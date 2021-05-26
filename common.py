import random
import time
import requests
import datetime
import csv
from proxy_support import USE_PROXY,PROXY,random_proxy

#Function to get response from server
def get_response(url,headers):

  global PROXY
  
  got_response = True
  retry = 0
  while got_response and retry<5:
    try:

      if USE_PROXY:
        print("Using Proxy : ",PROXY)
        s = requests.Session()
        print('Getting Response ...')
        response = s.get(url, headers=headers,timeout=5,proxies={"http":PROXY, "https":PROXY})

      else:
        s = requests.Session()
        print('Getting Response ...')
        response = s.get(url, headers=headers)

      if response.status_code == 200:
        got_response = False

        sleep_time = random.randint(3,7)
        time.sleep(sleep_time)
        return response

      else:

        if USE_PROXY:
          PROXY = random_proxy()
          print('New Proxy','--> ','--','New Proxy:',PROXY)

        retry = retry + 1
        #response = ''
        print(response.status_code,"Retrying")
        sleep_time = random.randint(3,7)
        time.sleep(sleep_time)

    except Exception as e:

      if USE_PROXY:
        PROXY = random_proxy()
        print('New Proxy','--> ','--','New Proxy:',PROXY)

      retry = retry + 1
      print("Exception in get_response() : ",e)
      sleep_time = random.randint(3,7)
      time.sleep(sleep_time)

  return response


#Function to get date of scraping
def get_date():

  x = datetime.datetime.now()
  date = str(x.year)+ "/" + str(x.month) + "/" + str(x.day)
  return date

