import requests
import MusicManager
import os
from dotenv import load_dotenv, find_dotenv


def main():
    load_dotenv(find_dotenv())
    api_key = os.getenv("API_KEY")
    print(api_key)
    MusicManager.get_top_songs("ThatGoblinKing", api_key)


if __name__ == '__main__':
    main()