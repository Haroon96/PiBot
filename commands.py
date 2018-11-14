import subprocess
import os
import shutil
import random
from config import Config
from bot import Bot
from proxy_manager import update_proxy as _update_proxy


def download_youtube_audio(params, chat_id):
	bot = Bot()
	bot.send_message(chat_id, "Downloading...")
	out_filename = f'ytdl-{random.randint(0, 1000)}'
	out_template = f'{out_filename}.%(ext)s'
	audio_filename = f'{out_filename}.mp3'
	subprocess.Popen(f'youtube-dl -o {out_template} -x --audio-format mp3 --audio-quality 320k {params}', shell=True).wait()
	bot.send_audio(chat_id, open(audio_filename, 'rb'))


def reboot_media_server(params, chat_id):
	Bot().send_message(chat_id, 'Rebooting MiniDLNA server')
	os.popen("sudo -S minidlnad -R", 'w').write(Config().read('sudo_password'))


def status_check(params, chat_id):
	Bot().send_message(chat_id, 'OK!')


def reboot(params, chat_id):
	Bot().send_message(chat_id, 'Rebooting...')
	os.popen("sudo -S reboot", 'w').write(Config().read('sudo_password'))


def update(params, chat_id):
	Bot().send_message(chat_id, 'Pulling updates...')
	remote_repo = Config().read('remote_repo')
	subprocess.Popen(f'git pull {remote_repo}', shell=True).wait()
	reboot(params, chat_id)

def update_proxy(params, chat_id):
	Bot().send_message(chat_id, 'Updating proxy...')
	_update_proxy()
	reboot(params, chat_id)


def list_media_server(params, chat_id):
	response = ''
	for i in os.listdir(Config().read('media_server_path')):
		response += f'{i}\n'
	if response == '':
		response = 'Media server is empty'
	Bot().send_message(chat_id, response)


def purge_media_server(params, chat_id):
	dir = Config().read('media_server_path')
	shutil.rmtree(dir)
	os.mkdir(dir)
	Bot().send_message(chat_id, 'Media server has been purged')
