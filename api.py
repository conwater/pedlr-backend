from flask import Flask, request
import pickledb


bike_database_name = "bikedatabase.db"
bike_database = pickledb.load(bike_database_name, False)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main_web():
	url_args = request.args.to_dict()
	possible_actions = ("unlock", "gps", "info", "alarm", "new_bike")
	if 'bike_id' not in url_args or 'action' not in url_args:
		return {
			'success': False,
			'message': 'Must specify a bike_id and an action'
		}
	action = url_args["action"].lower()
	if action not in possible_actions:
		return {
			'success': False,
			'message': f'"{action}" is not a valid action'
		}

	bike = bike_database.get(url_args['bike_id'])
	if bike is False:
		return {
			'success': False,
			'message': f"{url_args['bike_id']} doesn't exist"
		}
	bike_id = url_args['bike_id']
	if action == 'info':
		return {'bike_id': bike_id, **bike}
	elif action == 'unlock':
		return change_lock_state(bike_id, url_args)
	elif action == 'alarm':
		return change_alarm_state(bike_id, url_args)
	elif action == 'new_bike':
		return register_bike(bike_id)
	elif action == 'gps':
		return change_gps_state(bike_id, url_args)

def change_lock_state(bike_id, url_args):

	if 'set_unlock' in url_args.keys() and 'is_unlock' in url_args.keys():
		return {
			'success': False,
			'message': 'Cannot set both "set_unlock" and "is_unlock" in the same request'
		}

	elif 'set_unlock' not in url_args.keys() and 'is_unlock' not in url_args.keys():
		return {
			'success': False,
			'message': 'Request must contain either "is_unlock" or "set_unlock" state'
		}

	elif 'set_unlock' in url_args.keys():
		state = url_args['set_unlock']
		if state.lower() not in ('false', 'true'):
			return {
				'success': False,
				'message': '"set_unlock" must be a boolean (true or false)'
			}
		state = True if state.lower() == 'true' else False

		bike_database.dadd(bike_id, ('set_unlock', state))
	else:
		state = url_args['is_unlock']
		if state.lower() not in ('false', 'true'):
			return {
				'success': False,
				'message': '"is_unlock" must be a boolean (true or false)'
			}
		state = True if state.lower() == 'true' else False

		bike_database.dadd(bike_id, ('is_unlock', state))

	bike_database.dump()
	return {'success': True}

def change_alarm_state(bike_id, url_args):
	if 'set_alarm' in url_args.keys() and 'is_alarm' in url_args.keys():
		return {
			'success': False,
			'message': 'Cannot set both "set_alarm" and "is_alarm" in the same request'
		}

	elif 'set_alarm' not in url_args.keys() and 'is_alarm' not in url_args.keys():
		return {
			'success': False,
			'message': 'Request must contain either "is_alarm" or "set_alarm" state'
		}

	elif 'set_alarm' in url_args.keys():
		state = url_args['set_alarm']
		if state.lower() not in ('true', 'false'):
			return {
				'success': False,
				'message': '"set_alarm" must be a boolean (true or false)'
			}
		state = True if state.lower() == 'true' else False

		bike_database.dadd(bike_id, ('set_alarm', state))
	else:
		state = url_args['is_alarm']
		if state.lower() not in ('true', 'false'):
			return {
				'success': False,
				'message': '"is_alarm" must be a boolean (true or false)'
			}
		state = True if state.lower() == 'true' else False

		bike_database.dadd(bike_id, ('is_alarm', state))

	bike_database.dump()
	return {'success': True}

def register_bike(bike_id):
	if bike_database.get(bike_id) is not False:
		return {
			'success': False,
			'message': f'"{bike_id}" already exists'
		}

	bike_dict = {
		'set_unlock': False,
		'is_unlock': False,
		'set_alarm': False,
		'is_alarm': False,
		'GPS': [0, 0]
	}

	bike_database.set(bike_id, bike_dict)
	bike_database.dump()
	return {'success': True}

def change_gps_state(bike_id, url_args):
	if 'x' not in url_args.keys() or 'y' not in url_args.keys():
		return {
			'success': False,
			'message': 'Must pass "x" and "y" as arguments'
		}
	if bike_database.get(bike_id) is False:
		return {
        	'success': False,
        	'message': f'"{bike_id}" doesn\'t exist'
        }
	try:
		x = float(url_args['x'])
		y = float(url_args['y'])
	except:
		return {
			'success': False,
			'message': 'Must pass valid x and y coordinates'
		}
	
	bike_database.dadd(bike_id, ('GPS', [x, y]))
	bike_database.dump()
	return {'success': True}

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
	app.run(port=8080)

