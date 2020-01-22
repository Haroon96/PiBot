import sys
import os
import re
import json
import requests
import unicodedata
from bs4 import BeautifulSoup
from googlesearch import search as gsearch
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TPE1, TALB, TPE2, USLT, APIC, TCON
from pathvalidate import sanitize_filename
from config import Config

def find_genius_data(title, genius_url):
    urls = [genius_url]

    # get top google result is no genius_url provided
    if genius_url is None:
        urls = gsearch(f'site:genius.com {title}', stop=1)

    for url in urls:
        r = requests.get(url)
        html = r.text
        
        # get song_id
        key = re.search(r'"Song ID":[0-9]+', html).group()
        song_id = re.search(r'[0-9]+', key).group()

        # get lyrics
        lyrics = ''
        genre = ''
        try:
            soup = BeautifulSoup(html, 'html.parser')
            lyrics = soup.find('div', attrs={'class': 'lyrics'}).text.strip()
            genre = json.loads(soup.find('meta', attrs={"itemprop":"page_data"})['content'])['dmp_data_layer']['page']['genres'][0]
        except Exception as e:
            print("Failed to fetch lyrics:", e)
            pass
            
        return (song_id, lyrics, genre)
        
def get_music_info(q, genius_url):
    token = Config().read('genius_api_token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # search for song
    song_id, lyrics, genre = find_genius_data(q, genius_url)

    # search song metadata
    r = requests.get(f'https://api.genius.com/songs/{song_id}', headers=headers)

    js = r.json()['response']['song']
    js['lyrics'] = lyrics
    js['genre'] = genre

    return js

def get_cover_art_url(music_info):
    if music_info['album'] is not None:
        return music_info['album']['cover_art_url']
    return music_info['song_art_image_url']

def get_album_info(music_info):
    if music_info['album'] is not None:
        return (music_info['album']['name'], music_info['album']['artist']['name'])
    return (f"{music_info['title']} - Single", music_info['primary_artist']['name'])

def get_title(music_info):
    title = music_info['title_with_featured'].replace('Ft.', 'feat.')
    return unicodedata.normalize('NFKD', title)

def rename_file(title, artist, oldfilepath):
    basepath, oldname = os.path.split(oldfilepath)
    _, ext = os.path.splitext(oldname)
    newname = sanitize_filename(f'{artist} - {title}{ext}')
    newfilepath = os.path.join(basepath, newname)
    os.rename(oldfilepath, newfilepath)
    return newfilepath

def embed_music_metadata(title, filename, genius_url=None):
    try:

        music_info = get_music_info(title, genius_url)

        mp3 = MP3(filename)

        title = get_title(music_info)
        artist = music_info['primary_artist']['name']

        mp3['TIT2'] = TIT2(encoding=3, text=[title])
        mp3['TPE1'] = TPE1(encoding=3, text=[artist])

        album_name, album_artist = get_album_info(music_info)
        mp3['TALB'] = TALB(encoding=3, text=[album_name])
        mp3['TPE2'] = TPE2(encoding=3, text=[album_artist])

        mp3['TCON'] = TCON(encoding=3, text=[music_info['genre']])
        mp3['USLT::XXX'] = USLT(encoding=1, lang='XXX', desc='', text=music_info['lyrics'])

        try:
            artwork = requests.get(get_cover_art_url(music_info), stream=True)
            mp3['APIC:'] = APIC(encoding=3, mime="image/jpeg", type=3, desc='', data=artwork.raw.read())
        except Exception as e:
            print(f"Failed to embed artwork for title: {title}", e)

        mp3.save()

        return f'{artist} - {title}', rename_file(title, artist, filename)

    except Exception as e:
        print(f"Failed to encode music data for title: {title}", e)

    return title, filename
