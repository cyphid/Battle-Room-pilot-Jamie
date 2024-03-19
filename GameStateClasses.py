import typing
from dataclasses import dataclass


@dataclass(order=False, frozen=True)
class Position:
  x: int
  y: int

  def __str__(self) -> str:
    return f"({self.x}, {self.y})"

  def __repr__(self) -> None:
    return str(self)

  def __add__(self, other):
    if isinstance(other, Position):
      return Position(self.x + other.x, self.y + other.y)
    elif isinstance(other, tuple):
      return Position(self.x + other[0], self.y + other[1])
    else:
      raise TypeError(
          f"unsupported operand type(s) for +: 'Position' and '{type(other)}'")

  def __sub__(self, other):
    if isinstance(other, Position):
      return Position(self.x - other.x, self.y - other.y)
    elif isinstance(other, tuple):
      return Position(self.x - other[0], self.y - other[1])
    else:
      raise TypeError(
          f"unsupported operand type(s) for -: 'Position' and '{type(other)}'")

  # returns the manhatten distance between two positions
  def __abs__(self):
    return abs(self.x) + abs(self.y)


@dataclass(order=False, frozen=True)
class Customisations:
  color: str
  head: str
  tail: str


@dataclass(order=False)
class Snake:

  id: str
  name: str
  health: int
  body: typing.List[Position]
  head: Position
  length: int
  shout: str
  customisations: Customisations

  def __init__(self, snake_dict) -> None:
    self.id: str = snake_dict["id"]
    self.name: str = snake_dict["name"]
    self.health: int = snake_dict["health"]
    self.body: typing.List[Position] = [
        Position(**i) for i in snake_dict["body"]
    ]
    self.head: Position = Position(**snake_dict["head"])
    self.length: int = snake_dict["length"]
    self.shout: str = snake_dict["shout"]
    self.customisations: Customisations = Customisations(
        **snake_dict["customizations"])

  def __eq__(self, other):
    if isinstance(other, Snake):
      return self.id == other.id
    else:
      raise TypeError(
          f"unsupported operand type(s) for ==: 'Snake' and '{type(other)}'")


@dataclass(order=False)
class Board:

  height: int
  width: int
  food: typing.List[Position]
  snakes: typing.List[Snake]
  hazards: typing.List[Position]

  def __init__(self, board_dict) -> None:
    self.height: int = board_dict["height"]
    self.width: int = board_dict["width"]
    self.food: typing.List[Position] = [
        Position(**i) for i in board_dict["food"]
    ]
    self.snakes: typing.List[Snake] = [Snake(i) for i in board_dict["snakes"]]
    self.hazards: typing.List[Position] = [
        Position(**i) for i in board_dict["hazards"]
    ]


@dataclass(order=False)
class Squad:

  allow_body_collisions: bool
  shared_elimination: bool
  shared_health: bool
  shared_length: bool

  def __init__(self, squad_dict) -> None:
    self.allow_body_collisions: bool = squad_dict["allowBodyCollisions"]
    self.shared_elimination: bool = squad_dict["sharedElimination"]
    self.shared_health: bool = squad_dict["sharedHealth"]
    self.shared_length: bool = squad_dict["sharedLength"]


@dataclass(order=False)
class Royale:
  shrink_every_n_turns: int

  def __init__(self, royale_dict) -> None:
    self.shrink_every_n_turns: int = royale_dict["shrinkEveryNTurns"]


@dataclass(order=False)
class Settings:
  food_spawn_chance: int
  minimum_food: int
  hazard_damage_per_turn: int
  royale: Royale
  squad: Squad

  def __init__(self, settings_dict) -> None:
    self.food_spawn_chance: int = settings_dict["foodSpawnChance"]
    self.minimum_food: int = settings_dict["minimumFood"]
    self.hazard_damage_per_turn: int = settings_dict["hazardDamagePerTurn"]
    self.royale: Royale = Royale(settings_dict["royale"])
    self.squad: Squad = Squad(settings_dict["squad"])


@dataclass(order=False)
class Ruleset:
  name: str
  version: str
  settings: Settings

  def __init__(self, ruleset_dict) -> None:
    self.name: str = ruleset_dict["name"]
    self.version: str = ruleset_dict["version"]
    self.settings: Settings = Settings(ruleset_dict["settings"])


@dataclass(order=False)
class Game:
  id: str
  ruleset: Ruleset
  map: str
  timeout: int
  source: str

  def __init__(self, game_dict: typing.Dict) -> None:
    self.id: str = game_dict["id"]
    self.ruleset: Ruleset = Ruleset(game_dict["ruleset"])
    self.map: str = game_dict["map"]
    self.timeout: int = game_dict["timeout"]
    self.source: str = game_dict["source"]


@dataclass(order=False)
class GameState:
  game: Game
  board: Board
  you: Snake
  turn: int

  def __init__(self, current_game_state) -> None:
    self.game: Game = Game(current_game_state["game"])
    self.board: Board = Board(current_game_state["board"])
    self.you: Snake = Snake(current_game_state["you"])
    self.turn: int = current_game_state["turn"]
