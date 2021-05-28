from common import get_response
from bs4 import BeautifulSoup
import csv
import json
from checkout import get_cart_token,get_checkout_url
import requests
import os
import json

def get_api_url(page):
	api_url = "https://services.mybcapps.com/bc-sf-filter/filter?t=1621746261497&page="+str(page)+"&shop=limited-edt.myshopify.com&limit=48&sort=created-descending&display=grid&collection_scope=163082698823&product_available=false&variant_available=false&build_filter_tree=false&check_cache=false&sort_first=available&callback=BCSfFilterCallback&event_type=page"

	return api_url 

products_page_header = {
	

	"authority": "limitededt.com",
	"method": "GET",
	"path": "/products",
	"scheme": "https",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "deflate",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"cookie": "_landing_page=%2F; _orig_referrer=; secure_customer_sig=; cart_currency=SGD; _y=4de7d1d1-1ac7-44d7-9c17-a9f76e0a79b8; _shopify_y=4de7d1d1-1ac7-44d7-9c17-a9f76e0a79b8; _ga=GA1.2.2046952162.1620651102; _fbp=fb.1.1620651109623.461986699; omnisendAnonymousID=WRHeUxLo00cL3k-20210510125207; intercom-id-la3i4bs0=1d28dfd8-ef24-4aca-a63e-b385f991e6e3; intercom-session-la3i4bs0=; _s=7abccfd9-4500-483b-8299-04bdcbd42b02; _shopify_s=7abccfd9-4500-483b-8299-04bdcbd42b02; shopify_pay_redirect=pending; _shopify_sa_p=; _gid=GA1.2.565647917.1621050200; coin-currency=PKR; soundestID=20210515034425-jmqWkIs7BuwuuFmvc16JWXOccU86FdyhY0itURoVo6t90PntL; omnisendSessionID=gXzbButDz9ijon-20210515034425; cart=09376403f2a20e53c6a737cfa514c661; cart_ts=1621050632; cart_sig=595925e9ad31ee8935fdb0cd6a8c3890; cart_ver=gcp-us-east1%3A1; omnisendCartProducts=[]; last_cart_lead=09376403f2a20e53c6a737cfa514c661; _shopify_sa_t=2021-05-15T03%3A58%3A47.155Z",
	"pragma": "no-cache",
	"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
	"sec-ch-ua-mobile": "?0",
	"sec-fetch-dest": "document",
	"sec-fetch-mode": "navigate",
	"sec-fetch-site": "none",
	"sec-fetch-user": "?1",
	"upgrade-insecure-requests": "1",
	"user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",

}


#Function to parse collections urls
def main_page_parser(response):
	base_url = 'https://limitededt.com'

	soup = BeautifulSoup(response.content,'lxml')

	headers = soup.find_all("header",class_="SectionHeader")

	urls_list = []
	for h in headers:

		href = h.find("a").get("href")
		urls_list.append(base_url + href)

	return urls_list


# def brand_page_parser(response):
# 	base_url = 'https://limitededt.com'

# 	soup = BeautifulSoup(response.content,'lxml')

# 	headings = soup.find_all("div",class_='ProductItem__Info ProductItem__Info--center')

# 	urls_list = []
# 	for h in headings:

# 		href = h.find("a").get("href")
# 		urls_list.append(base_url + href)

# 	return urls_list



# def all_products_urls(response):

# 	brand_pages_urls = main_page_parser(response)

# 	all_products_list = []
# 	for brand in brand_pages_urls:
# 		resp = get_response(brand,products_page_header)

# 		urls_list = brand_page_parser(resp)

# 		print("Products in ",brand," are :",len(urls_list))
# 		all_products_list = all_products_list + urls_list

# 	return all_products_list






#Function to extract and return fields from product json
# def product_parser(product,url):

