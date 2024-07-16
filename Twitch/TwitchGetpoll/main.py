from flask import Flask, request, jsonify
import time
import requests
import psycopg2
import os
from dotenv import load_dotenv
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

def tokendataget():
    connection, cursor = connect()
    if connection is None or cursor is None:
        print({'error': 'Database connection failed get data'},500)
        return jsonify({'error': 'Database connection failed'}), 500 
    else:
        print("GETTING DATABASE VALUES")
        cursor.execute('SELECT * FROM token')
        row = cursor.fetchone()
        print(row)
        cursor.close()
        connection.close()
        row_dict = {
        'access_token': row[0],
        'refresh_token': row[1],
        'expires_at': row[2]
    }
        return row_dict
    
def tokendataUpdate(access_value, refresh_value,expires_value):
     #Get DB VALUE FOR TWITCH
    connection, cursor = connect()
    if connection is None or cursor is None:
        print({'error': 'Database connection failed get update'},500)
        return jsonify({'error': 'Database connection failed'}), 500
    else:
        cursor.execute('SELECT * FROM token')
        row = cursor.fetchone()
        
        # UPDATE DATABASE
        print("UPDATING DATABASE VALUES")
        try:
            if not row:
                print("DB is not found")
                cursor.execute('INSERT INTO token (access_token, refresh_token, expires_at) VALUES (%s, %s, %s)', (access_value, refresh_value, expires_value))
                connection.commit()    
            else:
                print("DB is found in database")
                cursor.execute('UPDATE token SET access_token = %s, refresh_token = %s, expires_at = %s', (access_value,refresh_value, expires_value))
                connection.commit()
            connection.close()
            return 'Database updated sucess'
        except (Exception,psycopg2.DatabaseError) as e:
            print(f"An error occured: {e}")
            return 'Database updated Failed'
if __name__ == '__main__':
    app.run(debug=True)
