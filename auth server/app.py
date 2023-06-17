from flask import Flask, request, jsonify, render_template
import sqlite3
from services.scopes import scopesObject

app = Flask(__name__, static_url_path='/static', static_folder='static')

scopelist = scopesObject()

@app.route('/auth', methods=['GET'])
def auth():
    # get url parameters
    redirect_url = request.args.get('redirect_url')
    scope = request.args.get('scope')

    if scope is None:
        return jsonify({'error': 'Missing scope parameter'}), 400

    if not redirect_url:
        return jsonify({'error': 'Missing redirect_url parameter'}), 400
    
    if not scopelist.validate_scope(scope):
        return jsonify({'error': 'Invalid scope parameter'}), 400
    
    scope_description = scopelist.get_scope_description(scope)

    redirect_base_url = redirect_url.split('/')[2] 


    # render the template with the parameters
    return render_template('auth.html', redirect_url=redirect_url, url=redirect_base_url, scope=scope, scope_description=scope_description)

@app.route('/login', methods=['POST'])
def login():
    # get form data
    username = request.form.get('username')
    password = request.form.get('password')
    redirect_url = request.form.get('redirect_url')
    scope = request.form.get('scope')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    if not redirect_url:
        return jsonify({'error': 'Missing redirect_url parameter'}), 400

    if not scopelist.validate_scope(scope):
        return jsonify({'error': 'Invalid scope parameter'}), 400
    
    # check if the user exists
    # if not, return an error
    # if yes, return the user id
    user_id = 1

    # redirect to the redirect_url with the user_id and the scope as url parameters
    return jsonify({'user_id': user_id, 'scope': scope}), 200


if __name__ == '__main__':
    # move current directory to the directory of this file
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # run app
    app.run(debug=True, port=3000)
