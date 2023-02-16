# pedlr-backend
This repository contains the code for creating a server and API for the pedlr bike lock and app.
The server keeps track of bike information including lock status, alarm status, and GPS location for each bicycle registered in the database.

Both the pedlr app and the pedlr bike lock can interact with this API, enabling easy data transfer regardless of what cell network each device is connected to.

## Network Diagram
*will be updated later*

## Database Structure
| **Variable** | **Type** | **Description** |
| :----------- | :------: | :-------------- |
| bike_id      | `dict`   | A dictionary containing the following info                   |
| set_unlocked | `bool`   | Whether the phone has requested the bike to unlock           |
| is_unlocked  | `bool`   | Whether the bike is unlocked                                 |
| set_alarm    | `bool`   | Whether the phone has requested the alarm to activate        |
| is_alarm     | `bool`   | Whether the bike's alarm is active                           |
| GPS          | `list`   | A list containing the GPS latitude and longitude of the bike |

Below is a sample database entry for your reference.
```json
{
  "abc123": {
  "set_unlocked": true,
  "is_unlocked": true,
  "set_alarm": false,
  "is_alarm": false,
  "GPS": [0,0]
  }
}
```
## Setup
A setup script and a text file containing the required Python packages can be found within the setup folder. The setup script first creates a virtual environment, and then installs the necessary Python packages. To run the setup script, run `setup.sh <venv_location>`. Change `<venv_location>` to be the location where the virtual environment will be created.

## Requirements
The backend is built using Python (and the packages below) to achieve the desired functionality of an API and database. The following packages are required for the backend to function properly.  
| **Software** | **Version** |
| :----------: | :---------- |
| Python       | 3.8.10      |
| pickledb     | 0.9.2       |
| flask        | 2.2.2       |

## Valid URLs
This is a list of valid URLs that can be used to access the data. Make sure to replace the `<ip_address>` and `<bike_id>` with the IP address of the server and the ID of the bike being accessed. 
| **URL** | **Response** | **Type** |
| :-----  | :----------- | :------- |
| http://<ip_address>:8080/ | `{'message': 'Welcome to the Pedlr API!'}` | `GET` |
| http://<ip_address>:8080/<bike_id>/info | `{'bike_id': <bike_id>, 'set_unlocked': <bool>, 'is_unlocked': <bool>, 'set_alarm': <bool>, 'is_alarm': <bool>, 'GPS': [0, 0]}` | `GET`|
| http://<ip_address>:8080/<bike_id>/lock | `{'success': True}` or `{'success': False, 'message': '<error_message>'}` | `POST`  (must include either `set_unlocked` or `is_unlocked` entry in the request) |
| http://<ip_address>:8080/<bike_id>/alarm | `{'success': True}` or `{'success': False, 'message': '<error_message>'}` | `POST`  (must include either `set_alarm` or `is_alarm` entry in the request) |
| http://<ip_address>:8080/new_bike/<bike_id> | `{'success': True}` *or* `{'success': False}`  (this will make an initial entry into the database with the specified `bike_id`) | `POST` |