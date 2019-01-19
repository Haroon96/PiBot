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


def move_to_server(filename):
	shutil.move(filename, Config().read('media_server_path') + "/" + filename)


def copy_to_server(filename):
	shutil.copy(filename,  Config().read('media_server_path') + "/" + filename)


def embed_subs(vidfile, subfile):
	outfile = vidfile[:-4] + "[SUBBED].mkv"
	subprocess.run(["ffmpeg", "-i", vidfile, "-i", subfile,
					"-c", "copy", "-c:s", "srt", outfile])
	return outfile


def search(ext):
	files = os.listdir()
	for f in files:
		if f.endswith(ext):
			return f
	return 0


def get_vid_filename():
	exts = ['.mkv', '.mp4', '.avi']
	for e in exts:
		f = search(e)
		if (f != 0):
			return f
	return 0


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
	name, path = parse_args(sys.argv)

	bot = Bot()

	# only download subs for shows inside tvshows subdirectory
	if "/tvshows" in path:
		bot.send_master_message(f'Waiting for subs for {name}')
		print(path)
		changedir(path)
		origvidfile = get_vid_filename()

		if get_audio_codec(origvidfile) == 'eac3':
			tmpvidfile = origvidfile
			origvidfile = reencode_audio(origvidfile)
			os.remove(tmpvidfile)

		sleep(3*60*60) # sleep for 3 hours for subs to be available

		try:
			subfile = download_subtitles(origvidfile)
			subbedvidfile = embed_subs(origvidfile, subfile)
		except:
			bot.send_master_message(f'Failed to encode subs for {name}')
		finally:
			move_to_server(subbedvidfile)
			os.remove(origvidfile)

	bot.send_master_message(f'{name} has finished downloading')


if __name__ == "__main__":
	changedir()
	sys.path.append('../')
	from bot import Bot
	from config import Config
	main()
