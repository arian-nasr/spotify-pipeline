import mysql.connector
import os
from flask import Flask

app = Flask(__name__)

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

    query = 'SELECT track_name, artist_names FROM tracks'
    cursor.execute(query)
    results = cursor.fetchall()

    tracks = [{'track_name': row[0], 'artist_names': row[1]} for row in results]

    cursor.close()
    connection.close()

    return tracks

@app.route('/tracks', methods=['GET'])
def tracks_endpoint():
    tracks = get_tracks_from_db()
    return {'tracks': tracks}, 200

if __name__ == '__main__':
    app.run()