# 	collection = url.split('/')[-1]
# 	product_url = 'https://limitededt.com/collections/'+collection+'/'+'products/'+product['handle']
# 	product_title = product['title']
# 	product_image = product['images'][0]['src']
# 	product_state = 'available'
# 	product_variants_detail = []

# 	product_available_variants = []
# 	for v in product['variants']:

# 		if v['available'] == True:
# 			product_available_variants.append(v['title'])

# 			product_variants_detail.append({
# 				'id':v['id'],
# 				'price':v['price'],
# 				})

# 	if len(product_available_variants) > 0:
# 		#print(product_title,product_image,product_available_variants,product_variants_detail)

# 		print('		Available : ',product_url)
# 		product_state = 'available'

# 	else:
# 		print('		Sold Out : ',product_url)
# 		product_state = 'sold'


# 	product_variants_detail = json.dumps(product_variants_detail)
# 	product_available_variants = json.dumps(product_available_variants)

# 	return [product_state,product_url,product_title,product_image,product_available_variants,product_variants_detail]

def product_parser(product):
	base_url = "https://limitededt.com/collections/footwear/products/"
	product_url = base_url + product['handle']

	product_title = product['title']
	product_image = product['images']['1']

	if product['available'] == True:
		product_state = 'available'
	else:
		product_state = 'sold'

	product_variants_detail = []
	product_available_variants = []
	variants = product['variants']
	for v in variants:

		if v['available'] == True:
			product_available_variants.append(v['title'])

			product_variants_detail.append({
				'id':v['id'],
				'price':v['price']
				})

	product_question = ''
	html = product['body_html']
	if 'Question:' in html:
		product_question = html
		

	#print(product_variants_detail)
	#print(product_available_variants)
	product_variants_detail = json.dumps(product_variants_detail)
	product_available_variants = json.dumps(product_available_variants)

	return [product_state,product_url,product_title,product_image,product_available_variants,product_variants_detail,product_question]


	




























#Function to save data in CSV		
def csv_writer(product_list):

	file = "new_file.csv"
	csv_file = open(file, 'a', newline="",encoding="utf-8")

	try:

		writer = csv.writer(csv_file)
		writer.writerow(product_list)
		csv_file.close()

	except Exception as e:
		print('Error in CSV()',e)


#Function to read DATA from CSV
def csv_reader(file):

	data = []
	with open(file,encoding="utf-8") as csv_file:
	    reader = csv.reader(csv_file)
	    for row in reader:
	        data.append(row)

	return data

#Creating Data Structure for Scraped Data
def create_struct(data):

	struct = {}

	for row in data:
		#print(row)
		struct[row[1]] = {'state':row[0],'title':row[2],
	'image':row[3],'available':row[4],'variants':row[5],'question':row[6]}

	return struct

#Function to send notifications
def send_notification(state,key,value,web_hook_url):

	#print(key,'---',value)
	variants_available = json.loads(value['available'])
	#print(variants_available)

	question = value['question']
	title = value['title']
	price = json.loads(value['variants'])[0]['price']

	cart_links_list = []
	for variants_id in json.loads(value['variants']):

		#print('HI',variants_id)
		cart_token = get_cart_token()
		cart_link = get_checkout_url(str(variants_id['id']),cart_token)
		cart_links_list.append(cart_link)

	cart_data = ''

	for i in range(len(variants_available)):

		

		cart_data = cart_data + variants_available[i] +'|  In Stock    |[Open Task]('+ cart_links_list[i] +')\n'

	content = '**'+title+'**\n'+key+'\n**State**\n'+state+'\n**PRICE**\n'+price+'\n\n'+question+'\n\n**Cart**\n\n'+cart_data
	
	discord_hook(content,web_hook_url)
	#return content
	#pass

#Function to send message to Discord Web Hook
def discord_hook(content,web_hook_url):
	url = web_hook_url

	data = {"content": content}

	print('Sending Message')
	response = requests.post(url, json=data)

