import os
import sys
import shutil
import subprocess
from subprocess import PIPE
from bs4 import BeautifulSoup
from time import sleep
from babelfish import Language
from subliminal import Video, download_best_subtitles, save_subtitles

def changedir(path=0):
	if (path == 0):
		path = os.path.realpath(__file__)
		path = path[:path.rindex("/")]
	os.chdir(path)


def parse_args(argv):
	path = " ".join(argv[1:])
	name = path[path.rindex('/') + 1:]
	return name, path


def download_subtitles(name):
	v = Video.fromname(name)
	subs = download_best_subtitles([v], {Language("eng")})
	save_subtitles(v, subs[v])
	return f"{name[:-4]}.en.srt"


def get_media_server_path():
	base_dir = Config().read('base_directory')
	media_server_dir = Config().read('media_server_directory')
	return os.path.join(base_dir, media_server_dir)


def move_to_server(filename):
	shutil.move(filename, f'{ get_media_server_path() }/{ filename }')


def embed_subs(vidfile, subfile):
	outfile = vidfile[:-4] + "[SUBBED].mkv"
	subprocess.run(["ffmpeg", "-i", vidfile, "-i", subfile,
					"-c", "copy", "-c:s", "srt", outfile])
	return outfile


def is_video(f):
	exts = ['.mkv', '.mp4', '.avi', '.m4v']
	for e in exts:
		if f.endswith(e):
			return True
	return False


def reencode_audio(vidfile):
	outfile = vidfile[:-4] + "[RENC].mkv"
	subprocess.run(["ffmpeg", "-i", vidfile, "-c:v",
					"copy", "-c:a", "ac3", outfile])
	return outfile


def get_audio_codec(vidfile):
	out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
						  "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", vidfile], stdout=PIPE).stdout
	return out.decode().strip()


def main():
	name, base_path = parse_args(sys.argv)
	bot = Bot()

	bot.send_master_message(f'{name} has been downloaded.')
	
	# only download subs for shows inside tvshows subdirectory
	bot.send_master_message(f'Waiting for subs for {name}.')

	sleep(int(Config().read('subs_wait_period')))
	
	for path, _dirs, files in os.walk(base_path, topdown=False):
		for vidfile in files:
			if is_video(vidfile):

				changedir(path)

				if get_audio_codec(vidfile) == 'eac3':
					vidfile = reencode_audio(vidfile)

				try:
					subfile = download_subtitles(vidfile)
					vidfile = embed_subs(vidfile, subfile)
				except:
					bot.send_master_message(f'Failed to encode subs for {vidfile}.')

		bot.send_master_message(f'{name} has finished being subbed.')


if __name__ == "__main__":
	changedir()
	sys.path.append('../')
	from bot import Bot
	from config import Config
	main()
