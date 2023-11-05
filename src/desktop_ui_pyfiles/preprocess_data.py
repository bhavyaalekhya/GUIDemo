import os
import json


def preprocess_step_files(recipe_step_directory, output_step_template_directory):
	os.makedirs(output_step_template_directory, exist_ok=True)
	for recipe_file in os.listdir(recipe_step_directory):
		recipe_file_path = os.path.join(recipe_step_directory, recipe_file)
		step_template_list = []
		with open(recipe_file_path, 'r') as file:
			for line in file:
				line = line.strip()
				# State : 0 -> Not Done, 1 -> Error, 2 -> Done
				item = {"step": line, "state": 0}
				step_template_list.append(item)
		
		# Save the list as a json file
		output_step_template_file_path = os.path.join(output_step_template_directory, recipe_file)
		with open(output_step_template_file_path, 'w') as file:
			json.dump(step_template_list, file)


def preprocess_sub_step_files(recipe_sub_step_directory, output_sub_step_template_directory):
	os.makedirs(output_sub_step_template_directory, exist_ok=True)
	for recipe_sub_step_file in os.listdir(recipe_sub_step_directory):
		recipe_sub_step_file_path = os.path.join(recipe_sub_step_directory, recipe_sub_step_file)
		with open(recipe_sub_step_file_path, 'r') as file:
			instructions = file.read()
		
		# Splitting the instructions into steps
		steps = instructions.strip().split("Step")
		
		# Parsing each step and its sub-steps into a dictionary
		recipe_state_dict_list = []
		for step in steps:
			if step:  # Check if step is not empty
				step_lines = step.strip().split("\n")
				step_number = step_lines[0].split(":")[0].strip()  # Extract step number
				step_description = step_lines[0].split(":")[1].strip()  # Extract step description
				sub_steps = [sub_step.strip() for sub_step in step_lines[1:]]  # Extract sub-steps
				# Remove the serial number from each sub-step
				sub_steps = [sub_step.split(". ", 1)[-1] for sub_step in sub_steps]
				sub_step_dict_list = []
				for sub_step_description in sub_steps:
					# State : 0 -> Not Done, 1 -> In Progress, 2 -> Done, 3 -> Missing, 4 -> Ordering,
					# 5 -> Technique, 6 -> Preparation
					sub_step_dict = {
						"sub_step": sub_step_description,
						"state": 0
					}
					sub_step_dict_list.append(sub_step_dict)
				
				recipe_state_dict_list.append({
					"step": step_description,
					"sub_steps": sub_step_dict_list
				})
		
		# Save the dictionary as a json file
		output_sub_step_template_file_path = os.path.join(output_sub_step_template_directory, recipe_sub_step_file)
		with open(output_sub_step_template_file_path, 'w') as file:
			json.dump(recipe_state_dict_list, file)


if __name__ == '__main__':
	preprocess_step_files("recipe_steps", "recipe_steps_templates")
	preprocess_sub_step_files("recipe_sub_steps", "recipe_sub_steps_templates")
