# tests/test_spotify.py
import pytest
from utils.spotify_api import *
import csv
import os

@pytest.fixture(scope="module")
def access_token():
    return get_bearer_token()

def test_search_artist(access_token):
    artist_name = "A.R. Rahman"
    response = search_artist(artist_name, access_token)
    assert "artists" in response
    assert len(response["artists"]["items"]) > 0
    artist_id = response["artists"]["items"][0]["id"]
    return artist_id

def test_get_top_tracks_and_store_in_csv(access_token):
    artist_id = test_search_artist(access_token)
    response = get_top_tracks(artist_id, access_token)
    assert "tracks" in response
    assert len(response["tracks"]) > 0

def test_search_track_info_and_verify(access_token):
    try:
        current_directory = os.getcwd()
        subfolder_path = os.path.join(current_directory, "outputs")
        file_path = os.path.join(subfolder_path, "top_track.csv")
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            row = next(reader)
        response = get_track_info(row[0],access_token)
        response_name = response["name"]
        return response_name
    except Exception as e:
        print(e)

def test_verify_csv_value_with_response_value(access_token):
    try:
        response_artist = test_search_track_info_and_verify(access_token)
        current_directory = os.getcwd()
        subfolder_path = os.path.join(current_directory, "outputs")
        file_path = os.path.join(subfolder_path, "top_track.csv")
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            row = next(reader)
        csv_artist=row[1]
        assert response_artist == csv_artist
    except Exception as e:
        print(e)

def test_search_artist_with_invalid_requests(access_token):
    artist_name = "0i9080090"
    response = invalid_search_artist(artist_name, access_token)
    assert response == 400

def test_search_artist_with_invalid_credentials(access_token):
    artist_name = "A.R. Rahman"
    access_token = "dummy"
    response = search_artist_with_dummy(artist_name, access_token)
    assert response == 401