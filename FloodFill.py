#include
import typing

def move(game_state: typing.Dict = None) -> typing.Dict:
  if game_state is None:
    return {"up": 1,
            "down": 0,
            "left": 0,
            "right": 0
           }


  # your function should return a dictionary with the following keys:

  return {"up": 0,
          "down": 0,
          "left": 0,
          "right": 0
         }
