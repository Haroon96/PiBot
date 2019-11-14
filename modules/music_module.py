from bs4 import BeautifulSoup
from config import Config
import requests
import eyed3
import sys
import os

def get_music_info(q):
    token = Config().read('genius_api_token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # search for song
    r = requests.get('https://api.genius.com/search', params={'q': q}, headers=headers)
    song_id = r.json()['response']['hits'][0]['result']['id']
    # search song metadata
    r = requests.get(f'https://api.genius.com/songs/{song_id}', headers=headers)

    return r.json()['response']['song']

def embed_music_metadata(title, filename):
    try:

        music_info = get_music_info(title)
        art = requests.get(music_info['album']['cover_art_url'], stream=True)

        audio_file = eyed3.load(filename)

        audio_file.tag.title = music_info['title']
        audio_file.tag.artist = music_info['primary_artist']['name']
        audio_file.tag.album = music_info['album']['name']
        audio_file.tag.images.set(3, art.raw.read(), 'image/jpeg')

        audio_file.tag.save()

    except Exception as e:
        print(e)