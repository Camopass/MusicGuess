import requests
import os


def download_song(name):
    url = "https://itunes.apple.com/search"

    params = dict(
        term=name,
        media="music",
        entity="song"
    )

    resp = requests.get(url, params=params)
    data = resp.json()

    print(data)

    preview_url = data['results'][0]['previewUrl']

    with open(f'./previews/{name.replace(" ", "_")}.aac', 'wb') as f:
        f.write(requests.get(preview_url).content)

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

    resp = requests.get(url, params=params)

    print(resp.content)

