# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import numpy as np
import os
import importlib
#import scipy 
# ^ requires a later version of python
import random
import typing
from GameStateClasses import (Position, GameState, Game, Ruleset, Board, Snake, Customisations)
example_game_state = {
  "game": {
    "id": "totally-unique-game-id",
    "ruleset": {
      "name": "standard",
      "version": "v1.1.15",
      "settings": {
        "foodSpawnChance": 15,
        "minimumFood": 1,
        "hazardDamagePerTurn": 14,
        "royale": {
          "shrinkEveryNTurns": -1
        },
        "squad": {
          "allowBodyCollisions": True,
          "sharedElimination": True,
          "sharedHealth": True,
          "sharedLength": True
        }
      }
    },
    "map": "standard",
    "source": "league",
    "timeout": 500
  },
  "turn": 14,
  "board": {
    "height": 11,
    "width": 11,
    "food": [
      {"x": 5, "y": 5},
      {"x": 9, "y": 0},
      {"x": 2, "y": 6}
    ],
    "hazards": [
      {"x": 3, "y": 2}
    ],
    "snakes": [
      {
        "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [
          {"x": 0, "y": 0},
          {"x": 1, "y": 0},
          {"x": 2, "y": 0}
        ],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "customizations":{
          "color":"#FF0000",
          "head":"pixel",
          "tail":"pixel"
        }
      },
      {
        "id": "snake-b67f4906-94ae-11ea-bb37",
        "name": "Another Snake",
        "health": 16,
        "body": [
          {"x": 5, "y": 4},
          {"x": 5, "y": 3},
          {"x": 6, "y": 3},
          {"x": 6, "y": 2}
        ],
        "latency": "222",
        "head": {"x": 5, "y": 4},
        "length": 4,
        "shout": "I'm not really sure...",
        "customizations":{
          "color":"#26CF04",
          "head":"silly",
          "tail":"curled"
        }
      }
    ]
  },
  "you": {
    "id": "snake-508e96ac-94ad-11ea-bb37",
    "name": "My Snake",
    "health": 54,
    "body": [
      {"x": 0, "y": 0},
      {"x": 1, "y": 0},
      {"x": 2, "y": 0}
    ],
    "latency": "111",
    "head": {"x": 0, "y": 0},
    "length": 3,
    "shout": "why are we shouting??",
    "customizations": {
      "color":"#FF0000",
      "head":"pixel",
      "tail":"pixel"
    }
  }
}
irreleventFiles = ("main.py", "Template.py", "test.py", "GameStateClasses.py", "server.py", "FloodFill.py")


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data

# 
def instantiate_modules() -> typing.Tuple:
  files = [file[:-3] for file in os.listdir() if ".py" in file and file not in irreleventFiles]
  modulesDict = {file:None for file in files}
  for file in files:
    modulesDict[file] = importlib.import_module(file)
    print(f"successfully imported {file}")
    print(f"{modulesDict[file]}")
  return modulesDict

def info() -> typing.Dict:
  print("INFO")
  return {
    "apiversion": "1",
    "author": "",  
    "color": "#1dbfbb", 
    "head": "gamer",
    "tail": "coffee"
  }

# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data

def get_recommendations(game_state: typing.Dict, algorithmModules: typing.Dict) -> typing.List[typing.Dict]:
    recommendations = []
    for module in algorithmModules.values():
        if hasattr(module, "move"):
            recommendations.append(module.move(game_state))
    return recommendations

def aggregate_recommendations(recommendations: typing.List[typing.Dict]) -> typing.Dict:
    viable_moves = {"up": 0, "down": 0, "left": 0, "right": 0}
    for direction in viable_moves.keys():
        viable_moves[direction] = sum(move[direction] for move in recommendations)
    return viable_moves

def softmax_dict(viable_moves: typing.Dict) -> typing.Dict:
    viable_moves = {key: np.exp(value) for key, value in viable_moves.items()}
    original_sum = sum(viable_moves.values())
    for direction in viable_moves.keys():
        viable_moves[direction] /= original_sum
    return viable_moves

def print_probabilities(viable_moves: typing.Dict):
    for move, probability in viable_moves.items():
        print(f"{move}: {probability:.3f}", end=" ")

def choose_move(viable_moves: typing.Dict) -> str:
    return random.choices(tuple(viable_moves.keys()), weights=tuple(viable_moves.values()))[0]

def move(game_state: typing.Dict = None) -> typing.Dict:
  global algorithmModules
  # For testing purposes  
  if game_state is None:
        game_state = example_game_state

  recommendations = get_recommendations(game_state, algorithmModules)
  aggregated_scores = aggregate_recommendations(recommendations)
  probabilities = softmax_dict(aggregated_scores)
  print_probabilities(probabilities)
  our_move = choose_move(probabilities)
  print(" 🎲-> " + our_move)

  return {"move": our_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  # pre-processing import modules
  global algorithmModules
  algorithmModules = instantiate_modules()

  
  run_server({
      "info": info, 
      "start": start, 
       "move": move, 
      "end": end
  })

