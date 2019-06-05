from bot import Bot
import commands

def add_command(cmd, action, info):
	command_dict[cmd] = {'action': action, 'info': info}


def init_commands():
	add_command('adl', commands.download_youtube_audio, 'Download audio from Youtube')
	add_command('vdl', commands.download_youtube_video, 'Download video from Youtube')
	add_command('rms', commands.reboot_media_server, 'Reboot MiniDLNA server')
	add_command('status', commands.status_check, 'Check the status of the bot')
	add_command('reboot', commands.reboot, 'Reboot the device')
	add_command('upd', commands.update, 'Update code (Pull from remote repo)')
	add_command('lms', commands.list_media_server, 'List the media available in media server directory')
	add_command('pbd', commands.purge_base_directory, 'Clear base directory')
	add_command('upx', commands.update_proxy, 'Fetch a new proxy')
	add_command('qbt', commands.download_torrent, 'Download torrents using qBittorrent')

def generate_help():
	ref = ''
	for cmd in command_dict:
		ref += f"`{cmd}`: {command_dict[cmd]['info']}\n\n"
	return ref

def interpret(msg, chat_id):
	args = msg.split(' ')
	
	cmd = args[0].lower()
	params = ''.join(args[1:])

	if cmd == 'help':
		Bot().send_message(chat_id, generate_help())
	elif cmd in command_dict:
		command_dict[cmd]['action'](params, chat_id)
	else:
		Bot().send_message(chat_id, "Unrecognized command")


command_dict = {}
init_commands()
