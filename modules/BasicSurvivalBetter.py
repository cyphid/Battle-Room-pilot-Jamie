import typing
from GameStateClasses import (Position, GameState, Game, Ruleset, Board, Snake, Customisations)

def update_for_board_edges(game_state, up, down, left, right):
    if game_state.you.body[0].x == game_state.board.width - 1:
        right = -10
    if game_state.you.body[0].x == 0:
        left = -10
    if game_state.you.body[0].y == game_state.board.height - 1:
        up = -10
    if game_state.you.body[0].y == 0:
        down = -10
    return up, down, left, right

def update_for_food(game_state, up, down, left, right):
    for food in game_state.board.food:
        if food.x == game_state.you.body[0].x - 1:
            left += 5
        if food.x == game_state.you.body[0].x + 1:
            right += 5
        if food.y == game_state.you.body[0].y - 1:
            up += 5
        if food.y == game_state.you.body[0].y + 1:
            down += 5
    return up, down, left, right

def update_for_snake_bodies(game_state, up, down, left, right):
    for snake in game_state.board.snakes:
        for pos in snake.body:
            if pos.x == game_state.you.body[0].x - 1:
                left = -10
            if pos.x == game_state.you.body[0].x + 1:
                right = -10
            if pos.y == game_state.you.body[0].y - 1:
                down = -10
            if pos.y == game_state.you.body[0].y + 1:
                up = -10
    return up, down, left, right

def update_for_head_to_head_collisions(game_state, up, down, left, right):
    for snake in game_state.board.snakes:
        if snake.length >= game_state.you.length:
            # Adjust logic for proximity and direction
            # This is an example and may need adjustment based on your game's logic
            pass # Implement similar to existing logic
    return up, down, left, right

def move(game_state: typing.Dict = None) -> typing.Dict:
    game_state = GameState(game_state)

    up = down = left = right = 0

    if game_state is None:
        return {"up": 1, "down": 0, "left": 0, "right": 0}

    up, down, left, right = update_for_board_edges(game_state, up, down, left, right)
    up, down, left, right = update_for_food(game_state, up, down, left, right)
    up, down, left, right = update_for_snake_bodies(game_state, up, down, left, right)
    up, down, left, right = update_for_head_to_head_collisions(game_state, up, down, left, right)

    return {"up": up, "down": down, "left": left, "right": right}
