from logging import root
from xml.etree import ElementTree

import requests
import Song


def download_song(song):
    url = "https://itunes.apple.com/search"

    params = dict(
        term=f"{song.artist} - {song.title}",
        media="music",
        entity="song"
    )

    resp = requests.get(url, params=params)
    data = resp.json()

    preview_url = data['results'][0]['previewUrl']

    filepath = f'./previews/{song.artist.replace(" ", "_")}_{song.title.replace(" ", "_")}.aac'
    with open(filepath, 'wb') as f:
        f.write(requests.get(preview_url).content)
    return filepath

def get_top_songs(name, api_key):
    url = "https://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "user.gettoptracks",
        "user": name,
        "api_key": api_key,
        "format": "json",
        "limit": 100,
        "period": "overall",
    }

    resp = requests.get(url, params=params).json()
    top_songs = resp['toptracks']['track']
    top_songs_formatted = [Song.Song(song["name"], song["artist"]["name"], song["playcount"])
                           for song in top_songs]
    return top_songs_formatted

def get_image(song):
    mb_url = "https://musicbrainz.org/ws/2/release"
    mb_params = {
        "query": f"artist:{song.artist} AND release:{song.title}",
        "format": "json",
    }
    mb_resp = requests.get(mb_url, params=mb_params).content
    root = ElementTree.fromstring(mb_resp)
    id = root[0][0].attrib.get("id")
    url = f"https://coverartarchive.org/release/{id}/"
    headers = {
        "User-Agent": "MusicGuess/0.01 (camopass@gmail.com)"
    }
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    print(resp.content)
    resp = resp.json()
    image_url = resp['images'][0]['image']
    return requests.get(image_url).content