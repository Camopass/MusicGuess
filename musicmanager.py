from xml.etree import ElementTree

import requests
from song import Song


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
        "limit": 5,
        "period": "overall",
    }

    resp = requests.get(url, params=params).json()

    top_songs = resp['toptracks']['track']
    top_songs_formatted = [Song(song["name"], 
                                song["artist"]["name"], 
                                song["playcount"],
                                name,
                                [],
                                get_image_url(song))
                           for song in top_songs]
    return top_songs_formatted

def get_image_url(song):
    mb_url = "https://musicbrainz.org/ws/2/release"
    search = f"artist:{song['artist']['name']} AND release:{song['name']}"
    mb_params = {
        "query": search,
        "format": "json",
    }
    mb_resp = requests.get(mb_url, params=mb_params).content
    try:
        root = ElementTree.fromstring(mb_resp)
        mbid = root[0][0].attrib.get("id")
    except:
        return "https://webstockreview.net/images/square-clipart-grey.png"
    return f"https://coverartarchive.org/release/{mbid}/"

def get_image(song):
    mb_url = "https://musicbrainz.org/ws/2/release"
    mb_params = {
        "query": f"artist:{song.artist} AND release:{song.title}",
        "format": "json",
    }
    mb_resp = requests.get(mb_url, params=mb_params).content
    try:
        root = ElementTree.fromstring(mb_resp)
        mbid = root[0][0].attrib.get("id")
        url = f"https://coverartarchive.org/release/{mbid}/"
    except:
        url = "https://webstockreview.net/images/square-clipart-grey.png"
    headers = {
        "User-Agent": "MusicGuess/0.01 (camopass@gmail.com)"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp = resp.json()
        image_url = resp['images'][0]['image']
        return requests.get(image_url).content
    else:
        with open('assets/covernotfound.png', 'rb') as f:
            return f.read()