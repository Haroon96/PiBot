import telepot
import time
import os
import sys
from proxy import get_proxy
import subprocess
import youtube_handler
from telepot.loop import MessageLoop

def get_token():
	token = open("token").read().strip()
	return token

def create_bot(token):	
	telepot.api.set_proxy(get_proxy())
	return telepot.Bot(token)

def sendMessage(id, msg):
	create_bot(get_token()).sendMessage(id, msg)
	
def handle(msg):
	print(msg)
	text = msg['text']
	id = msg['chat']['id']
	if 'youtu.be' in text or 'youtube' in text:
		sendMessage(id, 'Processing YouTube link')
		youtube_handler.handle(id, text)
	else:
		cmd = text.lower().strip()
		if 'rms' == cmd:
			sendMessage(id, 'Rebooting media server')
			os.popen("sudo -S minidlnad -R", 'w').write(open('pass').read())
		elif 'status' == cmd:
			sendMessage(id, 'Haroon-Pi is running')
		elif 'reboot' == cmd:
			sendMessage(id, 'Haroon-Pi is running')
			os.popen("sudo -S reboot", 'w').write(open('pass').read())
		elif 'help' == cmd:
			sendMessage(id, 'status, reboot, rms, help')
	
def main():
	os.chdir(sys.path[0])
	bot = create_bot(get_token())
	MessageLoop(bot, handle).run_as_thread()
	
	while 1:
		time.sleep(10)
	

if __name__ == "__main__":
	main()
