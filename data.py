import sqlite3
import io
import glob
import os.path
from os.path import basename
import numpy as np
import face_recognition


def import_and_train_data():
    sql = '''INSERT INTO PERSONS (name, arr, picture) VALUES(?, ?, ?);'''
    cur = CONN.cursor()
    for picture_file in glob.glob('picturesTraining/*.jpg'):
        name = os.path.splitext(basename(picture_file))[0]
        if not cur.execute("SELECT name FROM persons WHERE name=?", (name, )).fetchone():
            print(name, ' is new.. Trains')
            with open(picture_file, 'rb') as input_file:
                ablob = input_file.read()
                image = face_recognition.load_image_file(picture_file)
                face_encoding = face_recognition.face_encodings(image)[0]
                CONN.execute(sql, [name, face_encoding, sqlite3.Binary(ablob)])
                print('done with: ', name)
        else:
            print(name, ' allready exist!')
    CONN.commit()


def create_or_open_db(db_file):
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("array", convert_array)
    connection = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    sql = '''CREATE TABLE if not exists PERSONS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
        name           TEXT    NOT NULL,
        lastvisit       TEXT            ,
        arr   array    NOT NULL,
        picture         BLOB);'''
    connection.execute(sql)
    return connection


def export_data():
    sql = "SELECT name, arr FROM PERSONS"
    cur = CONN.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    return result



def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

CONN = create_or_open_db('db.persons')
import_and_train_data()
