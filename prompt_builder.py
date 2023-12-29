import random
from utils import *
import json

CHARACTER_JSON = "character.json"
THEMES_JSON = "themes.json"

def build_prompt(gender, theme):
    # Main prompt builder function
    # character_json, themes_json = read_both_jsons(CHARACTER_JSON, THEMES_JSON)
    
    if theme == "random":
        theme = random.choice(get_themes_list())
    return theme

def get_themes_list():
    # Read and return list of themes
    _, themes_json = read_both_jsons(CHARACTER_JSON, THEMES_JSON)
    themes_list = list(themes_json.keys())
    return themes_list
