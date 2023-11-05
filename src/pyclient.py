import random
import string
import time

from websocket import create_connection

import json

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

COFFEE_STATE_TEMPLATE = [{"Title": "Step 1:\n",
                          "SubSteps": [{"Title": "1. Take bowl\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "2. Fill water using measure bowl\n", "Done": 0, "NotSure": 0,
                                        "Error": 0}, {"Title": "3. Take kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "4. Open the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "5. Pour water\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "6. Close the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0}]},
                         {"Title": "Step 2:\n",
                          "SubSteps": [{"Title": "1. Take Filter cone\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "2. Take mug\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "3. Place the filter cone on top of mug\n", "Done": 0, "NotSure": 0,
                                        "Error": 0}]}, {"Title": "Step 3:\n", "SubSteps": [
		{"Title": "1. Take Paper filter\n", "Done": 0, "NotSure": 0, "Error": 0},
		{"Title": "2. Prepare Paper filter half\n", "Done": 0, "NotSure": 0, "Error": 0},
		{"Title": "3. Prepare Paper filter quarter\n", "Done": 0, "NotSure": 0, "Error": 0},
		{"Title": "4. Put Paper filter into dripper\n", "Done": 0, "NotSure": 0, "Error": 0}]}, {"Title": "Step 4:\n",
                                                                                                 "SubSteps": [{
	                                                                                                 "Title": "1. Take the kitchen scale\n",
	                                                                                                 "Done": 0,
	                                                                                                 "NotSure": 0,
	                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "2. Take the coffee beans with container on the scale\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "3. Take the coffee grinder\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "4. Open the coffee grinder\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "5. Pour the coffee beans into the grinder\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "6. Cover the lid of grinder\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "7. Grind coffee beans\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "8. Take the dripper\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "9. Open the coffee grinder\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0},
	                                                                                                 {
		                                                                                                 "Title": "10. Transfer the grounds to the filter cone\n",
		                                                                                                 "Done": 0,
		                                                                                                 "NotSure": 0,
		                                                                                                 "Error": 0}]},
                         {"Title": "Step 5:\n",
                          "SubSteps": [{"Title": "1. Take kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "2. Open the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "3. Take the thermometer\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "4. Put the thermometer into kettle\n", "Done": 0, "NotSure": 0,
                                        "Error": 0},
                                       {"Title": "5. Take out the thermometer\n", "Done": 0, "NotSure": 0, "Error": 0},
                                       {"Title": "6. Close the lid of kettle\n", "Done": 0, "NotSure": 0, "Error": 0}]},
                         {"Title": "Step 6:\n", "SubSteps": [
	                         {"Title": "1. Take the dripper with grounds coffee\n", "Done": 0, "NotSure": 0,
	                          "Error": 0},
	                         {"Title": "2. Pour a small amount of water into dripper\n", "Done": 0, "NotSure": 0,
	                          "Error": 0}]}, {"Title": "Step 7:\n", "SubSteps": [
		{"Title": "1. Pour the rest of the water over the grounds in a circular motion\n", "Done": 0, "NotSure": 0,
		 "Error": 0}]}, {"Title": "Step 8:\n",
                         "SubSteps": [{"Title": "1. Removing the dripper\n", "Done": 0, "NotSure": 0, "Error": 0},
                                      {"Title": "2. Discard the paper filter and coffee grounds.", "Done": 0,
                                       "NotSure": 0, "Error": 0}]}]

