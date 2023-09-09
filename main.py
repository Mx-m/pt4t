import random
import time
import faulthandler
import numpy as np
faulthandler.enable()
import sys
import select


def get_user_input_with_timeout(prompt, timeout):
    print(prompt)

    user_input = None
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)

    if rlist:
        user_input = sys.stdin.readline().strip()
    else:
        print("Timeout reached. No input received.")

    return user_input


def end_get_user_input_with_timeout(prompt, timeout, user_moving):
    print(prompt)
    user_input = None
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)

    if rlist:
        user_moving = True
        user_input = sys.stdin.readline().strip()
    else:
        print("Timeout reached. No input received.")
        user_moving = False

    return user_input, user_moving


def init_tetrominos():
    b = '[]'
    x = '  '
    i = [[[b, b, b, b]], [[b],
                          [b],
                          [b],
                          [b]]]
    o = [[[b, b],
         [b, b]]]
    t = [[[x, b, x],
          [b, b, b]],
         [[b, x],
          [b, b],
          [b, x]],
         [[b, b, b],
          [x, b, x]],
         [[x, b],
          [b, b],
          [x, b]]]
    j = [[[x, b],
          [x, b],
          [b, b]],
         [[b, x, x],
          [b, b, b]],
         [[b, b],
          [b, x],
          [b, x]],
         [[b, b, b],
          [x, x, b]]]
    l = [[[b, x],
          [b, x],
          [b, b]],
         [[b, b, b],
          [b, x, x]],
         [[b, b],
          [x, b],
          [x, b]],
         [[x, x, b],
          [b, b, b]]]
    s = [[[x, b, b],
          [b, b, x]],
         [[b, x],
          [b, b],
          [x, b]]]
    z = [[[b, b, x],
          [x, b, b]],
         [[x, b],
          [b, b],
          [b, x]]]
    return {'i': i, 'o': o, 't': t, 'j': j, 'l': l, 's': s, 'z': z}


def init_game():
    # game matrix
    b = '{}'
    x = '  '
    gm = [[b, b, b, b, b, b, b, b, b, b, b, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, x, x, x, x, x, x, x, x, x, x, b],
          [b, b, b, b, b, b, b, b, b, b, b, b]]
    return gm


def rotate_tetromino(t_dict, state):
    n = len(t_dict) - 1
    if n == state:
        rotated_matrix = t_dict[0]
        state = 0
        return rotated_matrix, state
    else:
        rotated_matrix = t_dict[state + 1]
    state = state + 1
    return rotated_matrix, state


def reverse_tetromino(t_dict, state):
    n = len(t_dict) - 1
    if state == 0:
        rotated_matrix = t_dict[n]
        state = n
        return rotated_matrix, state
    else:
        rotated_matrix = t_dict[state - 1]
    state = state - 1
    return rotated_matrix, state