#Function to compare prev and new data and send notifications
def check_for_change(newfile,prevfile,web_hook_url):
	new_data = csv_reader(newfile)
	prev_data = csv_reader(prevfile)

	new_struct = create_struct(new_data)
	prev_struct = create_struct(prev_data)

	#Logic for checking changes
	for url in new_struct:
		if url in prev_struct:
			print('Yes')

			if new_struct[url]['state'] == 'available':

				if prev_struct[url]['state'] == 'sold':
					print('Change State from sold to available',url)
					#send_notification()
					#Sending Notification
					send_notification('Restock',url,new_struct[url],web_hook_url)

				#Now check for any new size or variants update
				if prev_struct[url]['state'] == 'available':
					for v in json.loads(new_struct[url]['available']):
						if v in json.loads(prev_struct[url]['available']):
							print(v,'Already')
						else:
							print('Send Notification for New Variant',url)

							send_notification('Variant Restock',url,new_struct[url],web_hook_url)


		else:
			print('New Item')
			send_notification('New Arrival',url,new_struct[url],web_hook_url)


#Function to remove file
def delete_file(file):
	os.remove(file)

#Function to rename file
def rename_file(prev_name,new_name):
	os.rename(prev_name,new_name)


#Collecting all collections urls from main page
def all_collections_urls(response):
	soup = BeautifulSoup(response.content,'lxml')
	a = soup.find_all("a",class_="Text--subdued Link Link--primary")

	all_collections_urls = []
	for url in a:
		all_collections_urls.append(i.get('href'))

	return all_collections_urls[0:-2]


def extract_json(response):

	text  = response.text.replace("/**/ typeof BCSfFilterCallback === \'function\' && BCSfFilterCallback","")
	resp_json = json.loads(text[1:-2])

	total_products = resp_json['total_product']
	pages = total_products/48
	if type(pages) == float:
		pages = int(pages) + 1


	return {'json':resp_json,'pages':pages}


######################################################

######################################################

#Function to scrape Products Data from Site ...
# def products_scraper():
# 	url = "https://limitededt.com/products"
# 	response = get_response(url,products_page_header)

# 	#all_products_urls(response)
# 	print('Getting Collection URLS')
# 	collections_urls = main_page_parser(response)

# 	count = 1
# 	for url in collections_urls:
# 		print('Getting URL : ',count,"--",url)
# 		col_resp = get_response(url + '/products.json',products_page_header)
# 		col_json = col_resp.json()
# 		products = col_json['products']

# 		for product in products:

# 			product_data = product_parser(product,url)
# 			csv_writer(product_data)

# 			print('		Product Saved')

# 		count = count + 1

#Function to scrape products data from '/footwear'

def products_scraper_footwear():

	print("Getting First Page '/footwear' :")
	response = get_response(get_api_url(1),products_page_header)
	resp_json = extract_json(response)
	products = resp_json['json']['products']
	for product in products:

		product_data = product_parser(product)
		csv_writer(product_data)

	pages = resp_json['pages']

	for page in range(2,pages+1):
		print("Getting Next Page :",page)
		response = get_response(get_api_url(page),products_page_header)
		resp_json = extract_json(response)
		products = resp_json['json']['products']
		for product in products:

			product_data = product_parser(product)
			csv_writer(product_data)



#products_scraper_footwear()
# new_data = csv_reader("new_file.csv")
# new_struct = create_struct(new_data)

# keys = list(new_struct.keys())

# content = send_notification('New Arrival',keys[3],new_struct[keys[3]])


# #content = '[example](https://support.discord.com/hc/en-us/community/posts/360038398572-Hyperlink-Markdown)'

# discord_hook(content)




#check_for_change('new_file.csv','prev_file.csv',"https://discord.com/api/webhooks/843695641598885918/d3VuT_VZ6EMxxMmRwnVOvu2YxyMNPYWALgsb9soXzkz-lc55cDhLCbpGnJw9cYlMMEA_")