import csv
import random


def csv_proxy_reader(file):

	proxies = []
	with open(file) as csv_file:
	    reader = csv.reader(csv_file)
	    for row in reader:
	        proxies.append(row.pop())

	return proxies

def random_proxy():

  random_index = random.randint(0, proxy_length - 1)
  return PROXIES[random_index]

PROXIES = csv_proxy_reader("proxies.csv")
proxy_length = len(PROXIES)

if proxy_length > 0:
  USE_PROXY = True
  PROXY = random_proxy()
  
else:
  USE_PROXY = False
  PROXY = False