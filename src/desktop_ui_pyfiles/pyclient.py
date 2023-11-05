import random
import string
import time
import json
from constants import Constants as const
from step_states import StepStateTemplate as step_state_template
from sub_step_states import SubStepStateTemplate as sub_step_state_template

from websocket import create_connection

step_size = {
	const.COFFEE: 8,
	const.PINWHEELS: 14,
	const.TEA: 7,
	const.QUESADILLA: 7,
	const.OATMEAL: 7
}

sub_step_size = {
	const.COFFEE: 34,
	const.PINWHEELS: 27,
	const.TEA: 29,
	const.QUESADILLA: 19,
	const.OATMEAL: 43
}

step_state_template_map = {
	const.COFFEE: step_state_template.COFFEE_TEMPLATE,
	const.PINWHEELS: step_state_template.PINWHEELS_TEMPLATE,
	const.TEA: step_state_template.TEA_TEMPLATE,
	const.QUESADILLA: step_state_template.QUESADILLA_TEMPLATE,
	const.OATMEAL: step_state_template.OATMEAL_TEMPLATE
}

sub_step_state_template_map = {
	const.COFFEE: sub_step_state_template.COFFEE_TEMPLATE,
	const.PINWHEELS: sub_step_state_template.PINWHEELS_TEMPLATE,
	const.TEA: sub_step_state_template.TEA_TEMPLATE,
	const.QUESADILLA: sub_step_state_template.QUESADILLA_TEMPLATE,
	const.OATMEAL: sub_step_state_template.OATMEAL_TEMPLATE
}


# ----------------------------------------------------------------------------------------------------------

def build_recipe_step_state_from_template(recipe, step_status):
	recipe_step_state_template = step_state_template_map[recipe]
	recipe_step_obj = json.loads(json.dumps(recipe_step_state_template))
	step_id = 0
	for step in recipe_step_obj:
		step[const.STATE] = step_status[step_id]
		step_id = step_id + 1
	return recipe_step_obj


def build_recipe_sub_step_status_from_template(recipe, sub_step_status):
	recipe_sub_step_status_template = sub_step_state_template_map[recipe]
	recipe_sub_step_obj = json.loads(json.dumps(recipe_sub_step_status_template))
	sub_step_id = 0
	for step in recipe_sub_step_obj:
		for sub_step in step[const.SUB_STEPS]:
			sub_step[const.STATE] = sub_step_status[sub_step_id]
			sub_step_id = sub_step_id + 1
	return recipe_sub_step_obj


# ---------------------------------------------------------------------------------------------------------
#  ---------------------------------- UPDATES DETAILS -----------------------------------
# ---------------------------------------------------------------------------------------------------------

def construct_update_recipe_steps(recipe_list: list, step_status_list: list):
	recipe_step_status_dict_list = []
	for recipe, step_status in zip(recipe_list, step_status_list):
		recipe_step_status_dict = {
			const.RECIPE: recipe,
			const.RECIPE_STATES: build_recipe_step_state_from_template(recipe, step_status)
		}
		recipe_step_status_dict_list.append(recipe_step_status_dict)
	
	message = {
		const.TYPE: const.UPDATE_RECIPE_STEP_STATES,
		const.DETAILS: recipe_step_status_dict_list
	}
	message_json = json.dumps(message)
	return message_json


def construct_update_recipe_sub_steps(recipe_list, sub_step_status_list):
	recipe_sub_step_status_dict_list = []
	for recipe, sub_step_status in zip(recipe_list, sub_step_status_list):
		recipe_step_status_dict = {
			const.RECIPE: recipe,
			
			const.RECIPE_SUB_STEP_STATES: build_recipe_sub_step_status_from_template(recipe, sub_step_status)
		}
		recipe_sub_step_status_dict_list.append(recipe_step_status_dict)
	
	message = {
		const.TYPE: const.UPDATE_RECIPE_STEP_STATES,
		const.DETAILS: recipe_sub_step_status_dict_list
	}
	message_json = json.dumps(message)
	return message_json


class WSClient:
	
	def __init__(self):
		self.ws = create_connection("ws://localhost:8000")
		self.recipe_list = ["coffee", "pinwheels", "tea", "oatmeal", "quesadilla"]
	
	def close(self):
		self.ws.close()
	
	# State : 0 -> Not Done, 1 -> Error, 2 -> Done
	def update_recipe_step_status(self, recipe_list: list, step_status_list: list):
		self.ws.send(construct_update_recipe_steps(recipe_list, step_status_list))
	
	# State : 0 -> Not Done, 1 -> In Progress, 2 -> Done, 3 -> Missing, 4 -> Ordering,
	# 5 -> Technique, 6 -> Preparation
	def update_recipe_sub_step_status(self, recipe_list: list, sub_step_status_list: list):
		self.ws.send(construct_update_recipe_sub_steps(recipe_list, sub_step_status_list))
	
	# ----------------------------------------- DUMMY METHODS -----------------------------------------
	
	@staticmethod
	def fetch_dummy_update_recipe():
		rint = random.randint(1, 10)
		if rint < 2:
			recipe = const.COFFEE
		elif 2 <= rint < 4:
			recipe = const.PINWHEELS
		elif 4 <= rint < 6:
			recipe = const.TEA
		elif 6 <= rint < 8:
			recipe = const.QUESADILLA
		else:
			recipe = const.OATMEAL
		return recipe
	
	@staticmethod
	def fetch_dummy_step_status(num_steps):
		step_status = []
		for i in range(num_steps):
			step_status.append(random.randint(0, 3))
		return step_status
	
	@staticmethod
	def fetch_dummy_sub_step_status(num_sub_steps):
		sub_step_status = []
		for i in range(num_sub_steps):
			sub_step_status.append(random.randint(0, 7))
		return sub_step_status
	
	def fetch_dummy_update_steps(self):
		recipe = self.fetch_dummy_update_recipe()
		status = self.fetch_dummy_step_status(step_size[recipe])
		return recipe, status
	
	def fetch_dummy_update_sub_steps(self):
		recipe = self.fetch_dummy_update_recipe()
		status = self.fetch_dummy_sub_step_status(sub_step_size[recipe])
		return recipe, status
	
	# ---------------------------------------------------------------------------------------------------------
	#  ---------------------------------- DUMMY UPDATES -----------------------------------------------
	# ---------------------------------------------------------------------------------------------------------
	
	def dummy_update_steps(self):
		num_recipes = random.randint(1, 6)
		recipe_list = []
		step_status_list = []
		for i in range(num_recipes):
			recipe, status = self.fetch_dummy_update_steps()
			recipe_list.append(recipe)
			step_status_list.append(status)
		self.ws.send(construct_update_recipe_steps(recipe_list, step_status_list))
	
	def dummy_update_sub_steps(self):
		num_recipes = random.randint(1, 6)
		recipe_list = []
		sub_step_status_list = []
		for i in range(num_recipes):
			recipe, status = self.fetch_dummy_update_sub_steps()
			recipe_list.append(recipe)
			sub_step_status_list.append(status)
		self.ws.send(construct_update_recipe_sub_steps(recipe_list, sub_step_status_list))


def send_dummy_updates():
	wsclient = WSClient()
	for i in range(100):
		wsclient.dummy_update_steps()
		time.sleep(3)
		wsclient.dummy_update_sub_steps()
	wsclient.close()


if __name__ == "__main__":
	send_dummy_updates()