PINWHEELS_STATE_TEMPLATE = [{"Title": "Step 1:\n",
                             "SubSteps": [{"Title": "1. Take Cutting Board\n", "Done": 0, "NotSure": 0, "Error": 0},
                                          {"Title": "2. Place tortilla on cutting board\n", "Done": 0, "NotSure": 0,
                                           "Error": 0}]}, {"Title": "Step 2:\n", "SubSteps": [
	{"Title": "1. Take butter knife\n", "Done": 0, "NotSure": 0, "Error": 0},
	{"Title": "2. Take nut butter jar\n", "Done": 0, "NotSure": 0, "Error": 0},
	{"Title": "3. Scoop nut butter from butter jar using butter knife\n", "Done": 0, "NotSure": 0, "Error": 0},
	{"Title": "4. Spread nut butter on tortilla\n", "Done": 0, "NotSure": 0, "Error": 0}]}, {"Title": "Step 3:\n",
                                                                                             "SubSteps": [{
	                                                                                             "Title": "1. Take the paper towel\n",
	                                                                                             "Done": 0,
	                                                                                             "NotSure": 0,
	                                                                                             "Error": 0},
	                                                                                             {
		                                                                                             "Title": "2. Clean the butter knife using paper towel\n",
		                                                                                             "Done": 0,
		                                                                                             "NotSure": 0,
		                                                                                             "Error": 0}]},
                            {"Title": "Step 4:\n",
                             "SubSteps": [{"Title": "1. Take butter knife\n", "Done": 0, "NotSure": 0, "Error": 0},
                                          {"Title": "2. Take jelly jar\n", "Done": 0, "NotSure": 0, "Error": 0},
                                          {"Title": "3. Scoop jelly from jelly jar using butter knife\n", "Done": 0,
                                           "NotSure": 0, "Error": 0},
                                          {"Title": "4. Spread jelly on tortilla\n", "Done": 0, "NotSure": 0,
                                           "Error": 0}]}, {"Title": "Step 5:\n", "SubSteps": [
		{"Title": "1. Take the paper towel\n", "Done": 0, "NotSure": 0, "Error": 0},
		{"Title": "2. Clean the butter knife using paper towel\n", "Done": 0, "NotSure": 0, "Error": 0}]},
                            {"Title": "Step 6:\n", "SubSteps": [
	                            {"Title": "1. Tightly roll the tortilla\n", "Done": 0, "NotSure": 0, "Error": 0}]},
                            {"Title": "Step 7:\n",
                             "SubSteps": [{"Title": "1. Take the toothpicks\n", "Done": 0, "NotSure": 0, "Error": 0},
                                          {"Title": "2. Insert 5 toothpicks into the tortilla\n", "Done": 0,
                                           "NotSure": 0, "Error": 0}]}, {"Title": "Step 8:\n", "SubSteps": [
		{"Title": "1. Trim the ends of the tortilla roll with the butter knife on both sides\n", "Done": 0,
		 "NotSure": 0, "Error": 0}]}, {"Title": "Step 9:\n",
                                       "SubSteps": [{"Title": "1. Take floss\n", "Done": 0, "NotSure": 0, "Error": 0}, {
	                                       "Title": "2. Place floss under the tortilla halfway between the two toothpicks\n",
	                                       "Done": 0, "NotSure": 0, "Error": 0}]}, {"Title": "Step 10:\n", "SubSteps": [
		{"Title": "1. Cross the two ends of the floss over the top of the tortilla roll\n", "Done": 0, "NotSure": 0,
		 "Error": 0}, {"Title": "2. Pull the floss to cut the tortilla\n", "Done": 0, "NotSure": 0, "Error": 0}]},
                            {"Title": "Step 11:\n", "SubSteps": [{
	                            "Title": "1. Continue slicing with floss to create the second pinwheel.  (Repeat 10)\n",
	                            "Done": 0, "NotSure": 0, "Error": 0}]},
                            {"Title": "Step 12:\n", "SubSteps": [
	                            {"Title": "1. Continue slicing with floss to create the third pinwheel.  (Repeat 10)\n",
	                             "Done": 0, "NotSure": 0, "Error": 0}]}, {"Title": "Step 13:\n", "SubSteps": [
		{"Title": "1. Continue slicing with floss to create fourth and fifth pinwheels.  (Repeat 10)\n", "Done": 0,
		 "NotSure": 0, "Error": 0}]}, {"Title": "Step 14:\n", "SubSteps": [
		{"Title": "1. Take the plate\n", "Done": 0, "NotSure": 0, "Error": 0},
		{"Title": "2. Place the pinwheels on the plate", "Done": 0, "NotSure": 0, "Error": 0}]}]

state_template = {COFFEE: COFFEE_STATE_TEMPLATE, PINWHEELS: PINWHEELS_STATE_TEMPLATE}
sub_step_size = {COFFEE: 34, PINWHEELS: 27}


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
		sub_step_id = 0
		return json.dumps(recipe_json_obj)


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- UPDATES RECIPE DETAILS ----------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def construct_update_recipe(recipe):
	message = {TYPE: UPDATE_RECIPE}
	details = {RECIPE: recipe, RECIPE_STATE: build_recipe_from_template(recipe, [])}
	message[DETAILS] = details
	message_json = json.dumps(message)
	return message_json


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


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- UPDATES RECIPE ERRORS -----------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def construct_update_errors(recipe, errors):
	message = {TYPE: UPDATE_ERRORS}
	details = {RECIPE: recipe, ERRORS: errors}
	message[DETAILS] = details
	message_json = json.dumps(message)
	return message_json


