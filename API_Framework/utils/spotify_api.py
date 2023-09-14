# utils/spotify_api.py
from curses import echo
import requests
from base64 import b64encode
from config.config import *
import csv
import os

def get_bearer_token():
    """
    This function user client id and client secret and return bearer token
    """
    auth_header = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    data = {"grant_type": "client_credentials"}
    try:
        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        response_data = response.json()
        return response_data.get("access_token")
    except Exception as e:
        print(e)


def search_artist(artist_name, access_token):
    """
    This function search for the artists for the given artist name return its response
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"query": artist_name, "type": "artist", "limit": 1}
    try:
        response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
        return response.json()
    except Exception as e:
        print(e)

def get_top_tracks(artist_id, access_token):
    """
    This function search for the tracks using artist id and store track and artist info into csv file
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = SPOTIFY_TOP_TRACKS_URL.format(artist_id=artist_id)
    try:
        response = requests.get(url, headers=headers, params={"market": "in"})
        result=response.json()
        assert response.status_code == 200
        current_directory = os.getcwd()
        subfolder_path = os.path.join(current_directory, "outputs")
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(subfolder_path, "top_track.csv")
        with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Track Name", "Artist"])
                writer.writerow([result["tracks"][0]["id"], result["tracks"][0]["name"]])
        return response.json()
    except Exception as e:
        print(e)

def get_track_info(track_id, access_token):
    """
    This function search for the tracks info using track id
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = SPOTIFY_TRACK_URL.format(track_id=track_id)
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(e)

def invalid_search_artist(artist_name, access_token):
    """
    This function search for the artists for the given artist name return its response
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"query": artist_name, "type": "797679", "limit": 1, "value": "dummy"}
    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
    return response.status_code

def search_artist_with_dummy(artist_name, access_token):
    """
    This function search for the artists for the given artist name return its response
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"query": artist_name, "type": "797679", "limit": 1, "value": "dummy"}
    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
    return response.status_code


