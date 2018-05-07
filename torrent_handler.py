import os
import sys
import zipfile
import shutil
import subprocess
from send_message import send_message
from bs4 import BeautifulSoup
from helpers import get, post
from time import sleep


def get_server_location():
	return "/mnt/extstorage/mediaserver/"

def changedir(path=0):
	if (path == 0):
		path = os.path.realpath(__file__)
		path = path[:path.rindex("/")]	
	os.chdir(path)

def parse_args(argv):
	i = argv.index("--name")
	j = argv.index("--path")
	name = " ".join(argv[i + 1:j])
	path = " ".join(argv[j + 1:])
	return name, path

def parse(html):
	soup = BeautifulSoup(html, 'html.parser')
	results = soup.find('table').findAll('tr')[1:]
	
	partial_link = ""
	for result in results:
		ok = True
		if result.findAll('td')[0].text.find('English') == -1:
			ok = False
		if len(result.findAll('td', attrs={"class":"a41"})) > 0:
			ok = False
		if ok:
			partial_link = result.find('a')['href']
			break

	link = make_result_url(partial_link)
	html = post(link)
	
	soup = BeautifulSoup(html, 'html.parser')
	dllink = soup.find('a',{"id":"downloadButton"})['href']
	return make_result_url(dllink)
	
def make_search_url(query):	
	return "https://subscene.com/subtitles/release?q=" + query

def make_result_url(postfix):
	return "https://subscene.com" + postfix	

def download_subtitles(name):
	search_url = make_search_url(name)
	html = get(search_url)
	dllink = parse(html)
	sub = get(dllink)

	filename = "subs.zip"
	f = open(filename, "wb")
	f.write(sub)
	f.close()

	return filename

def extract_archive(filename):
	zip_ref = zipfile.ZipFile(filename, 'r')
	zip_ref.extractall()
	zip_ref.close()

def move_to_server(filename):
	shutil.move(filename, get_server_location() + "/" + filename)

def copy_to_server(filename):
	shutil.copy(filename, get_server_location() + "/" + filename)
	
def embed_subs(vidfile, subfile):
	outfile = vidfile[:-4] + "[SUBBED].mkv"
	subprocess.run(["ffmpeg", "-i", vidfile, "-i", subfile, "-c", "copy", "-c:s", "srt", outfile])
	return outfile

def search(ext):
	files = os.listdir()
	for f in files:
		if f.endswith(ext):
			return f
	return 0

def get_vid_filename():
	f = search(".mkv")
	if (f == 0):
		f = search(".mp4")
	return f
	
def get_sub_filename():
	return search(".srt")			

def main():
	changedir()

	name, path = parse_args(sys.argv)
	
	if path.find("/tvshows") >= 0:
		changedir(path)
		sleep(3*60*60) # sleep for 3 hours for subs to be available
		filename = download_subtitles(name)
		extract_archive(filename)
		vidfile = get_vid_filename()	
		subfile = get_sub_filename()
		outfile = embed_subs(vidfile, subfile)
		move_to_server(outfile)
		changedir()

	send_message(name + " has finished downloading.")
		
if __name__ == "__main__":
	main()
