import urllib3
from bs4 import BeautifulSoup
from helpers import get
from os import system

def get_url():
	return "https://free-proxy-list.net/";

def parse(html):
	soup = BeautifulSoup(html, 'html.parser')
	rawproxies = soup.find('table', attrs={'id' : 'proxylisttable'}).findAll('tr')[1:50]

	proxies = []
	for i in rawproxies:
		proxy = i.findAll('td')
		protocol = "http"
		if proxy[6].text == "yes":
			protocol = "https"
		ip = proxy[0].text
		port = proxy[1].text

		if test_ip(ip):
			print(protocol + "://" + ip + ":" + port)
			return protocol + "://" + ip + ":" + port

	return 0

def test_ip(ip):
	return True if system("ping -c 1 " + ip) is 0 else False

def get_proxy():
	#url = get_url()
	#html = get(url)
	#return parse(html)
	return "http://185.93.3.123:8080"
