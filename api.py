from flask import Flask, request
import pickledb

bike_database_name = "bikedatabase.db"
bike_database = pickledb.load(bike_database_name, False)

app = Flask(__name__)

@app.route('/')
def hello_world():
	return {'message': 'Welcome to the Pedlr API!'}

@app.route('/<bike_id>/info', methods=['GET'])
def bike_data(bike_id):
	bike = bike_database.get(bike_id)
	if bike is False:
		return {
			'success': False,
			'message': f'"{bike_id}" doesn\'t exist'
		}

	return {'bike_id': bike_id, **bike}

@app.route('/<bike_id>/lock', methods=['POST'])
def change_lock_state(bike_id):
	if bike_database.get(bike_id) is False:
		return {
			'success': False,
			'message': f'"{bike_id}" doesn\'t exist'
		}
	post_data = dict(request.get_json())

	if 'set_unlocked' in post_data.keys() and 'is_unlocked' in post_data.keys():
		return {
			'success': False,
			'message': f'Cannot set both "set_unlocked" and "is_unlocked" in the same request'
		}

	elif 'set_unlocked' not in post_data.keys() and 'is_unlocked' not in post_data.keys():
		return {
			'success': False,
			'message': 'Request must contain either "is_unlocked" or "set_unlocked" state'
		}

	elif 'set_unlocked' in post_data.keys():
		state = post_data['set_unlocked']
		if type(state) is not bool:
			return {
				'success': False,
				'message': '"set_unlocked" must be a boolean (true or false)'
			}
		bike_database.dadd(bike_id, ('set_unlocked', state))
	else:
		state = post_data['is_unlocked']
		if type(state) is not bool:
			return {
				'success': False,
				'message': '"is_unlocked" must be a boolean (true or false)'
			}
		bike_database.dadd(bike_id, ('is_unlocked', state))

	bike_database.dump()
	return {'success': True}

@app.route('/<bike_id>/alarm', methods=['POST'])
def change_alarm_state(bike_id):
	if bike_database.get(bike_id) is False:
		return {
			'success': False,
			'message': f'"{bike_id}" doesn\'t exist'
		}
	post_data = dict(request.get_json())

	if 'set_alarm' in post_data.keys() and 'is_alarm' in post_data.keys():
		return {
			'success': False,
			'message': f'Cannot set both "set_alarm" and "is_alarm" in the same request'
		}

	elif 'set_alarm' not in post_data.keys() and 'is_alarm' not in post_data.keys():
		return {
			'success': False,
			'message': 'Request must contain either "is_alarm" or "set_alarm" state'
		}

	elif 'set_alarm' in post_data.keys():
		state = post_data['set_alarm']
		if type(state) is not bool:
			return {
				'success': False,
				'message': '"set_alarm" must be a boolean (true or false)'
			}
		bike_database.dadd(bike_id, ('set_alarm', state))
	else:
		state = post_data['is_alarm']
		if type(state) is not bool:
			return {
				'success': False,
				'message': '"is_alarm" must be a boolean (true or false)'
			}
		bike_database.dadd(bike_id, ('is_alarm', state))

	bike_database.dump()
	return {'success': True}

@app.route('/new_bike/<bike_id>', methods=['POST'])
def register_bike(bike_id):
	if bike_database.get(bike_id) is not False:
		return {'success': False}

	bike_dict = {
		'set_unlocked': False,
		'is_unlocked': False,
		'set_alarm': False,
		'is_alarm': False,
		'GPS': [0, 0]
	}

	bike_database.set(bike_id, bike_dict)
	bike_database.dump()
	return {'success': True}

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
