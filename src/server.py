import random
import string
import json
import threading

from websocket_server import WebsocketServer
from threading import Timer


class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer = None
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False


COFFEE = "coffee"
MUGCAKE = "mugcake"
PINWHEELS = "pinwheels"

TYPE = "Type"
DETAILS = "Details"
RECIPE = "Recipe"
STATUS = "Status"
ERRORS = "Errors"
RECIPE_STATE = "RecipeState"

UPDATE_RECIPE = "update recipe"
UPDATE_STATUS = "update status"
UPDATE_ERRORS = "update errors"

TITLE = "Title"
DONE = "Done"
NOT_SURE = "NotSure"
ERROR = "Error"
SUB_STEPS = "SubSteps"

COFFEE_STATE_TEMPLATE = [
    {
        "Title": "Recipe 1",
        "Steps": [
            {
                "Step_ID": "Step 1:\n",
                "SubSteps": [
                    {"Description": "1. Take bowl\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "2. Fill water using measure bowl\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "3. Take kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "4. Open the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "5. Pour water\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "6. Close the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 2:\n",
                "SubSteps": [
                    {"Description": "1. Take Filter cone\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "2. Take mug\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "3. Place the filter cone on top of mug\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 3:\n",
                "SubSteps": [
                    {"Description": "1. Take Paper filter\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "2. Prepare Paper filter half\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "3. Prepare Paper filter quarter\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "4. Put Paper filter into dripper\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 4:\n",
                "SubSteps": [
                    {"Description": "1. Take the kitchen scale\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "2. Take the coffee beans with container on the scale\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "3. Take the coffee grinder\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "4. Open the coffee grinder\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "5. Pour the coffee beans into the grinder\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "6. Cover the lid of grinder\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "7. Grind coffee beans\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "8. Take the dripper\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "9. Open the coffee grinder\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "10. Transfer the grounds to the filter cone\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 5:\n",
                "SubSteps": [
                    {"Description": "1. Take kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "2. Open the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "3. Take the thermometer\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "4. Put the thermometer into kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "5. Take out the thermometer\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "6. Close the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 6:\n",
                "SubSteps": [
                    {"Description": "1. Take the dripper with grounds coffee\n", "Done": 0, "NotSure": 0, "Error": 0},
                    {"Description": "2. Pour a small amount of water into dripper\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 7:\n",
                "SubSteps": [
                    {"Description": "1. Pour the rest of the water over the grounds in a circular motion\n", "Done": 0, "NotSure": 0, "Error": 0}
                ]
            },
            {
                "Step_ID": "Step 8:\n",
                "SubSteps": [
                    {"Description": "1. Removing the dripper\n", "Done": 1, "NotSure": 0, "Error": 0},
                    {"Description": "2. Discard the paper filter and coffee grounds.", "Done": 1, "NotSure": 0, "Error": 0}
                ]
            }
        ]
    }
]

state_template = {COFFEE: COFFEE_STATE_TEMPLATE}
sub_step_size = {COFFEE: 34}


# ----------------------------------------------------------------------------------------------------------


def build_recipe_from_template(recipe, status):
	template = state_template[recipe]
	total_sub_steps = sub_step_size[recipe]
	if len(status) == 0:
		print("Starting recipe so status does not matter")
		return template
	else:
		recipe_json_obj = json.loads(json.dumps(template))
		sub_step_id = 0
		for step in recipe_json_obj:
			for sub_step in step[SUB_STEPS]:
				sub_step[DONE] = 0
				sub_step[NOT_SURE] = 0
				sub_step[ERROR] = 0
				if status[sub_step_id] == 0:
					sub_step[NOT_SURE] = 1
				elif status[sub_step_id] == -1:
					sub_step[ERROR] = 1
				elif status[sub_step_id] == 1:
					sub_step[DONE] = 1
				sub_step_id = sub_step_id + 1
		return json.dumps(recipe_json_obj)


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- SERVER STARTUP CALLS  ----------------------------------------------
# ---------------------------------------------------------------------------------------------------------

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	#server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
	# if len(message) > 200:
	# 	message = message[:200] + '..'
	print("Client(%d) said: %s" % (client['id'], message))
	server.send_message_to_all(message)


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- UPDATES RECIPE DETAILS ----------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def construct_update_recipe(recipe):
	message = {TYPE: UPDATE_RECIPE}
	details = {RECIPE: recipe, RECIPE_STATE: build_recipe_from_template(recipe, [])}
	message[DETAILS] = details
	message_json = json.dumps(message)
	return message_json


def fetch_dummy_update_recipe(recipe):
	rint = random.randint(1, 10)
	if rint < 3:
		recipe = COFFEE
	elif 3 <= rint < 7:
		recipe = MUGCAKE
	else:
		recipe = PINWHEELS
	return recipe


def dummy_update_recipe(recipe):
	recipe = fetch_dummy_update_recipe(recipe)
	server.send_message_to_all(construct_update_recipe(recipe))


# Takes in recipe as input, specify only from below examples
# ["coffee", "mugcake", "pinwheels"]
def update_recipe(recipe):
	recipe = fetch_dummy_update_recipe(recipe)
	server.send_message_to_all(construct_update_recipe(recipe))


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- UPDATES RECIPE SUB STEPS DETAILS-------------------------------------
# ---------------------------------------------------------------------------------------------------------

def construct_update_sub_steps(recipe, status):
	message = {TYPE: UPDATE_STATUS}
	details = {RECIPE: recipe, RECIPE_STATE: build_recipe_from_template(recipe, status)}
	message[DETAILS] = details
	message_json = json.dumps(message)
	print(message_json)
	return message_json


def fetch_dummy_status_list(random_int):
	num_list = []
	for count in range(random_int):
		num_list.append(random.randint(-1, 1))
	return num_list


def fetch_dummy_update_sub_steps(recipe, status):
	rint = random.randint(1, 10)
	if rint < 3:
		recipe = COFFEE
	elif 3 <= rint < 7:
		recipe = MUGCAKE
	else:
		recipe = PINWHEELS
	status = fetch_dummy_status_list(sub_step_size[recipe])
	return status


def dummy_update_sub_steps(recipe, status):
	recipe = fetch_dummy_update_recipe(recipe)
	status = fetch_dummy_update_sub_steps(recipe, status)
	server.send_message_to_all(construct_update_sub_steps(recipe, status))


# Takes in recipe and status list as input, specify only from below examples
# ["coffee", "mugcake", "pinwheels"], [.....0, -1, 1......] (length of the list == total number of sub steps)
def update_sub_steps(recipe, status):
	server.send_message_to_all(construct_update_sub_steps(recipe, status))


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- UPDATES RECIPE ERRORS -----------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def construct_update_errors(recipe, errors):
	message = {TYPE: UPDATE_ERRORS}
	details = {RECIPE: recipe, ERRORS: errors}
	message[DETAILS] = details
	message_json = json.dumps(message)
	return message_json


def dummy_generate_random_text(nchar, nnum):
	digits = "".join([random.choice(string.digits) for i in range(nnum)])
	chars = "".join([random.choice(string.ascii_letters) for i in range(nchar)])
	return digits + chars


def fetch_dummy_errors(recipe, errors):
	rand_error_length = random.randint(1, 10)
	errors = []
	for i in range(rand_error_length):
		errors.append(dummy_generate_random_text(random.randint(2, 30), random.randint(7, 20)))
	return errors


def dummy_update_errors(recipe, errors):
	recipe = fetch_dummy_update_recipe(recipe)
	errors = fetch_dummy_errors(recipe, errors)
	server.send_message_to_all(construct_update_errors(recipe, errors))


# Takes in recipe and error list as input, specify only from below examples
# ["err1", "err2", "err3".....]
def update_errors(recipe, errors):
	server.send_message_to_all(construct_update_errors(recipe, errors))


# rt_status = RepeatedTimer(5, dummy_update_sub_steps, "text", [])
# rt_errors = RepeatedTimer(5, dummy_update_errors, COFFEE, "text")
# rt_recipe = RepeatedTimer(5, dummy_update_recipe, "text")


# -------------------------------------------------------------------------------------------------
# --------------------------- Starting web socket server in another thread -----------------------
# -------------------------------------------------------------------------------------------------


server = WebsocketServer(host='localhost', port=8000)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
#update_recipe(RECIPE)
#update_sub_steps(COFFEE, [])
#update_errors(RECIPE, ERRORS)
server.run_forever()
