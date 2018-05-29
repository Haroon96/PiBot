import telepot
import sys
import os
from proxy import get_proxy

def get_token():
	token = open("token").read().strip()
	return token

def form_name(args):
	return "".join(args[2:])

def create_bot(token):	
	telepot.api.set_proxy(get_proxy())
	return telepot.Bot(token)

def send_audio(chat_id, audio_file):
	create_bot(get_token()).sendAudio(chat_id, open(audio_file, 'rb'))

def main():
	chat_id = sys.argv[1]
	audio_file = form_name(sys.argv)
	haroon_chat_id = open('chat_id').read().strip()
	send_audio(chat_id, audio_file)
	if chat_id != haroon_chat_id:
		send_audio(haroon_chat_id, audio_file)
	os.remove(audio_file)

if __name__ == "__main__":
	main()
