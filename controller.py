from bot import Bot
import commands
from config import Config
from threading import Thread, Semaphore

config = Config()
bot = Bot()

def add_command(cmd, action, info, admin_only=False):
	command_dict[cmd] = {'action': action, 'info': info, 'admin': admin_only}

def init_commands():
	add_command('mdl', commands.download_youtube_audio, 'Download music from YouTube')
	add_command('vdl', commands.download_youtube_video, 'Download video from YouTube')
	add_command('rms', commands.reboot_media_server, 'Reboot MiniDLNA server', True)
	add_command('status', commands.status_check, 'Check the status of the bot')
	add_command('reboot', commands.reboot, 'Reboot the device', True)
	add_command('upd', commands.update, 'Update code (Pull from remote repo)', True)
	add_command('lms', commands.list_media_server, 'List the media available in media server directory')
	add_command('pbd', commands.purge_base_directory, 'Clear base directory', True)
	add_command('qbt', commands.download_torrent, 'Download torrents using qBittorrent')

def generate_help():
	ref = ''
	for cmd in command_dict:
		ref += f"`{cmd}`: {command_dict[cmd]['info']}\n\n"
	return ref

def run_command(method, args):
	semaphore.acquire()
	method(*args)
	semaphore.release()

def start_thread(method, args):
	Thread(target=run_command, args=(method, args,)).start()

def interpret(msg, chat_id):
	args = msg['text'].split()

	cmd = args[0].lower()
	msg_id = msg['message_id']
	params = ' '.join(args[1:])

	if cmd in command_dict:
		command = command_dict[cmd]

		# check if command is admin only
		if command['admin'] and chat_id not in config.read('admin_chat_ids'):
			start_thread(bot.send_message, (chat_id, "Unauthorized command!",))
		else:
			start_thread(command_dict[cmd]['action'], (params, chat_id, msg_id))
	else:
		# unrecognized command, send help prompt 
		start_thread(bot.send_message, (chat_id, generate_help(),))
	
# init commands
command_dict = {}
init_commands()

# init semaphore
semaphore = Semaphore(config.read('thread_limit'))
