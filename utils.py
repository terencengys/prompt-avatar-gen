import random
import json
import urllib
from urllib import request, parse

## Prompt section

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

## Comfy API section

def queue_prompt(prompt, server, client_id):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request(f"{server}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type, server):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"{server}/view?{url_values}") as response:
        return response.read()


def get_history(prompt_id, server):
    with urllib.request.urlopen(f"{server}/history/{prompt_id}") as response:
        return json.loads(response.read())


def get_images(ws, prompt, server, client_id):
    prompt_id = queue_prompt(prompt, server, client_id)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id, server)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'], server)
                    images_output.append(image_data)
            output_images[node_id] = images_output
    
    output = list(output_images.values())[0][0]
    print(len(output))
    return output
