from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


# List to simulate a database for storing participant data
participants_data = []

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
        # Generate a unique ID for the participant
        participant_id = str(uuid.uuid4())

        # Save participant data to the list (simulate database)
        participant_data = {
            'id': participant_id,
            'name': data.get('name'),
            'weight': data.get('weight'),
            'gender': data.get('gender'),
            'strength': data.get('strength'),
            'session_code': code
        }
        participants_data.append(participant_data)

        # Add participant ID to the session
        sessions[code]['participants'].append(participant_id)

        # Notify host about the participant
        host_message = f"{data.get('name')} has joined the session."

        # Get updated list of participants
        participants = sessions[code]['participants']

        return jsonify({'message': 'Joined session successfully', 'participant_id': participant_id, 'host_message': host_message, 'participants': participants}), 200


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
