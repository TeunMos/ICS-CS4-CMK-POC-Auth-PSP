from flask import Flask, request, jsonify, render_template
import requests
import sqlite3


app = Flask(__name__)

tokeninfo_endpoint = 'http://localhost:3001/tokeninfo'
userinfo_endpoint = 'http://localhost:3001/userinfo'

dbfile = 'notes.db'

# read schema from file
with open('schema.sql', 'r') as f:
    schema = f.read()

    # create db
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    # create tables
    c.executescript(schema)
    conn.commit()
    conn.close()


def auth(id_token):
    # check if id token is valid and get the scope
    response = requests.get(tokeninfo_endpoint + '?id_token=' + id_token)

    if response.status_code == 200:
        return response.json()['scope']
    
    return None

def userinfo(id_token):
    # get userinfo
    response = requests.get(userinfo_endpoint + '?id_token=' + id_token)

    if response.status_code == 200:
        return response.json()
    
    return None

def savenote(userid, note):
    # save or update note to db
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()

    c.execute('SELECT * FROM notes WHERE user_id=?', (userid,))
    result = c.fetchone()

    if result is None:
        c.execute('INSERT INTO notes (user_id, note) VALUES (?, ?)', (userid, note))
    else:
        c.execute('UPDATE notes SET note=? WHERE user_id=?', (note, userid))

    conn.commit()
    conn.close()

    return True

def getnote(userid):
    # get note from db
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()

    c.execute('SELECT * FROM notes WHERE user_id=?', (userid,))
    result = c.fetchone()

    conn.close()

    if result is None:
        return None
    
    return result[2]


@app.route('/note', methods=['GET', 'POST'])
def notes():
    # get id_token from header
    id_token = request.headers.get('Authorization')
    if id_token is None:
        return jsonify({'error': 'Missing Authorization header'}), 400

    # check if id token is valid and get the scope
    scope = auth(id_token)

    print(scope)

    if scope is None:
        return jsonify({'error': 'Invalid token'}), 401
    if scope != 'notes.read' and scope != 'notes.manage':
        return jsonify({'error': 'Invalid permissions'}), 403
    
    # get userinfo
    user = userinfo(id_token)
    if user is None:
        return jsonify({'error': 'Invalid token'}), 401


    if request.method == 'GET':
        # get note from db by user id
        note = getnote(user['sub'])

        if note is None:
            return jsonify({'error': 'Note not found'}), 404
        
        return jsonify({'note': note}), 200

    elif request.method == 'POST':
        if scope != 'notes.manage':
            return jsonify({'error': 'Invalid permissions'}), 403

        # get note from request body
        note = request.form.get('note')

        # save note to db
        savenote(user['sub'], note)

        return jsonify({'succes': True}), 200
    
    return jsonify({'error': 'Invalid request'}), 400
        

if __name__ == '__main__':
    app.run(debug=True)