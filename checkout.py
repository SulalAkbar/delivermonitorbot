import requests
from bs4 import BeautifulSoup


def get_checkout_url(variant_id,cart_token):

	url = "https://limitededt.com/cart"
	payload={'attributes[collection_mobile_items_per_row]': '',
	'attributes[collection_desktop_items_per_row]': '',
	'updates['+variant_id+':'+cart_token+']': '1',
	'checkout': '',
	'note': ''}
	files=[
	]
	headers = {
	  'Cookie': '_landing_page=%2F; _orig_referrer=; cart_currency=SGD; secure_customer_sig=; _shopify_y=4de7d1d1-1ac7-44d7-9c17-a9f76e0a79b8; _y=4de7d1d1-1ac7-44d7-9c17-a9f76e0a79b8; _ga=GA1.2.2046952162.1620651102; _fbp=fb.1.1620651109623.461986699;  _gid=GA1.2.565647917.1621050200;  cart='+cart_token+'; last_cart_lead=09376403f2a20e53c6a737cfa514c661; _secure_session_id=601edef921409027564fd96c4cb52584; _shopify_s=e03a6bf9-c355-47dd-9ff1-13440d85fa1b; _s=e03a6bf9-c355-47dd-9ff1-13440d85fa1b; _shopify_sa_p=; shopify_pay_redirect=pending; cart_ver=gcp-us-east1%3A63; cart_ts=1621082253; dynamic_checkout_shown_on_cart=1; _shopify_sa_t=2021-05-15T12%3A51%3A41.987Z; _shopify_ga=_ga=2.62749608.565647917.1621050200-2046952162.1620651102; cart_currency=SGD; cart=09376403f2a20e53c6a737cfa514c661; cart_ts=1621086836; _checkout_queue_token=Aj3ctHdGJIhBMpbzsY3z-TscDTef4fQDspXV5DqtzAJ_znXJiRPuk625GJIITGtSxmUZ9MURdfI6f2Tx-dlSVnI2j-7oZMGfI1AM-0UOf4FYg3JVFZ2ww_Tvb2KfOh8J9qAef_pi7oP52rkT_uK4OhQqY9vRnm-GMSeK-VeWQ_plxTuKJ7YbiCIVnA%3D%3D; _checkout_queue_checkout_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVZrWlRFeFlqRmxaR1F5TUdZNU4yUTBObVJoTXpBNU1UQTFNMlUxWVdVeE1nWTZCa1ZVIiwiZXhwIjoiMjAyMS0wNS0xNVQxNDo1Mzo1Ni4yMDVaIiwicHVyIjoiY29va2llLl9jaGVja291dF9xdWV1ZV9jaGVja291dF90b2tlbiJ9fQ%3D%3D--587521be1af9656a7d90f23d4b79030e46fc90e2; secure_customer_sig=; cart_ver=gcp-us-east1%3A70; _y=4de7d1d1-1ac7-44d7-9c17-a9f76e0a79b8; _s=e03a6bf9-c355-47dd-9ff1-13440d85fa1b; _shopify_y=4de7d1d1-1ac7-44d7-9c17-a9f76e0a79b8; _shopify_s=e03a6bf9-c355-47dd-9ff1-13440d85fa1b'
	}

	response = requests.request("POST", url, headers=headers, data=payload, files=files, allow_redirects=False)

	print(response.text)

	soup = BeautifulSoup(response.content,'lxml')

	checkout_url = soup.find("a").get("href")
	print(url)

	return checkout_url



def get_cart_token():

	url = "https://limitededt.com/cart.js"

	payload={}
	headers = {
	  #'referer': 'https://limitededt.com/collections/vans-vault-x-porter/products/porter-yoshida-co-ua-og-old-skool-lx?variant=32824975818823',
	  'Cookie': 'secure_customer_sig=; cart_currency=SGD; _y=4d5a3071-075a-4f2a-b514-c911339e5eca; _s=151d81fe-4569-47f3-af54-8aafec3bf4f8; _shopify_y=4d5a3071-075a-4f2a-b514-c911339e5eca; _shopify_s=151d81fe-4569-47f3-af54-8aafec3bf4f8'
	}

	response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

	#print(response.text)

	token = response.json()['token']

	print(token)
	return token



#cart_token = get_cart_token()
#get_checkout_url('32826218414151',cart_token)