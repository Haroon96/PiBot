import os
import sys
import shutil
import subprocess
from subprocess import PIPE
from bs4 import BeautifulSoup
from time import sleep
from babelfish import Language
from subliminal import Video, download_best_subtitles, save_subtitles

def changedir(path=None):
	if path is None:
		# move to directory of the script file to allow imports
		path = os.path.realpath(__file__)
		# __file__ contains file name too, only fetch the base path
		path = os.path.split(path)[0]
	os.chdir(path)


def parse_args(argv):
	# get path from arguments
	path = argv[1]
	# extract torrent name from path (basename of path)
	name = os.path.basename(os.path.normpath(path))
	return name, path


def download_subtitles(name):
	# download subtitles using subliminal
	v = Video.fromname(name)
	subs = download_best_subtitles([v], {Language("eng")})
	save_subtitles(v, subs[v])
	return f"{name[:-4]}.en.srt"


def get_media_server_path():
	# build media_server_path and return
	base_dir = config.read('base_directory')
	media_server_dir = config.read('media_server_directory')
	return os.path.join(base_dir, media_server_dir)


def encode_subs(vidfile, subfile):
	# extract filename and extension from vidfile
	filename, ext = os.path.splitext(vidfile)
	# build new filename
	outfile = f"{filename}[SUBBED].mkv"
	# use ffmpeg to encode subtitles
	p = subprocess.run(["ffmpeg", "-i", vidfile, "-i", subfile,
					"-c", "copy", "-c:s", "srt", outfile])
	
	if p.returncode != 0:
		raise Exception('Subs encoding failed')

	return outfile


def is_video(f):
	_, ext = os.path.splitext(f)
	return ext in ['.mkv', '.mp4', '.avi', '.m4v']


def reencode_audio(vidfile):
	# extract filename and extension from vidfile
	filename, ext = os.path.splitext(vidfile)
	# build new filename
	outfile = f"{filename}[RENC].mkv"
	# use ffmpeg to re-encode audio
	subprocess.run(["ffmpeg", "-i", vidfile, "-c:v",
					"copy", "-c:a", "ac3", outfile])
	return outfile


def get_audio_codec(vidfile):
	# get name of audio codec
	out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
						  "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", vidfile], stdout=PIPE).stdout
	return out.decode().strip()


def main():

	# get location of download
	name, root_path = parse_args(sys.argv)

	bot = Bot()
	
	# inform user that the torrent has downloaded
	bot.send_master_message(f'{name} has been downloaded.')

	# search for videos in the download path
	videos = []
	for path, _dirs, files in os.walk(root_path, topdown=False):
		for f in files:
			if is_video(f):
				videos.append(f)

	# end program if there are no videos in the download
	if len(videos) == 0:
		return

	# inform user and wait for subs_wait_period
	bot.send_master_message(f'Waiting for subs for {name}.')
	sleep_for = int(config.read('subs_wait_period'))
	sleep(sleep_for)
	
	# for each video in the download path
	for vidfile in videos:

		# change to video dir
		changedir(path)

		# if the audio is eac3, re-encode to ac3
		# eac3 is generally unsupported by Sony Bravia devices
		if get_audio_codec(vidfile) == 'eac3':
			# save original file name
			tmpvidfile = vidfile
			# re-encode audio to ac3 and update file name
			vidfile = reencode_audio(vidfile)
			# delete original file
			os.remove(tmpvidfile)

		try:
			# download subtitles for the video using subliminal
			subfile = download_subtitles(vidfile)
			# encode subs into the video file using ffmpeg
			vidfile = encode_subs(vidfile, subfile)
			# inform user of successful encoding
			bot.send_master_message(f'Successfully encoded subs for {vidfile}.')
		except:
			# inform user of failure
			bot.send_master_message(f'Failed to encode subs for {vidfile}.')

if __name__ == "__main__":
	# move to script dir to allow local imports
	changedir()
	sys.path.append('../')
	from bot import Bot
	from config import Config

	# create a new global config object
	global config
	config = config
	
	main()
