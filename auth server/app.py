from flask import Flask, request, jsonify, render_template

from services.scopes import scopesObject
from services.authorisationManager import authorisationManager
from services.tokenmanager import tokenManager
from services.userDBManager import userDBMan

from models.user import user


authMan = authorisationManager()
tokenMan = tokenManager()

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
    
    # validate login and get acces token
    acces_token = authMan.validateLogin(username, password, scope)
    
    if 'error' in acces_token:
        return jsonify(acces_token), 401
    
    acces_token = acces_token['acces_token']
    
    # get user from db
    DBuser = userDBMan().getUserbyUsername(username)

    # create user object
    user_ = user(DBuser[1], DBuser[3], DBuser[0])

    # generate id token
    id_token = tokenMan.GenerateIDToken(user_, scope, acces_token)

    # return id token
    return jsonify({'id_token': id_token}), 200


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    # get form data
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'Missing username, password or email'}), 400
    
    user_ = user(username, email)

    # register user
    result = authMan.createUser(user_, password)

    if result:
        return jsonify({'succes': 'user created succesfully'}), 200
    else:
        return jsonify({'error': 'Something went wrong'}), 500


if __name__ == '__main__':
    # move current directory to the directory of this file 
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # run app
    app.run(debug=True, port=3000)
