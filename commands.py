import subprocess
import os
import shutil
import random
from subprocess import PIPE
from config import Config
from bot import Bot
from proxy_manager import update_proxy as _update_proxy


def download_youtube_audio(params, chat_id):
	bot = Bot()
	bot.send_message(chat_id, "Starting download...")
	process = subprocess.run(f'youtube-dl -o %\(title\)s.%\(ext\)s --get-filename {params}', stdout=PIPE, shell=True)
	out = process.stdout.decode()
	audio_filename = f"{out[:out.rindex('.')]}.mp3"
	subprocess.run(f'youtube-dl -o %\(title\)s.%\(ext\)s -x --audio-format mp3 --audio-quality 320k {params}', shell=True)
	print(audio_filename)
	bot.send_audio(chat_id, open(audio_filename, 'rb'))
	os.remove(audio_filename)


def reboot_media_server(params, chat_id):
	Bot().send_message(chat_id, 'Rebooting MiniDLNA server.')
	os.popen("sudo -S minidlnad -R", 'w').write(Config().read('sudo_password'))


def status_check(params, chat_id):
	Bot().send_message(chat_id, 'OK!')


def reboot(params, chat_id):
	Bot().send_message(chat_id, 'Rebooting...')
	os.popen("sudo -S reboot", 'w').write(Config().read('sudo_password'))


def update(params, chat_id):
	Bot().send_message(chat_id, 'Pulling updates...')
	remote_repo = Config().read('remote_repo')
	subprocess.run(f'git pull {remote_repo}', shell=True)
	reboot(params, chat_id)


def update_proxy(params, chat_id):
	Bot().send_message(chat_id, 'Updating proxy...')
	_update_proxy()
	reboot(params, chat_id)


def list_media_server(params, chat_id):
	response = ''
	for i in os.listdir(get_media_server_path()):
		response += f'{i}\n'
	if response == '':
		response = 'Media server is empty.'
	Bot().send_message(chat_id, response)


def purge_base_directory(params, chat_id):
	dir = Config().read('base_directory')
	for i in os.listdir(dir):
		shutil.rmtree(f'{ dir }/{ i }', ignore_errors=True)
		os.mkdir(f'{ dir }/{ i }')
	Bot().send_message(chat_id, 'Base directory has been purged.')


def download_torrent(params, chat_id):
	subprocess.run(f'qbittorrent "{params}"', shell=True)
	Bot().send_message(chat_id, 'Starting torrent download...')
	

def get_media_server_path():
	base_dir = Config().read('base_directory')
	media_server_dir = Config().read('media_server_directory')
	return base_dir + media_server_dir