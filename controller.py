import time
from monitor import check_for_change,delete_file,rename_file,products_scraper_footwear


#In Minutes
INTERVAL_TIME = 30 

#Enter URL of channel for which you want to recive notifications
WEB_HOOK = "https://discord.com/api/webhooks/843695641598885918/d3VuT_VZ6EMxxMmRwnVOvu2YxyMNPYWALgsb9soXzkz-lc55cDhLCbpGnJw9cYlMMEA_"



def monitor_products():
	#print("\n\n\n\n\n\nStarting Scraping New Data :",count,'\n\n\n\n\n\n')
	#products_scraper()
	products_scraper_footwear()
	print("Checking Changes")
	check_for_change('new_file.csv','prev_file.csv',WEB_HOOK)
	print('Deleting Old file')
	delete_file('prev_file.csv')
	print('Renaming New File')
	rename_file('new_file.csv','prev_file.csv')




print('Starting Monitor Products ...')
monitor_products()
print('Closing Monitor Products ...')