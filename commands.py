import subprocess
import os
import shutil
import random
from subprocess import PIPE
from config import Config
from bot import Bot
import json
from modules.music_module import embed_music_metadata
from proxy_manager import update_proxy as _update_proxy


def send_youtube_link(chat_id, msg_id, js, replace_ext=None):
	title = js['title']
	filename = js['_filename']
	if replace_ext is not None:
		filename = f'{os.path.splitext(filename)[0]}.{replace_ext}'
	config = Config()
	base_dir = config.read('base_directory')
	http_url = config.read('media_http_url')
	rpath = filename.replace(base_dir, '')
	msg = f'<a href="{http_url}{rpath}">{title}</a>'
	Bot().send_message(chat_id, msg, msg_id=msg_id, format='HTML')

def get_youtube_output_format():
	config = Config()
	base_dir = config.read('base_directory')
	ytdl_dir = config.read('ytdl_directory')
	path = os.path.join(base_dir, ytdl_dir)
	return f'{path}/%\(title\)s.%\(ext\)s'

def download_youtube_audio(params, chat_id, msg_id):
	Bot().send_message(chat_id, "Starting download...", msg_id=msg_id)
	process = subprocess.run(f'youtube-dl -o {get_youtube_output_format()} -x --audio-format mp3 --audio-quality 320k --restrict-filenames --print-json {params}', shell=True, stdout=PIPE)
	js = json.loads(process.stdout.decode())
	# get title and filename from youtube-dl
	title = js['title']
	filename = f"{os.path.splitext(js['_filename'])[0]}.mp3"
	# update title and filename from metadata
	title, filename = embed_music_metadata(title, filename)
	# replace original json values
	js['title'] = title
	js['_filename'] = filename
	send_youtube_link(chat_id, msg_id, js, replace_ext='mp3')

def download_youtube_video(params, chat_id, msg_id):
	Bot().send_message(chat_id, "Starting download...", msg_id=msg_id)
	process = subprocess.run(f'youtube-dl -o {get_youtube_output_format()} --recode-video mkv --print-json --restrict-filenames {params}', stdout=PIPE, shell=True)
	js = json.loads(process.stdout.decode())
	send_youtube_link(chat_id, msg_id, js, replace_ext='mkv')

def reboot_media_server(params, chat_id, msg_id):
	Bot().send_message(chat_id, 'Rebooting MiniDLNA server.', msg_id=msg_id)
	spass = Config().read('sudo_password')
	os.popen("sudo -S minidlnad -R", 'w').write(spass)
	os.popen("sudo -S service minidlna restart", 'w').write(spass)

def remount_hdd(params, chat_id, msg_id):
	Bot().send_message(chat_id, 'Remounting HDDs.', msg_id=msg_id)
	os.popen("sudo -S mount -a", 'w').write(Config().read('sudo_password'))

def status_check(params, chat_id, msg_id):
	Bot().send_message(chat_id, 'OK!', msg_id=msg_id)

def reboot(params, chat_id, msg_id):
	Bot().send_message(chat_id, 'Rebooting...', msg_id=msg_id)
	os.popen("sudo -S shutdown -r", 'w').write(Config().read('sudo_password'))

def update(params, chat_id, msg_id):
	Bot().send_message(chat_id, 'Pulling updates...', msg_id=msg_id)
	remote_repo = Config().read('remote_repo')
	subprocess.run(f'git pull --no-edit {remote_repo}', shell=True)
	reboot(params, chat_id, msg_id)

def update_proxy(params, chat_id, msg_id):
	Bot().send_message(chat_id, 'Updating proxy...', msg_id=msg_id)
	_update_proxy()
	reboot(params, chat_id, msg_id)

def list_media_server(params, chat_id, msg_id):
	response = ''
	for i in os.listdir(get_media_server_path()):
		response += f'{i}\n'
	if response == '':
		response = 'Media server is empty.'
	Bot().send_message(chat_id, response, msg_id=msg_id)


def purge_base_directory(params, chat_id, msg_id):
	dir = Config().read('base_directory')
	for i in os.listdir(dir):
		shutil.rmtree(f'{ dir }/{ i }', ignore_errors=True)
		os.mkdir(f'{ dir }/{ i }')
	Bot().send_message(chat_id, 'Base directory has been purged.', msg_id=msg_id)


def download_torrent(params, chat_id, msg_id):
	subprocess.run(f'qbittorrent "{params}"', shell=True)
	Bot().send_message(chat_id, 'Starting torrent download...', msg_id=msg_id)


def get_media_server_path():
	base_dir = Config().read('base_directory')
	media_server_dir = Config().read('media_server_directory')
	return os.path.join(base_dir, media_server_dir)
