from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

sessions = {}


@app.route('/start_session', methods=['POST'])
def start_session():
    data = request.get_json()
    print(data)
    code = data.get('code')
    if code in sessions:
        return jsonify({'message': 'Session with code already exists'}), 400
    else:
        # You can add more session details if needed
        sessions[code] = {'participants': []}
        return jsonify({'message': 'Session started successfully'}), 201


@app.route('/join_session', methods=['POST'])
def join_session():
    data = request.get_json()
    print(data)
    code = data.get('code')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        name = data.get('name')
        sessions[code]['participants'].append(name)
        return jsonify({'message': 'Joined session successfully'}), 200


@app.route('/get_participants', methods=['GET'])
def get_participants():
    code = request.args.get('code')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        participants = sessions[code]['participants']
        return jsonify({'participants': participants}), 200


if __name__ == '__main__':
    app.run(debug=True)
