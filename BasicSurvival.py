import typing
from GameStateClasses import (Position, GameState, Game, Ruleset, Board, Snake, Customisations)

def move(game_state: typing.Dict = None) -> typing.Dict:
  game_state = GameState(game_state)

  up = 0
  down = 0
  left = 0
  right = 0
  
  if game_state is None:
    return {"up": 1,
            "down": 0,
            "left": 0,
            "right": 0
           }

  if game_state.you.body[0].x == game_state.board.width -1: # Board edge detection
    right = -10
  if game_state.you.body[0].x == 0:
    left = -10
  if game_state.you.body[0].y == game_state.board.height -1:
    up =   -10
  if game_state.you.body[0].y == 0:
    down = -10

  # Don't hit your own neck

  for food in game_state.board.food: # immediate food detection
    if food.x == game_state.you.body[0].x -1 and food.y == game_state.you.body[0].y: #⬅️
      left  += 5
    if food.x == game_state.you.body[0].x +1 and food.y == game_state.you.body[0].y: #➡️
      right += 5
    if food.y == game_state.you.body[0].y -1 and food.x == game_state.you.body[0].x: #⬆️
      up    += 5
    if food.y == game_state.you.body[0].y +1 and food.x == game_state.you.body[0].x: #⬇️
      down  += 5

  for snake in game_state.board.snakes: # avoid immediate snakes
    for pos in snake.body:
      if pos.x == game_state.you.body[0].x -1 and pos.y == game_state.you.body[0].y: #⬅️
        left =  -10
      if pos.x == game_state.you.body[0].x +1 and pos.y == game_state.you.body[0].y: #➡️
        right = -10
      if pos.y == game_state.you.body[0].y -1 and pos.x == game_state.you.body[0].x: #⬆️
        down =  -10
      if pos.y == game_state.you.body[0].y +1 and pos.x == game_state.you.body[0].x: #⬇️
        up =    -10

  for snake in game_state.board.snakes: # avoid head to head collisions
    if snake.length < game_state.you.length: # check if snake is smaller
      continue
    if snake.head.x == game_state.you.body[0].x -1 and snake.head.y == game_state.you.body[0].y -1: # ↙
      left  -=5
      up    -=5
    if snake.head.x == game_state.you.body[0].x +1 and snake.head.y == game_state.you.body[0].y -1: # ↘️
      right -=5
      up    -=5
    if snake.head.x == game_state.you.body[0].x +1 and snake.head.y == game_state.you.body[0].y +1: # ↗
      right -=5
      down  -=5
    if snake.head.x == game_state.you.body[0].x -1 and snake.head.y == game_state.you.body[0].y +1: # ↖️
      left  -=5
      down  -=5
    if snake.head.x == game_state.you.body[0].x -2 and snake.head.y == game_state.you.body[0].y: # ←←
      left  -=5
    if snake.head.x == game_state.you.body[0].x +2 and snake.head.y == game_state.you.body[0].y: # →→
      right -=5
    if snake.head.y == game_state.you.body[0].y -2 and snake.head.x == game_state.you.body[0].x: # ↑↑
      up    -=5
    if snake.head.y == game_state.you.body[0].y +2 and snake.head.x == game_state.you.body[0].x: # ↓↓
      down  -=5
  # your function should return a dictionary with the following keys:

  return {"up": up,
          "down": down,
          "left": left,
          "right": right
         }