import json
import random
from copy import deepcopy

import requests
import inquirer

from os.path import exists

CHAMP_FILE_PATH = "../champs.json"

def load_champs():
  if exists(CHAMP_FILE_PATH):
    with open(CHAMP_FILE_PATH, "r") as f:
      print(f"loaded champions from {CHAMP_FILE_PATH}")

      return json.load(f)
  else:

    print(f"failed to find {CHAMP_FILE_PATH}, fetching champions...")

    champs = {}

    champ_ids = list(fetch_champs().keys())

    for champ_id in champ_ids:
    
      print(f"loading {champ_id}...")

      champs[champ_id] = fetch_champ(champ_id)

    with open(CHAMP_FILE_PATH, 'w', encoding='utf-8') as f:
      json.dump(champs, f, ensure_ascii=False, indent=4)

    print(f"finished fetching champions, writing to {CHAMP_FILE_PATH}")

    return champs

class ChampProvider:

  def __init__(self):
    self.champs = load_champs()

  def choose_champ(self):

    champs = list(self.champs.values())

    # [ ("Aatrox", "Aatrox"), ("Ahri", "Ahri"), ... ]
    champ_choices = [(champ["name"], champ["id"]) for champ in champs]

    chosen_champ_id = inquirer.prompt([
      inquirer.List(
        "champ_id",
        "choose your champion",
        choices=champ_choices
      )
    ])["champ_id"]

    return self.get_champ(chosen_champ_id)

  def get_random_champ(self):
    
    champ_ids = list(self.champs.keys())
    
    random_champ_id = random.choice(champ_ids)

    return self.get_champ(random_champ_id)

  def get_champ(self, champ_id):

    # if we didn't use deepcopy, modifying one champion returned by this function would also 
    # modify all others returned in the future.
    # see https://levelup.gitconnected.com/understanding-reference-and-copy-in-python-c681341a0cd8
  
    return deepcopy(self.champs[champ_id])

  def choose_ability(self, champ_id):

    abilities = self.champs[champ_id]["spells"]

    # [ ("The Darkin Blade", 0), ("Infernal Chains", 1), ... ]
    ability_choices = [(ability["name"], idx) for idx, ability in enumerate(abilities)] 

    chosen_ability_idx = inquirer.prompt([
      inquirer.List(
        "ability_idx",
        "choose your ability",
        choices=ability_choices
      )
    ])["ability_idx"]

    return self.get_ability_by_idx(champ_id, chosen_ability_idx)

  def get_random_ability(self, champ_id):

    ability_indices = [idx for idx, ability in enumerate(self.champs[champ_id]["spells"])]

    random_ability_idx = random.choice(ability_indices)

    return self.get_ability_by_idx(champ_id, random_ability_idx)

  def get_ability_by_idx(self, champ_id, ability_idx):
  
    # regarding use of deepcopy see comment in ChampProvider.get_champ definition
  
    return deepcopy(self.champs[champ_id]["spells"][ability_idx])



def fetch_champ(champion_id):

  # https://developer.riotgames.com/docs/lol#data-dragon_champions

  url = f"https://ddragon.leagueoflegends.com/cdn/12.13.1/data/en_US/champion/{champion_id}.json"

  res = requests.get(url)

  json = res.json()

  champ = json["data"][champion_id]

  return champ

def fetch_champs():

  # https://developer.riotgames.com/docs/lol#data-dragon_champions

  url = "https://ddragon.leagueoflegends.com/cdn/12.13.1/data/en_US/champion.json"

  res = requests.get(url)

  json = res.json()

  champs = json["data"]

  return champs