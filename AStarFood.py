import typing
from queue import PriorityQueue


def a_star_search(start, goal, obstacles, grid_size):

  def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

  frontier = PriorityQueue()
  frontier.put((0, start))
  came_from = {start: None}
  cost_so_far = {start: 0}

  while not frontier.empty():
    current = frontier.get()[1]

    if current == goal:
      break

    for next in [(current[0] + dx, current[1] + dy)
                 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                 if 0 <= current[0] + dx < grid_size[0] and 0 <= current[1] +
                 dy < grid_size[1]]:
      if next in obstacles:
        continue
      new_cost = cost_so_far[current] + 1  # Constant cost for moving
      if next not in cost_so_far or new_cost < cost_so_far[next]:
        cost_so_far[next] = new_cost
        priority = new_cost + heuristic(goal, next)
        frontier.put((priority, next))
        came_from[next] = current

  path = []
  current = goal
  while current != start:
    path.append(current)
    current = came_from.get(current)
    if current is None:
      return []  # No path found
  path.reverse()  # Reverse it since we built it backwards
  return path


def move(game_state: typing.Dict):
  my_head = (game_state["you"]["body"][0]['x'],
             game_state["you"]["body"][0]['y'])
  food_locations = [(food['x'], food['y'])
                    for food in game_state['board']['food']]
  obstacles = {(part['x'], part['y'])
               for snake in game_state['board']['snakes']
               for part in snake['body']}
  grid_size = (game_state['board']['width'], game_state['board']['height'])

  # Find path to the closest food
  closest_food = None
  shortest_path = []
  for food in food_locations:
    path = a_star_search(my_head, food, obstacles, grid_size)
    if path and (not shortest_path or len(path) < len(shortest_path)):
      shortest_path = path
      closest_food = food

  # Determine the first move towards the closest food
  safe_moves_towards_food = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
  if shortest_path:
    next_step = shortest_path[0]
    dx = next_step[0] - my_head[0]
    dy = next_step[1] - my_head[1]

    score_value = 5
    if dx == -1:
      safe_moves_towards_food['left'] = score_value
    elif dx == 1:
      safe_moves_towards_food['right'] = score_value
    if dy == -1:
      safe_moves_towards_food['down'] = score_value
    elif dy == 1:
      safe_moves_towards_food['up'] = score_value
  return safe_moves_towards_food

# def estimateMovesToSegmentClearance(game_state: typing.Dict, segment: typing.Tuple[int, int], segment_length: int):
  


# Ideas for computing when a space occupied by a snake will become available
# the index into the snake's body will determine its distance from the head. Therefore, the distance from the tail is the total length of the snake minus the index. i.e. distance_from_tail = len(snake) - snake.index(segment)
# Recall that the distance from the tail is equal to the number of moves until the space becomes available, and also the A* tracks the number of turns it took to reach a spot. If the number of moves to reach a segment exceeds the distance from the tail, then the space is available, and A* can safely ignore the offending segment. i.e.
# if g_cost > distance_from_tail(segment):
#   ignore segment