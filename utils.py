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


def random_sample_and_join(str_list, optional=True):
    # Up to 1/3 the number of elements in str_list
    if optional:
        min_no = 0
    else:
        min_no = 1
    
    try:
        random_number = random.randint(min_no, len(str_list)//2)
    except ValueError:
        random_number = 1
    return sample_and_join(str_list, random_number)


def make_into_list_and_join(*args):
    prompt_list = []
    for prompt in args:
        prompt_list.append(prompt)
    return ', '.join(prompt_list)


def sample_gender(gender):
    gender_dict = {
        "male": [
            "moustache",
            "beard",
            ],
        "female": [
            "long eyelashes",
            "lipstick"
            ]
    }
    if gender == "male":
        return f"male, man, {random_sample_and_join(gender_dict[gender])}"
    elif gender == "female":
        return  f"female, woman, {random_sample_and_join(gender_dict[gender])}"
    else:
        # Nonbinary chooses from all gender attributes
        return random_sample_and_join(gender_dict["male"]+gender_dict["female"])
