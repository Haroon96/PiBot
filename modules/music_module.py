from bs4 import BeautifulSoup
from googlesearch import search as gsearch
#from config import Config
import requests
import eyed3
import sys
import os
import re

def find_genius_data(title):
    # get top google result
    search_result = gsearch(f'site:genius.com {title}', stop=1)
    for url in search_result:
        r = requests.get(url)
        html = r.text
        
        # get song_id
        key = re.search(r'"Song ID":[0-9]+', html).group()
        song_id = re.search(r'[0-9]+', key).group()

        # get lyrics
        lyrics = ''
        try:
            lyrics = BeautifulSoup(html, 'html.parser').find('div', attrs={'class': 'lyrics'}).text
        except Exception as e:
            print("Failed to fetch lyrics:", e)
            pass
            
        return (song_id, lyrics)
        
def get_music_info(q):
    token = Config().read('genius_api_token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # search for song
    song_id, lyrics = find_genius_data(q)

    # search song metadata
    r = requests.get(f'https://api.genius.com/songs/{song_id}', headers=headers)

    js = r.json()['response']['song']
    js['lyrics'] = lyrics

    return js

def get_cover_art_url(music_info):
    if 'cover_art_url' in music_info['album']:
        return music_info['album']['cover_art_url']
    return music_info['song_art_image_url']

def embed_music_metadata(title, filename):
    try:

        music_info = get_music_info(title)
        art = requests.get(get_cover_art_url(music_info), stream=True)

        audio_file = eyed3.load(filename)

        audio_file.tag.title = music_info['title']
        audio_file.tag.artist = music_info['primary_artist']['name']
        audio_file.tag.album = music_info['album']['name']
        audio_file.tag.lyrics.set(music_info['lyrics'])
        audio_file.tag.images.set(3, art.raw.read(), 'image/jpeg', '"Album Cover"')

        audio_file.tag.save()

    except Exception as e:
        print(f"Failed to encode music data for title: {title}", e)