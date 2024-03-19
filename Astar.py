import typing
from GameStateClasses import (Position, GameState, Game, Ruleset, Board, Snake, Customisations)


explored = typing.Dict[Position, Position]
allowedMoves = ("up", "down", "left", "right")


class Node:
  def __init__(self, _g, _h, _position: Position, _parent = None):
    self.g = _g
    self.h = _h
    self.f = self.g + self.h
    self.position = _position
    self.parent = _parent # needs to be able to store None

  def __eq__(self, other):
    if isinstance(other, Node):
      return self.position == other.position
    elif isinstance(other, Position):
      return self.position == other
    else:
      return False


def calc_h(start: Position, end: Position):
  return abs(start.x - end.x) + abs(start.y - end.y)

def is_available(game_state: GameState, pos_to_test: Position) -> bool:
# check if it is outside the border
  if pos_to_test.y < 0 or pos_to_test.y > game_state.board.height - 1:
    return False
  if pos_to_test.x < 0 or pos_to_test.x > game_state.board.width - 1:
    return False
  # check if it is a snake
  for snake in game_state.board.snakes:
    for segment in snake.body:
      if segment == pos_to_test:
        return False
  # check if it is a hazard (Royale only)

  # no obstacles
  return True
  
def get_neighbours(game_state: GameState, position: Position) -> typing.List[Position]:
  # return a list of 1, 2, 3, or 4 neighbouring nodes which are available to move to.
  # More inefficient than a gaming laptop battery
  neighbours = []
  for direction in allowedMoves:
    if direction == "up":
      neighbour = Position(position.x, position.y + 1)
    elif direction == "down":
      neighbour = Position(position.x, position.y - 1)
    elif direction == "left":
      neighbour = Position(position.x - 1, position.y)
    else:
      neighbour = Position(position.x + 1, position.y)
    if is_available(game_state, neighbour):
      neighbours.append(neighbour)
  return neighbours

def A_star(game_state: GameState, start: Position, end: Position) -> typing.List:
  if start == end:
    return [start]
  to_explore: typing.List = []
  explored: typing.Dict[Position, Position] = {}
  # key is a Position, and the value is the
  # node it came from
  to_explore.append(start)
  
  while len(to_explore) > 0:
    current_node = to_explore.pop(-1)
    neighbours = get_neighbours(game_state, current_node)
  # sorts them based on how far they are from the goal, in reverse order
  neighbours.sort(key=lambda x: abs(x - end), reverse=True)
  for neighbour in neighbours:
    if neighbour not in explored:
      explored[neighbour] = current_node
      to_explore.append(neighbour)
    if end in neighbours:
      break
  
  path = []
  if end not in explored:
    return [False]
  current_node = explored[end]
  while current_node != start:
    path.append(current_node)
    current_node = explored[current_node]
  path.append(start)
  path.reverse()
  return path



def move(game_state: typing.Dict = None) -> typing.Dict:
  game_state = GameState(game_state)
  direction = ""
  food_distances = []
  for food in game_state.board.food:
    food_distances.append(abs(head - food))
  closest_food = game_state.board.food[food_distances.index(min(food_distances))]
  A_star_path = A_star(game_state, game_state.you.head, closest_food)
  if A_star_path[-2].x == A_star_path[-1].x + 1:
    direction = "right"
  elif A_star_path[-2].x == A_star_path[-1].x - 1:
    direction = "left"
  elif A_star_path[-2].y == A_star_path[-1].y + 1:
    direction = "up"
  else:
    direction = "down"
  output = {"up": 0, "down": 0, "left": 0, "right": 0}
  output[direction] += 4
  print(output)
  return output