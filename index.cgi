#!/web/entities/pedlr/venv/bin/python3

import cgi
import cgitb
import json
import pickledb

cgitb.enable(display=0, logdir="/web/entities/pedlr")
#logfile = open("logfile.txt", "a")
bike_database_name = "bikedatabase.db"
bike_database = pickledb.load(bike_database_name, False)


def bike_data(bike_id=None):
	# Retrieve data from database or other source
	bike = bike_database.get(bike_id)
	if bike is False:
		return json.dumps({
			'success': False,
			'message': f'"{bike_id}" doesn\'t exist'
		})

	return json.dumps({"bike_id": bike_id, **bike})

def change_lock_state(bike_id):
	if bike_database.get(bike_id) is False:
		return json.dumps({
			'success': False,
			'message': f'"{bike_id}" doesn\'t exist'
		})

	post_data = cgi.FieldStorage()
	print(post_data)

	if 'set_unlock' in post_data.keys() and 'is_unlock' in post_data.keys():
		return json.dumps({
			'success': False,
			'message': f'Cannot set both "set_unlock" and "is_unlock" in the same request'
		})

	elif 'set_unlock' not in post_data.keys() and 'is_unlock' not in post_data.keys():
		return json.dumps({
			'success': False,
			'message': 'Request must contain either "is_unlock" or "set_unlock" state'
		})

	elif 'set_unlock' in post_data.keys():
		state = post_data['set_unlock']
		if type(state) is not bool:
			return json.dumps({
				'success': False,
				'message': '"set_unlock" must be a boolean (true or false)'
			})
		bike_database.dadd(bike_id, ('set_unlock', state))
	else:
		state = post_data['is_unlock']
		if type(state) is not bool:
			return json.dumps({
				'success': False,
				'message': '"is_unlock" must be a boolean (true or false)'
			})
		bike_database.dadd(bike_id, ('is_unlock', state))
	bike_database.dump()
	return json.dumps({'success': True})

def change_alarm_state(bike_id):
	if bike_database.get(bike_id) is False:
		return json.dumps({
			'success': False,
			'message': f'"{bike_id}" doesn\'t exist'
		})
	post_data = cgi.FieldStorage()

	if 'set_alarm' in post_data.keys() and 'is_alarm' in post_data.keys():
		return json.dumps({
			'success': False,
			'message': f'Cannot set both "set_alarm" and "is_alarm" in the same request'
		})

	elif 'set_alarm' not in post_data.keys() and 'is_alarm' not in post_data.keys():
		return json.dumps({
			'success': False,
			'message': 'Request must contain either "is_alarm" or "set_alarm" state'
		})

	elif 'set_alarm' in post_data.keys():
		state = post_data['set_alarm']
		if type(state) is not bool:
			return json.dumps({
				'success': False,
				'message': '"set_alarm" must be a boolean (true or false)'
			})
		bike_database.dadd(bike_id, ('set_alarm', state))
	else:
		state = post_data['is_alarm']
		if type(state) is not bool:
			return json.dumps({
				'success': False,
				'message': '"is_alarm" must be a boolean (true or false)'
			})
		bike_database.dadd(bike_id, ('is_alarm', state))

	bike_database.dump()
	return json.dumps({'success': True})

def register_bike(bike_id):
	if bike_database.get(bike_id) is not False:
		return json.dumps({'success': False})

	bike_dict = {
		'set_unlock': False,
		'is_unlock': False,
		'set_alarm': False,
		'is_alarm': False,
		'GPS': [0, 0]
	}

	bike_database.set(bike_id, bike_dict)
	bike_database.dump()
	return json.dumps({'success': True})

def handle_post():
	# Parse incoming data from request body
	form = cgi.FieldStorage()
	if "age" not in form:
		return json.dumps({"error": "Missing age parameter"})

	age = form.getvalue("age")
	try:
		age = int(age)
	except ValueError:
		return json.dumps({"error": "Age parameter must be an integer"})

	# Update age in data
	data = {"name": "John", "age": age, "city": "New York"}

	# Return success message as JSON
	return json.dumps({"status": "success"})

if __name__ == '__main__':
	# Parse incoming request and determine method
	form = cgi.FieldStorage()
	if 'bike_id' not in form:
		data = json.dumps({
				'success': False,
				'message': 'Must specify "bike_id"'
			})
	elif 'action' not in form:
		data = json.dumps({
				'success': False,
				'message': 'Must specify action'
			})
	elif form['action'].value == 'info':
		data = bike_data(form['bike_id'].value)
	elif form['action'].value == 'unlock':
		data = change_lock_state(form['bike_id'].value)
	elif form['action'].value == 'alarm':
		data = change_alarm_state(form['bike_id'].value)
	elif form['action'].value == 'new_bike':
		data = register_bike(form['bike_id'].value)
	else:
		data = json.dumps({
			'success': False,
			'message': 'Must specify valid action'
		})

	print("Content-Type: application/json")
	print()
	print(data)

