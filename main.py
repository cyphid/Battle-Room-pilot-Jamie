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

import random
import typing
from GameStateClasses import (Position, GameState, Game, Ruleset, Board,
Snake, Customisations)

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#1dbfbb",  # TODO: Choose color
        "head": "gamer",  # TODO: Choose head
        "tail": "coffee",  # TODO: Choose tail
    }
 
# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def closest_food(game_state: GameState, origin: Position):
  food_list = game_state.board.food
  closest_food_distance = 100000
  for food in food_list:
    diff_x = abs(game_state.you.head.x - food.x)
    diff_y = abs(game_state.you.head.y - food.y)
    total_distance = diff_x + diff_y
    if total_distance < closest_food_distance:
      closest_food_distance = total_distance
  return closest_food_distance
    
  

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    game_state = GameState(game_state)
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }
    
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state.you.body[0]  # Coordinates of your head
    my_neck = game_state.you.body[1]  # Coordinates of your "neck"

    if my_neck.x < my_head.x:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck.x > my_head.x:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck.y < my_head.y:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck.y > my_head.y:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds

    Board_width = game_state.board.width
    Board_height = game_state.board.height
    # we can remove the variables Board_width and Board_height
    if my_head.x == 0:
        is_move_safe["left"] = False
    if my_head.x == Board_width - 1:
       is_move_safe["right"] = False
    if my_head.y == 0: 
      is_move_safe["down"] = False
    if my_head.y == Board_height - 1:
      is_move_safe["up"] = False
    
        
  

    # DONE: Step 2 - Prevent your Battlesnake from colliding with itself
    my_snake = game_state.you
    my_snake_head = my_snake.head

    for snake in game_state.board.snakes:
      for segment in snake.body:
        if my_snake_head.x + 1 == segment.x and my_snake_head.y == segment.y:
          is_move_safe["right"] = False
        if my_snake_head.x - 1 == segment.x and my_snake_head.y == segment.y:
          is_move_safe["left"] = False
        if my_snake_head.y + 1 == segment.y and my_snake_head.x == segment.x:
          is_move_safe["up"] = False
        if my_snake_head.y - 1 == segment.y and my_snake_head.x == segment.x:
          is_move_safe["down"] = False

  
    # TODO: Step 3 - Find Food
    # dist = []
  
    # dist.append(closest_food(game_state, my_head + (0,1)  ))
    # dist.append(closest_food(game_state, my_head + (0,-1) ))
    # dist.append(closest_food(game_state, my_head + (1,0) ))
    # dist.append(closest_food(game_state, my_head + (-1,0) ))

    # min_dist = 1000000
    # for i in dist:
    #   if i < min_dist:
    #     min_dist = i
    
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    
    if len(safe_moves) == 0:
        print(f"MOVE {game_state.turn}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    # print(f"MOVE {game_state.turn}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
