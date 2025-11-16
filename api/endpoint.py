import mysql.connector
import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://spotify-grabber-docker"])

mysql_host = os.getenv('MYSQL_HOST', 'mysql')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

def get_tracks_from_db():
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = connection.cursor()

    query = 'SELECT track_name, artist_names FROM tracks WHERE deleted = FALSE'
    cursor.execute(query)
    results = cursor.fetchall()

    tracks = [{'track_name': row[0], 'artist_names': row[1]} for row in results]

    cursor.close()
    connection.close()

    return tracks

def mark_track_deleted(track_name, artist_names):
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = connection.cursor()

    update_query = '''
    UPDATE tracks
    SET deleted = TRUE
    WHERE track_name = %s AND artist_names = %s
    '''
    cursor.execute(update_query, (track_name, artist_names))
    connection.commit()

    cursor.close()
    connection.close()

@app.route('/tracks', methods=['GET'])
def tracks_endpoint():
    tracks = get_tracks_from_db()
    return {'tracks': tracks}, 200

@app.route('/tracks/delete/<track_name>/<artist_names>', methods=['GET'])
def delete_track_endpoint(track_name, artist_names):
    mark_track_deleted(track_name, artist_names)
    return {'message': 'Track marked as deleted'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)