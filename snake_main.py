import game_parameters
from snake import Snake
from game_display import GameDisplay
from apple import Apple
from bomb import Bomb
from typing import List, Any


# put snake on board
# put bomb on board
# put apples on board
# end round

def main_loop(gd: GameDisplay) -> None:
    # the main loop is in charge on the continuity of the game and stops it if the user lost or won

    taken_coors = []
    score = 0
    apple_list = []
    i = 1
    stop_growing_round = -1

    bomb = create_bomb(i, gd)
    snake = Snake((10, 10), 3)
    # taken_coors+=snake.get_coordinates()
    for t in range(3):
        apple = creat_apple(taken_coors)
        apple_list.append(apple)
        taken_coors.append(apple.get_location())

    draw_board(apple_list, bomb, snake, gd)
    gd.show_score(0)
    gd.end_round()
    # print('score:', score, 'snake:', snake.get_coordinates(), 'bomb:', bomb.get_location())

    while True:
        taken_coors = snake.get_coordinates() + bomb.get_location() + get_apples_location(apple_list)
        key_clicked = gd.get_key_clicked()

        bomb_set_up(bomb, i, gd, taken_coors)
        move_snake = snake.move_snake(key_clicked)
        if not move_snake:
            # snake.cut_head()
            draw_board(apple_list, bomb, snake, gd)
            # print('score:', score, 'snake:', snake.get_coordinates(), 'bomb:', bomb.get_location())
            gd.end_round()
            return

        if set(bomb.get_location()).intersection(snake.get_coordinates()):
            draw_board(apple_list, bomb, snake, gd)
            # print('score:', score, 'snake:', snake.get_coordinates(), 'bomb:', bomb.get_location())
            gd.end_round()
            return
            break

        if snake.check_collide():
            snake.cut_head()
            draw_board(apple_list, bomb, snake, gd)
            # print('score:', score, 'snake:', snake.get_coordinates(), 'bomb:', bomb.get_location())
            gd.end_round()
            return

        # if check_lost(snake, bomb):
        #     draw_board(apple_list, bomb, snake, gd)
        #     gd.end_round()
        #     break
        #

        score, stop_growing_round, apple_list = apple_set_up(snake, bomb, apple_list, score, stop_growing_round, i,
                                                             taken_coors)

        draw_board(apple_list, bomb, snake, gd)

        gd.show_score(score)
        i += 1
        # print('score:', score, 'snake:', snake.get_coordinates(), 'bomb:', bomb.get_location())
        gd.end_round()
    return


def apple_set_up(snake, bomb, apple_list, score, stop_growing_round, i, taken_coors):
    add_to_score, snake_ate_apple = check_apple(snake, bomb, apple_list)
    score += add_to_score
    if snake_ate_apple:
        if stop_growing_round > i:
            stop_growing_round += 3
        else:
            stop_growing_round = i + 3
        snake.change_ate_apple(True)
    if i == stop_growing_round:
        snake.change_ate_apple(False)
    while len(apple_list) < 3:
        apple = creat_apple(taken_coors)
        apple_list.append(apple)

    return score, stop_growing_round, apple_list


def get_apples_location(apple_list):
    apple_coors = []
    for apple in apple_list:
        apple_coors.append(apple.get_location())
    return apple_coors


def draw_board(apple_list, bomb, snake, gd):
    # draws all items on board
    # print(snake.get_coordinates())
    # print(bomb.get_location())
    draw_snake(snake, gd)
    draw_bomb(bomb, gd)
    for apple in apple_list:
        draw_apple(apple, gd)


def creat_apple(taken_coors):
    """
    :param apple_list: a list contains all apples that are in game
    :param taken_coors: list of coordinates that are taken by other object
    creates an apple in a place that is not taken and adds it to the list
    """
    x, y, apple_score = game_parameters.get_random_apple_data()
    while not check_empty((x, y), taken_coors):
        x, y, apple_score = game_parameters.get_random_apple_data()
    apple = Apple((x, y), apple_score)
    taken_coors.append(apple.get_location())
    return apple


def check_empty(coor, taken_coors):
    # True if the coordinate given is empty, False if it is taken
    if coor in taken_coors:
        return False
    return True


def check_apple(snake, bomb, apple_lst: List):
    """
    :param apple_lst: list of apples that are created and not destroyed yet
    makes all checks concerning the apples:
    if the snake ate the apple, if the bomb destroyed the apple
    :return: if the snake ate the apple : the score of the apple, True
             else: 0, False
    """
    score = 0
    snake_ate_apple = False
    bomb_coor = bomb.get_location()
    snake_head_location = snake.get_coordinates()[0]
    for apple in apple_lst:
        if apple.get_location() in bomb_coor:
            apple_lst.remove(apple)
        if apple.get_location() == snake_head_location:
            apple_lst.remove(apple)
            score += apple.get_score()
            snake_ate_apple = True
    return score, snake_ate_apple


def check_lost(snake, bomb):
    if snake.check_collide():
        snake.cut_head()
        return True
    snake_coor = snake.get_coordinates()
    bomb_coor = bomb.get_location()
    for coor in snake_coor:
        if coor in bomb_coor:
            return True
    return False


def draw_snake(snake, gd):
    snake_coor = snake.get_coordinates()
    for coor in snake_coor:
        gd.draw_cell(coor[0], coor[1], snake.color)


def draw_apple(apple, gd):
    gd.draw_cell(apple.location[0], apple.location[1], apple.color)


def draw_bomb(bomb, gd):
    for one_location in bomb.get_location():
        gd.draw_cell(one_location[0], one_location[1], bomb.get_color())


def bomb_set_up(bomb, i, gd, taken_coors):
    bomb.set_time_state(i)
    if bomb.get_bomb_exploded():
        bomb.reset_bomb(i, taken_coors)
    # draw_bomb(bomb, gd)


def create_bomb(i, gd, bomb=None):
    if bomb is not None:
        del bomb
    bomb = Bomb(i, gd)
    return bomb
