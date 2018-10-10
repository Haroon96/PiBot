import urllib3

def download(method, url):
	http = urllib3.PoolManager()
	r = http.request(method, url)
	return r.data

def get(url):
	return download('GET', url)
	
def post(url):
	return download('POST', url)
	
