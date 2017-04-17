import flask
from dbconnector import dbconnector
from flask_httpauth import HTTPBasicAuth


app = flask.Flask(__name__)  # create an instance of the Flask application
auth = HTTPBasicAuth()
connector = dbconnector.sqliteConnector("data/Quoterly.db")


@app.route('/users', methods=['POST'])
def add_user():
    if not flask.request.json or 'username' not in flask.request.json or 'email' not in flask.request.json or 'password' not in flask.request.json:
        flask.abort(400)  # the request body missing one of the fields
    if not connector.is_available_user(flask.request.json['username'], flask.request.json['email']):
        flask.abort(403)  # such user already exists or some of the fields have wrong data
    connector.add_user(flask.request.json['username'], flask.request.json['email'], flask.request.json['password'])  # call the database connector method to add new user
    return flask.jsonify({'user':
                         {
                             'username': flask.request.json['username'],
                             'email': flask.request.json['email'],
                             'passhash': flask.request.json['password']
                         }})


@app.route('/users/<string:username>', methods=['GET'])
def get_user_data(username):
    user_data = connector.get_user(username)
    return flask.jsonify({'user': {
        'login': user_data[0],
        'email': user_data[1],
        'reg_date': user_data[2],
        'is_admin': user_data[4]
    }})


cur_user = None


@app.route('/users/<string:username>/update', methods=['POST'])
@auth.login_required
def update_user(username):
    if connector.is_admin(cur_user):
        if not flask.request.json:
            connector.delete_user(username)
            return flask.jsonify({"result": "deleted"})
        if 'is_admin' in flask.request.json:
            connector.update_user(username, 'is_admin', flask.request.json['is_admin'])
        if 'email' in flask.request.json:
            connector.update_user(username, 'email', flask.request.json['email'])
        if 'password' in flask.request.json:
            connector.update_user(username, 'pass_hash', flask.request.json['password'])
    elif cur_user == username:
        if not flask.request.json:
            connector.delete_user(username)
            return flask.jsonify({"result": "deleted"})
        if 'email' in flask.request.json:
            connector.update_user(username, 'email', flask.request.json['email'])
        if 'password' in flask.request.json:
            connector.update_user(username, 'pass_hash', flask.request.json['password'])
    else:
        flask.abort(403)
    return get_user_data(username)


@auth.verify_password
def verify_password(username, password):
    global cur_user
    vaild_user = connector.match_password(username, password)
    if not vaild_user:
        return False
    cur_user = username
    return True


@app.route('/quotes/add', methods=['POST'])
@auth.login_required
def add_quote():
    if not flask.request.json or 'quote_text' not in flask.request.json or 'author' not in flask.request.json:
        flask.abort(400)
    data = connector.add_quote(flask.request.json['quote_text'], flask.request.json['author'], cur_user)
    return flask.jsonify({'quote': {
        'id': data[0],
        'quote_text': data[1],
        'author': data[2],
        'username': data[3],
        'pub_date': data[4]
    }})


@app.route('/quotes/random', methods=['GET'])
def get_random_quote():
    quote = connector.get_random_quote()
    if not quote:
        flask.abort(404)
    return flask.jsonify({'quote': {
        'id': quote[0],
        'quote_text': quote[1],
        'author': quote[2],
        'username': quote[3],
        'pub_date': quote[4]
    }})


@app.route('/quotes/<int:quote_id>', methods=['GET'])
# set the address and methods of the following function
def get_quote_by_id(quote_id):
    quote = connector.get_quote_by_id(quote_id)
    if not quote:
        flask.abort(404)
    return flask.jsonify({'quote': {
        'id': quote[0],
        'quote_text': quote[1],
        'author': quote[2],
        'username': quote[3],
        'pub_date': quote[4]
    }})


@app.route('/quotes/user/<string:quote_username>', methods=['GET'])
def get_quotes_by_user(quote_username):
    quotes = connector.get_quotes_by_user(quote_username)
    if not quotes:
        flask.abort(404)
    return flask.jsonify({'quotes':
                        [
                            {
                                 'id': quote[0],
                                 'quote_text': quote[1],
                                 'author': quote[2],
                                 'username': quote[3],
                                 'pub_date': quote[4]
                            }
                        for quote in quotes]})


@app.route('/quotes/<int:quote_id>/update', methods=['POST'])
@auth.login_required
def update_quote(quote_id):
    if connector.is_admin(cur_user):
        if not flask.request.json:
            connector.delete_quote(quote_id)
            return flask.jsonify({"result": "deleted"})
        if 'quote_text' in flask.request.json:
            connector.update_quote_field(quote_id, 'quote_text', flask.request.json['quote_text'])
        if 'author' in flask.request.json:
            connector.update_quote_field(quote_id, 'author', flask.request.json['author'])
    elif cur_user == connector.get_user_by_quote(quote_id):
        if not flask.request.json:
            connector.delete_quote(quote_id)
            return flask.jsonify({"result": "deleted"})
        if 'quote_text' in flask.request.json:
            connector.update_quote_field(quote_id, 'quote_text', flask.request.json['quote_text'])
        if 'author' in flask.request.json:
            connector.update_quote_field(quote_id, 'author', flask.request.json['author'])
    else:
        flask.abort(403)
    return get_quote_by_id(quote_id)


@app.errorhandler(404)
def not_found(e):
    return flask.jsonify({'error': 'not found'})


@app.errorhandler(403)
def access_forbidden(e):
    return flask.jsonify({'error': 'access forbidden'})


@app.errorhandler(400)
def bad_request(e):
    return flask.jsonify({'error': 'bad request'})


@auth.error_handler
def unauthorized_access():
    return flask.jsonify({'error': 'authorization required'})


if __name__ == '__main__':  # run only launched this file
    app.run(debug=False)
