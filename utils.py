import random
import json

def read_both_jsons(character_json_file, themes_json_file):
    with open(character_json_file, "r") as read_file:
        character_json = json.load(read_file)
    with open(themes_json_file, "r") as read_file:
        themes_json = json.load(read_file)
    return character_json, themes_json

def sample_and_join(str_list, number):
    sampled_list = random.sample(str_list, number)
    return ', '.join(sampled_list)

def make_into_list_and_join(*args):
    prompt_list = []
    for prompt in args:
        prompt_list.append(prompt)    
    return ', '.join(prompt_list)