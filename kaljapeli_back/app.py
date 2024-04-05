from flask import Flask, request, jsonify
from flask_cors import CORS
from game_logic import BasicLogic, ClassicMinuteBeerMode, Timer
from player import Player
import uuid
import json

app = Flask(__name__)
CORS(app)

# Dictionary to store participant data
participants_data = {}

# Dictionary to store sessions and their participants
sessions = {}


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder


@app.route('/start_session', methods=['POST'])
def start_session():
    data = request.get_json()
    code = data.get('code')
    if code in sessions:
        return jsonify({'message': 'Session with code already exists'}), 400
    else:
        sessions[code] = {'participants': {}}
        return jsonify({'message': 'Session started successfully'}), 201


@app.route('/join_session', methods=['POST'])
def join_session():
    data = request.get_json()
    code = data.get('code')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        participant_id = str(uuid.uuid4())
        personal_details = data.get('personalDetails')
        name = personal_details.get('name')
        weight = personal_details.get('weight')
        gender = personal_details.get('gender')
        drink_strength = personal_details.get('drink_strength')

        participant = Player(participant_id, name, gender,
                             weight, drink_strength)
        participants_data[participant_id] = participant
        sessions[code]['participants'][participant_id] = participant.__dict__

        host_message = f"{name} has joined the session."
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


@app.route('/remove_participant', methods=['POST'])
def remove_participant():
    data = request.get_json()
    code = data.get('code')
    participant_id = data.get('participant_id')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        participants = sessions[code]['participants']
        print(participants, participants_data)

        if participant_id in participants:
            del participants[participant_id]
            del participants_data[participant_id]
            return jsonify({'message': 'Participant removed successfully'}), 200
        else:
            participantlist = ', '.join(
                [participants[pid]['name'] for pid in participants])
            return jsonify({'message': 'Participant not found, here are the current participants: ' + participantlist}), 404


@ app.route('/start_game', methods=['POST'])
def start_game():
    print('Starting game')
    data = request.get_json()
    code = data.get('code')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        participants = sessions[code]['participants']
        print(participants)
        participant_instances = [Player(**participants[pid])
                                 for pid in participants]
        classic_mode = ClassicMinuteBeerMode(participant_instances, code)

        # Start the game session
        # here we create a game loop that runs for the game time or until stopped by the host
        while Timer.get_elapsed_time() < Timer.game_time and not classic_mode.game_over:
            message = classic_mode.update_game()
            print(message)

        response = jsonify({'message': 'Game session started successfully'})
        return response, 200


if __name__ == '__main__':
    app.run(debug=True)
