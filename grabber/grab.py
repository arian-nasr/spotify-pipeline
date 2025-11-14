import requests
import os
import json
import mysql.connector

client_id = os.getenv('SP_CLIENT_ID')
client_secret = os.getenv('SP_CLIENT_SECRET')
playlist_id = os.getenv('SP_PLAYLIST_ID')
mysql_host = os.getenv('MYSQL_HOST', 'mysql')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

# need to add proper error handling later
def get_spotify_token():
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
    )
    auth_response.raise_for_status()
    return auth_response.json().get('access_token', '')

access_token = get_spotify_token()

# need to add proper error handling later
def grab_playlist(playlist_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(
        f'https://api.spotify.com/v1/playlists/{playlist_id}',
        headers=headers
    )
    response.raise_for_status()
    return response.json()

playlist_data = grab_playlist(playlist_id)

# Connect to MySQL and store track names and all artist names
def store_tracks_in_db(playlist_data):
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = connection.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tracks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        track_name VARCHAR(255),
        artist_names VARCHAR(255),
        UNIQUE KEY unique_track (track_name, artist_names)
    )
    '''
    cursor.execute(create_table_query)

    insert_query = '''
    INSERT IGNORE INTO tracks (track_name, artist_names)
    VALUES (%s, %s)
    '''

    for item in playlist_data['tracks']['items']:
        track_name = item['track']['name']
        artist_names = ', '.join(artist['name'] for artist in item['track']['artists'])
        cursor.execute(insert_query, (track_name, artist_names))

    connection.commit()
    cursor.close()
    connection.close()

store_tracks_in_db(playlist_data)