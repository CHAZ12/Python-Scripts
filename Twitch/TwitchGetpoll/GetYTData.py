from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv
import os
import time
import werkzeug
import json
#from config import config
load_dotenv
app = Flask(__name__)


# Retrieve database configuration from environment variables
db_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'database': os.getenv('POSTGRES_DATABASE'),
    'port': int(5432),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}

def connect():
    try:
        #params = config()
        params = db_config
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Database connection failed connect: {error}')
        return None, None

def GetYTIDs():
    connection, cursor = connect()
    if connection is None or cursor is None:
        print({'error': 'Database connection failed get data'},500)
        return jsonify({'error': 'Database connection failed'}), 500 
    try:
        print("GETTING DATABASE VALUES")
        cursor.execute('SELECT * FROM token')
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        row_dict = {
        'continuation': row[3],
        'videoid': row[4]
        }
        return row_dict
    except:
        return None
    
    
    
def YTIDsUpdate(video_id, continuation):
     #Get DB VALUE FOR TWITCH
    connection, cursor = connect()
    if connection is None or cursor is None:
        print({'error': 'Database connection failed get update'})
        return jsonify({'error': 'Database connection failed'})
    else:
        cursor.execute('SELECT * FROM token')
        row = cursor.fetchone()
        
        # UPDATE DATABASE
        print("UPDATING DATABASE VALUES")
        try:
            if not row:
                print("DB is not found")
                cursor.execute('INSERT INTO token (videoid, continuation) VALUES (%s, %s)', (video_id, continuation))
                connection.commit()    
            else:
                print("DB is found in database")
                cursor.execute('UPDATE token SET videoid = %s, continuation = %s', (video_id, continuation))
                connection.commit()
            connection.close()
            return 'Database updated success'
        except (Exception,psycopg2.DatabaseError) as e:
            print(f"An error occured: {e}")
            return 'Database updated Failed'
if __name__ == '__main__':
    app.run(debug=True)
