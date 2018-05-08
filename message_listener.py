import telepot
import time
import os
import sys
from proxy import get_proxy
import subprocess
from send_message import send_message as sm
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
		subprocess.Popen('youtube-dl -x --audio-format mp3 --audio-quality 0 --exec "python3 send_audio.py ' + str(id) + ' {}" ' + text, shell=True)
	else:
		cmd = text.lower().strip()
		if 'rms' == cmd:
			sendMessage(id, 'Rebooting media server')
			os.popen("sudo -S minidlnad -R", 'w').write(open('pass').read())
		elif 'status' == cmd:
			sendMessage(id, 'Running')
		elif 'reboot' == cmd:
			sendMessage(id, 'Rebooting...')
			os.popen("sudo -S reboot", 'w').write(open('pass').read())
		elif 'help' == cmd:
			sendMessage(id, 'status, reboot, rms, help')
		elif 'update' == cmd:
			sendMessage(id, 'Pulling updates from GitLab...')
			subprocess.Popen('git pull https://haroon96:EchoFoxtrot96@gitlab.com/haroon96/HaroonPiBot', shell=True).wait()
			os.popen("sudo -S reboot", 'w').write(open('pass').read())
			
def main():
	os.chdir(sys.path[0])
	bot = create_bot(get_token())
	sm('Booted successfully')
	MessageLoop(bot, handle).run_as_thread()
	
	while 1:
		time.sleep(10)
	

if __name__ == "__main__":
	main()
