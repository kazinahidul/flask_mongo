from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/user"

mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    if name and email and password and request.method == 'POST':
        hashedPassword = generate_password_hash(password)
        print(name)
        print(hashedPassword)
        id = mongo.db.test.insert_one({'name': name, 'email': email, 'password':hashedPassword})
        
        resp = jsonify("user added successfully")
        resp.status_code = 200

        return resp
    else:
        return not_found()

@app.route('/users', methods=['GET'])
def users():
    users = mongo.db.test.find()
    resp = dumps(users)
    return resp
@app.route('/user/<id>', methods=['GET'])
def user(id):
    user = mongo.db.test.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.test.delete_one({'_id':ObjectId(id)})
    resp = jsonify("user deleted successfully")

    resp.status_code = 200

    return resp

@app.route('/update/<id>', methods=['PUT'])
def edit(id):
    _id = id
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    if name and email and password and request.method == 'PUT':
        hashedPassword = generate_password_hash(password)

        mongo.db.test.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': name, 'email': email, 'password':hashedPassword}})
        resp = jsonify("user updated successfully")

        resp.status_code = 200
        return resp

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp




if __name__ == '__main__':
    app.run(debug=True, port=8000)