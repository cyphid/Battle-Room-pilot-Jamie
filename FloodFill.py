#include
import typing

def move(game_state: typing.Dict = None) -> typing.Dict:
  if game_state is None:
    return {"up": 1,
            "down": 0,
            "left": 0,
            "right": 0
           }


  all_cells = {}
  for x in range(game_state.board.width):
    for y in range(game_state.board.height):
      all_cells[(game_state.Position(x, y))

  #find all walls
  walls = []
  for snake in game_state.board.snakes:
    for pos in snake.body:
      posx = pos.x
      posy = pos.y
      walls.append(game_state.Position(posx, posy))

  # start_actual_alg
  


  
  return {"up": 0,
          "down": 0,
          "left": 0,
          "right": 0
         }
