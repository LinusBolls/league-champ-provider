import random

import inquirer

from champ_provider import ChampProvider

champ_provider = ChampProvider()

def round(player_champ, ai_champ):

  player_action = champ_provider.choose_ability(player_champ["id"])

  print("you chose " + player_action["name"])

  ai_action = champ_provider.get_random_ability(ai_champ["id"])

  print("your opponent chose " + ai_action["name"])

while True:

  player_champ = champ_provider.choose_champ()

  print("you chose " + player_champ["name"] + " as your champion")

  ai_champ = champ_provider.get_random_champ()

  print("your opponent chose " + ai_champ["name"] + " as their champion")

  while True:

    round(player_champ, ai_champ)