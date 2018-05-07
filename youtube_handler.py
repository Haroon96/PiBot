import subprocess

def handle(id, text):
	subprocess.Popen('youtube-dl -x --audio-format mp3 --audio-quality 0 --exec "python3 send_audio.py ' + str(id) + ' {}" ' + text, shell=True)
