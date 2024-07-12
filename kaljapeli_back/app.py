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


'''
    This endpoint is used to start a session.
    The host provides a code to start the session.
    The code is used to identify the session.
    The session is stored in the sessions dictionary.
    If the code already exists in the sessions dictionary, a 400 response is returned.
    If the code does not exist in the sessions dictionary, a 201 response is returned.
'''


@app.route('/start_session', methods=['POST'])
def start_session():
    data = request.get_json()
    code = data.get('code')
    if code in sessions:
        return jsonify({'message': 'Session with code already exists'}), 400
    else:
        sessions[code] = {'participants': {}}
        return jsonify({'message': 'Session started successfully'}), 201


'''
    This endpoint is used to join a session.
    The participant provides their personal details to join the session.
    The participant is added to the participants dictionary in the session.
    The participant data is stored in the participants_data dictionary.
    If the session code is not found in the sessions dictionary, a 404 response is returned.
    If the session code is found in the sessions dictionary, a 200 response is returned.
'''


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


'''
    This endpoint is used to get the participants in the session.
    The participants are returned as a list of dictionaries.
    Each dictionary contains the participant data.
    If the session code is not found in the sessions dictionary, a 404 response is returned.
    If the session code is found in the sessions dictionary, a 200 response is returned.
'''


@app.route('/get_participants', methods=['GET'])
def get_participants():
    code = request.args.get('code')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        participants = sessions[code]['participants']
        return jsonify({'participants': participants}), 200


'''
    This endpoint is used to remove a participant from the session.
    The host can remove a participant by providing the participant_id, or the player can remove themselves.
    The participant_id is used to identify the participant to be removed.
    The participant_id is removed from the participants dictionary and the participant data is removed from the participants_data dictionary.
    If the participant_id is not found in the participants dictionary, a 404 response is returned.
    If the participant_id is found in the participants dictionary, a 200 response is returned.
'''


@app.route('/remove_participant', methods=['POST'])
def remove_participant():
    data = request.get_json()
    code = data.get('code')
    participant_id = data.get('playerId')
    if code not in sessions:
        return jsonify({'message': 'Session with code does not exist'}), 404
    else:
        participants = sessions[code]['participants']
        print(participants, participants_data)
        print(participant_id)

        if participant_id in participants:
            del participants[participant_id]
            del participants_data[participant_id]
            return jsonify({'message': 'Participant removed successfully'}), 200
        else:
            participantlist = ', '.join(
                [participants[pid]['name'] for pid in participants])
            return jsonify({'message': 'Participant not found, here are the current participants: ' + participantlist}), 404


'''
    This endpoint is used to start the game
    The host can start the game by providing the session code.
    The session code is used to identify the session.
    The participants in the session are used to create player instances.
    The game mode is set to ClassicMinuteBeerMode.
    The game session is started and runs for the game time or until stopped by the host.
    If the session code is not found in the sessions dictionary, a 404 response is returned.
    If the session code is found in the sessions dictionary, a 200 response is returned.
'''


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
