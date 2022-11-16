import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS


ADDRESS = [
    {
        'id': uuid.uuid4().hex,
        'address': '123 PLACE RD',
        'name': 'Jack Kerouac',
        'read': True
    }
]


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def remove_address(address_id):
    for address in ADDRESS:
        if address['id'] == address_id:
            ADDRESS.remove(address)
            return True
    return False


@app.route('/addresss', methods=['GET', 'POST'])
def all_addresss():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        ADDRESS.append({
            'id': uuid.uuid4().hex,
            'address': post_data.get('address'),
            'name': post_data.get('name'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['addresss'] = ADDRESS
    return jsonify(response_object)


@app.route('/addresss/<address_id>', methods=['PUT', 'DELETE'])
def single_address(address_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_address(address_id)
        ADDRESS.append({
            'id': uuid.uuid4().hex,
            'address': post_data.get('address'),
            'name': post_data.get('name'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_address(address_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
