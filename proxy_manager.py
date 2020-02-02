import urllib3
from bs4 import BeautifulSoup
from os import system
from config import Config

proxy_list_url = 'https://free-proxy-list.net/'
telegram_url = 'https://core.telegram.org/bots/api'

def get(url):
	http = urllib3.PoolManager()
	r = http.request('GET', url)
	return r.data

def generate_proxies():
	html = get(proxy_list_url)
	soup = BeautifulSoup(html, 'html.parser')
	proxy_list = soup.find(
		'table', attrs={'id': 'proxylisttable'}).findAll('tr')[1:50]

	for i in proxy_list:
		proxy = i.findAll('td')
		protocol = "http"
		if proxy[6].text == "yes":
			protocol = "https"
		ip = proxy[0].text
		port = proxy[1].text

		yield protocol + "://" + ip + ":" + port


def test_proxy(proxy_url):
	try:
		proxy = urllib3.ProxyManager(proxy_url)
		proxy.request('GET', telegram_url, timeout=5)
		return True
	except:
		return False


def update_proxy():
	for proxy in generate_proxies():
		if test_proxy(proxy):
			config = Config()
			config.write('proxy_url', proxy)
			config.save()
			return proxy
	return ''

if __name__ == "__main__":
	update_proxy()