class WSClient:
	
	def __init__(self):
		self.ws = create_connection("ws://localhost:8000")
	
	def close(self):
		self.ws.close()
	
	# Takes in recipe list as input
	# ["coffee", "pinwheels", "tea", "oatmeal", "quesedilla"]
	def update_recipes(self, recipe_list: list):
		for recipe in recipe_list:
			self.update_recipe(recipe)
	
	# Takes in recipe as input, specify only from below examples
	# ["coffee", "mugcake", "pinwheels"]
	def update_recipe(self, recipe):
		self.ws.send(construct_update_recipe(recipe))
	
	# Takes in recipe and status list as input, specify only from below examples
	# ["coffee", "mugcake", "pinwheels"], [.....0, -1, 1......] (length of the list == total number of sub steps)
	def update_sub_steps(self, recipe, status):
		self.ws.send(construct_update_sub_steps(recipe, status))
	
	# Takes in recipe list and status list as input
	# ["coffee", "tea", "pinwheels"], [[.....0, -1, 1......], [.....0, -1, 1......], [.....0, -1, 1......]]
	def update_recipes_sub_steps(self, recipe_list: list, status_list: list):
		for recipe, status in zip(recipe_list, status_list):
			self.update_sub_steps(recipe, status)
	
	# Takes in recipe and error list as input, specify only from below examples
	# ["err1", "err2", "err3".....]
	def update_errors(self, recipe, errors):
		self.ws.send(construct_update_errors(recipe, errors))
	
	# ----------------------------------------- DUMMY METHODS -----------------------------------------
	
	def fetch_dummy_update_recipe(self, recipe):
		rint = random.randint(1, 10)
		if rint < 3:
			recipe = COFFEE
		elif 3 <= rint < 7:
			recipe = MUGCAKE
		else:
			recipe = PINWHEELS
		return recipe
	
	def dummy_update_recipe(self, recipe):
		recipe = self.fetch_dummy_update_recipe(recipe)
		self.ws.send(construct_update_recipe(recipe))
	
	# ---------------------------------------------------------------------------------------------------------
	#  ---------------------------------- UPDATES RECIPE SUB STEPS DETAILS-------------------------------------
	# ---------------------------------------------------------------------------------------------------------
	
	def fetch_dummy_status_list(self, random_int):
		num_list = []
		for count in range(random_int):
			num_list.append(random.randint(-1, 1))
		return num_list
	
	def fetch_dummy_update_sub_steps(self, recipe, status):
		rint = random.randint(1, 10)
		if rint < 3:
			recipe = COFFEE
		elif 3 <= rint < 7:
			recipe = MUGCAKE
		else:
			recipe = PINWHEELS
		status = self.fetch_dummy_status_list(sub_step_size[recipe])
		return status
	
	def dummy_update_sub_steps(self, recipe, status):
		recipe = self.fetch_dummy_update_recipe(recipe)
		status = self.fetch_dummy_update_sub_steps(recipe, status)
		self.ws.send(construct_update_sub_steps(recipe, status))
	
	# ---------------------------------------------------------------------------------------------------------
	#  ---------------------------------- UPDATES RECIPE ERRORS -----------------------------------------------
	# ---------------------------------------------------------------------------------------------------------
	
	def dummy_generate_random_text(self, nchar, nnum):
		digits = "".join([random.choice(string.digits) for i in range(nnum)])
		chars = "".join([random.choice(string.ascii_letters) for i in range(nchar)])
		return digits + chars
	
	def fetch_dummy_errors(self, recipe, errors):
		rand_error_length = random.randint(1, 10)
		errors = []
		for i in range(rand_error_length):
			errors.append(self.dummy_generate_random_text(random.randint(2, 30), random.randint(7, 20)))
		return errors
	
	def dummy_update_errors(self, recipe, errors):
		recipe = self.fetch_dummy_update_recipe(recipe)
		errors = self.fetch_dummy_errors(recipe, errors)
		self.ws.send(construct_update_errors(recipe, errors))


def check_dummy():
	wsclient = WSClient()
	for i in range(100):
		wsclient.dummy_update_sub_steps("recipe", [])
		time.sleep(3)
		wsclient.dummy_update_recipe("recipe")
		time.sleep(3)
		wsclient.dummy_update_errors("recipe", [])
	wsclient.close()


if __name__ == "__main__":
	check_dummy()
