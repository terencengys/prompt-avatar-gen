import random
from utils import *
import json
import uuid
import configparser
import websocket
import face_recognition
import os
import cv2
import numpy as np

client_id = str(uuid.uuid4())

CHARACTER_JSON = "character.json"
THEMES_JSON = "themes.json"
CONFIG_INI = "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_INI)

COMFY_SERVER = config.get("Comfy", "COMFY_SERVER")
# OUTPUT_DIR = config.get("Comfy", "OUTPUT_DIR")
API_JSON = config.get("Comfy", "API_JSON")
PROMPT_FIELD_LOC = config.get("Comfy", "PROMPT_FIELD_LOC")
INPUT_IMG_DIR = config.get("Comfy", "INPUT_IMG_DIR")
TEMP_IMG_DIR = config.get("Comfy", "TEMP_IMG_DIR")

def build_prompt(gender_string, theme_string):
    # Convert all to lowercase and remove spaces
    gender = gender_string.lower().strip()
    theme = theme_string.lower().strip()

    # Main prompt builder function
    character_json, themes_json = read_both_jsons(CHARACTER_JSON, THEMES_JSON)
    
    if theme == "random":
        theme = random.choice(get_themes_list())

    color_list = character_json["colors"]
    skin_tone_list = character_json["skin_tone"]

    # Gender
    gender_str = sample_gender(gender)

    # Facial features (may be omitted if using controlnet on photographs)
    face_str = f"{random.choice(color_list)} eyes, {random.choice(color_list)} hair, {random.choice(skin_tone_list)} complexion, "

    # Facial expressions (TODO)

    # Clothing
    # Max 1, color modifier
    clothing_list = themes_json[theme]["clothing"]
    clothing_str = sample_and_join(clothing_list, 1)
    clothing_str = f"{random.choice(color_list)} {clothing_str}"

    # Clothing Accessories
    # Max _, color modifier
    clothing_acc_list =  themes_json[theme]["clothing_acc"]

    for index, value in enumerate(clothing_acc_list):
        clothing_acc_list[index] = f"{random.choice(color_list)} {value}"

    clothing_acc_str = random_sample_and_join(clothing_acc_list)

    # Eyewear
    # Max 1
    eyewear_list = themes_json[theme]["eyewear"]
    eyewear_str = random_sample_and_join(eyewear_list)

    # Background
    # Max 1/3 of total no. of elements
    background_list = themes_json[theme]["background"]
    background_str = random_sample_and_join(background_list, False)
    
    prompt_str = make_into_list_and_join(
        gender_str,
        face_str,
        clothing_str,
        clothing_acc_str,
        eyewear_str,
        background_str
        ).replace(', , ', ', ')
    
    return f"{theme}, {prompt_str.replace(', , ', ', ')}, "
    
def send_prompt(gender, theme):
    gen_prompt = build_prompt(gender, theme)

    with open(API_JSON) as file:
        api_json = json.load(file)

    api_json[PROMPT_FIELD_LOC]["inputs"]["Text"] = gen_prompt

    ws = websocket.WebSocket()

    ws.connect(f"ws://{COMFY_SERVER[7:]}/ws?clientId={client_id}")
    images = get_images(ws, api_json, COMFY_SERVER, client_id)

    return images

def get_themes_list():
    # Read and return list of themes
    _, themes_json = read_both_jsons(CHARACTER_JSON, THEMES_JSON)
    themes_list = list(themes_json.keys())
    themes_list.remove("template")
    return(themes_list)

def send_prompt_with_img(gender, theme, img):
    gen_prompt = build_prompt(gender, theme)

    image = img.file.read()
    # TODO Resize image if too large as it causes segfault
    
    img_array = cv2.imdecode(np.frombuffer(image,np.uint8), cv2.IMREAD_COLOR)
    face_locations = face_recognition.face_locations(img_array)

    # Assume only one face per img
    top, right, bottom, left = face_locations[0]
    top_1 = top - (bottom-top)//2
    bottom_1 = bottom + (bottom-top)//2
    right_1 = right + (right-left)//2
    left_1 = left - (right-left)//2
    face_image = cv2.resize(img_array[top_1:bottom_1, left_1:right_1], (512,512))
    cv2.imwrite(f"{INPUT_IMG_DIR}/input.jpg", face_image)
    
    with open(API_JSON) as file:
        api_json = json.load(file)

    api_json[PROMPT_FIELD_LOC]["inputs"]["Text"] = gen_prompt

    ws = websocket.WebSocket()

    ws.connect(f"ws://{COMFY_SERVER[7:]}/ws?clientId={client_id}")
    images = get_images(ws, api_json, COMFY_SERVER, client_id)

    os.remove(f"{INPUT_IMG_DIR}/input.jpg")

    return images


# if __name__ == "__main__":
#     print(build_prompt('male', 'astronaut'))