def start_game(gm, tetros):
    global game_fail
    global score
    user_moving = True
    difficulty = 75
    if 'score' in globals():
        game_speed = 1 - (score / difficulty)
    else:
        game_speed = 1
    game_start = True
    tetro_list = ['i', 'o', 't', 'j', 'l', 's', 'z']
    n = random.randint(0, 6)
    st = random.randint(0, len(tetros[tetro_list[n]]) - 1)  # randomize later
    t_matrix = tetros[tetro_list[n]][st]  # create initial block
    y = 1
    x = random.randint(1,11-len(t_matrix[0]))
    for i in range(len(t_matrix)):  # fill out game board initially
        for j in range(len(t_matrix[i])):
            if t_matrix[i][j] != '  ':
                gm[y + i][x + j] = t_matrix[i][j]
    refresh_game(gm)
    while game_start and not game_fail:
        empty = True
        turn_good = True
        empty_left = True
        empty_right = True
        end_empty = True
        end_empty_left = True
        end_empty_right = True
        fast = False
        while empty:
            # Check for empty space underneath
            for row in range(len(t_matrix)):
                for col in range(0, len(t_matrix[0])):
                    if t_matrix[row][col] != '  ':
                        # Calculate the position of the space directly below the current block
                        row_below = y + row + 1
                        col_below = x + col
                        if gm[row_below][col_below] != '  ':
                            if gm[row_below][col_below] == '{}':
                                empty = False
                                break
                            elif row != len(t_matrix)-1 and t_matrix[row + 1][col] == '[]':
                                empty = True
                            elif gm[row_below][col_below] == '[]':
                                empty = False
                                break
                if not empty:
                    break
            # Check for empty space to the left
            for row in range(len(t_matrix)):
                for col in range(len(t_matrix[0])):
                    if t_matrix[row][col] != '  ':
                        if x - 1 >= 1 and (gm[y + row][x + col - 1] == '  ' or (col - 1 >= 0 and t_matrix[row][col - 1] == '[]')):
                            empty_left = True
                        else:
                            empty_left = False
                            break
                if not empty_left:
                    break
            # Check for empty space to the right
            for row in range(len(t_matrix)):
                for col in range(len(t_matrix[0]) - 1, -1, -1):
                    if t_matrix[row][col] != '  ':
                        if x + col + 1 < len(gm[0])-1 and (
                                gm[y + row][x + col + 1] == '  ' or (col + 1 <= len(t_matrix[0])-1 and t_matrix[row][col + 1] == '[]')):
                            empty_right = True
                        else:
                            empty_right = False
                            break
                if not empty_right:
                    break
            if not empty:
                continue
            # clear tetromino
            for i in range(len(t_matrix)):
                for j in range(len(t_matrix[i])):
                    if t_matrix[i][j] != '  ':
                        gm[y + i][x + j] = "  "
            # advance down
            y = y + 1
            # reprint tetromino
            for i in range(len(t_matrix)):
                for j in range(len(t_matrix[i])):
                    if t_matrix[i][j] != '  ':
                        gm[y + i][x + j] = t_matrix[i][j]
            # Check for user input to rotate the tetromino
            if 'score' in globals():
                game_speed = 1-(score/difficulty)
            elif fast:
                game_speed = 0.5
                print('fast')
                if empty:
                    continue
                elif not empty:
                    fast = False
                    continue
                else:
                    fast = False
                    continue
            else:
                game_speed = 1
            user_input = get_user_input_with_timeout("move: ", game_speed)
            # if user wants to turn
            if user_input == 'w' and (y + len(t_matrix)) < (len(gm) - 1) and x + len(t_matrix)-1 < len(gm[0])-1:
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                tetro_and_state = rotate_tetromino(tetros[tetro_list[n]], st)
                t_matrix = tetro_and_state[0]
                st = tetro_and_state[1]
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            if gm[y+i][x+j] != '  ':
                                turn_good = False
                                tetro_and_state = reverse_tetromino(tetros[tetro_list[n]], st)
                                t_matrix = tetro_and_state[0]
                                st = tetro_and_state[1]
                                break
                    if not turn_good:
                        break
            # if user wants to move left
            elif user_input == 'a' and x > 1 and empty_left:
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                x = x - 1
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            if gm[y+i][x+j] != '  ':
                                empty_left = False
                                x = x + 1
                                break
                    if not empty_left:
                        break
            # if user wants to move right
            elif user_input == 'd' and x + len(t_matrix[0]) < len(gm[0]) - 1 and empty_right:
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                x = x + 1
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            if gm[y+i][x+j] != '  ':
                                empty_left = False
                                x = x - 1
                                break
                    if not empty_left:
                        break
            # if user wants to SLAM block down
            elif user_input == 'v':
                fast = True
            # if user wants to quit
            elif user_input == 'q':
                game_fail = True
                break
                # a game by clouds
            # Update the game matrix with the new tetromino position
            for i in range(len(t_matrix)):
                for j in range(len(t_matrix[i])):
                    if t_matrix[i][j] != '  ':
                        gm[y + i][x + j] = t_matrix[i][j]
            refresh_game(gm)
        if game_fail:
            break
        t_end = time.time() + game_speed
        while user_moving and time.time() < t_end:
            user_input_list = end_get_user_input_with_timeout("move: ", game_speed, user_moving)
            user_input = user_input_list[0]
            user_moving = user_input_list[1]
            # Check for empty space to the left
            for row in range(len(t_matrix)):
                for col in range(len(t_matrix[0])):
                    if t_matrix[row][col] != '  ':
                        if x - 1 >= 1 and (
                                gm[y + row][x + col - 1] == '  ' or (col - 1 >= 0 and t_matrix[row][col - 1] == '[]')):
                            end_empty_left = True
                        else:
                            end_empty_left = False
                            break
                if not end_empty_left:
                    break
            # Check for empty space to the right
            for row in range(len(t_matrix)):
                for col in range(len(t_matrix[0]) - 1, -1, -1):
                    if t_matrix[row][col] != '  ':
                        if x + col + 1 < len(gm[0]) - 1 and (
                                gm[y + row][x + col + 1] == '  ' or (
                                col + 1 <= len(t_matrix[0]) - 1 and t_matrix[row][col + 1] == '[]')):
                            end_empty_right = True
                        else:
                            end_empty_right = False
                            break
                if not end_empty_right:
                    break
            # if user wants to turn
            if user_input == 'w' and (y + len(t_matrix)) < (len(gm) - 1) and x + len(t_matrix) - 1 < len(gm[0]) - 1:
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                tetro_and_state = rotate_tetromino(tetros[tetro_list[n]], st)
                t_matrix = tetro_and_state[0]
                st = tetro_and_state[1]
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            if gm[y + i][x + j] != '  ':
                                turn_good = False
                                tetro_and_state = reverse_tetromino(tetros[tetro_list[n]], st)
                                t_matrix = tetro_and_state[0]
                                st = tetro_and_state[1]
                                break
                    if not turn_good:
                        break
            # if user wants to move left
            elif user_input == 'a' and x > 1 and end_empty_left:
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                x = x - 1
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            if gm[y + i][x + j] != '  ':
                                empty_left = False
                                x = x + 1
                                break
                    if not empty_left:
                        break
            # if user wants to move right
            elif user_input == 'd' and x + len(t_matrix[0]) < len(gm[0]) - 1 and end_empty_right:
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                x = x + 1
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            if gm[y + i][x + j] != '  ':
                                empty_left = False
                                x = x - 1
                                break
                    if not empty_left:
                        break
            # if user wants to quit
            elif user_input == 'q':
                game_fail = True
                break
                # a game by clouds
            # Update the game matrix with the new tetromino position
            for i in range(len(t_matrix)):
                for j in range(len(t_matrix[i])):
                    if t_matrix[i][j] != '  ':
                        gm[y + i][x + j] = t_matrix[i][j]
            # Check for empty space underneath
            for row in range(len(t_matrix)):
                for col in range(0, len(t_matrix[0])):
                    if t_matrix[row][col] != '  ':
                        # Calculate the position of the space directly below the current block
                        row_below = y + row + 1
                        col_below = x + col
                        if gm[row_below][col_below] != '  ':
                            if gm[row_below][col_below] == '{}':
                                end_empty = False
                                break
                            elif row != len(t_matrix) - 1 and t_matrix[row + 1][col] == '[]':
                                end_empty = True
                            elif gm[row_below][col_below] == '[]':
                                end_empty = False
                                break
                if not end_empty:
                    break
            if end_empty:
                # clear the old tetromino
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = "  "
                # move down
                y = y + 1
                # Update the game matrix with the new tetromino position
                for i in range(len(t_matrix)):
                    for j in range(len(t_matrix[i])):
                        if t_matrix[i][j] != '  ':
                            gm[y + i][x + j] = t_matrix[i][j]
            refresh_game(gm)
        print("block down")
        game_start = False
    if y == 1:
        game_fail = True
    br = '{}'
    b = '[]'
    x = '  '
    # check for clears
    for j in range(1, 21):
        if gm[j] == [br, b, b, b, b, b, b, b, b, b, b, br]:
            score = score + 1
            gm[j] = [br, x, x, x, x, x, x, x, x, x, x, br]
            i = j
            while i > 1:
                gm[i] = gm[i-1]
                gm[i - 1] = [br, x, x, x, x, x, x, x, x, x, x, br]
                i = i - 1
    return game_speed

def refresh_game(gm):
    gm_display = np.array(gm)
    for line in gm_display:
        print('  '.join(map(str, line)))


if __name__ == '__main__':
    game_fail = False
    tetros = init_tetrominos()
    gm = init_game()
    start_game(gm, tetros)
    score = 0
    game_speed = 1
    while game_fail == False:
        game_speed = start_game(gm, tetros)
    refresh_game(gm)
    print('\n')
    print('{}{}.game over.{}{}')
    print('score: ' + str(score*(100*(2-game_speed))))
