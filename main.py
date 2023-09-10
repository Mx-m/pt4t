import random
import time
import faulthandler
import numpy as np
from playsound import playsound
import threading
faulthandler.enable()
import pyaudio
import wave
import sys
import select


def title_screen():
    print('\n\n')
    tm = [['[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '      [][][]      ',
           '[][][][][][][][][]'],
          ['[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '      [][][]      ',
           '[][][][][][][][][]'],
          ['      [][][]      ', '[][][]            ', '      [][][]      ', '[][][]      [][][]', '      [][][]      ',
           '[][][]            '],
          ['      [][][]      ', '[][][]            ', '      [][][]      ', '[][][]      [][][]', '      [][][]      ',
           '[][][]            '],
          ['      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH'],
          ['      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH'],
          ['      HHHHHH      ', 'HHHHHH            ', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           '            HHHHHH'],
          ['      HHHHHH      ', 'HHHHHH            ', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           '            HHHHHH'],
          ['      HHHHHH      ', 'HHHHHHHHHHHHHHHHHH', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH'],
          ['      HHHHHH      ', 'HHHHHHHHHHHHHHHHHH', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH']]
    refresh_game(tm)
    print('')
    print('by: clouds')
    print('\n')
    print('                                                PRESS ENTER TO START')
    print('\n\n')
    print(
        "Tetris ® & © 1985~2023 Tetris Holding.\nTetris logos, Tetris theme song and Tetriminos are trademarks of Tetris Holding.\nThe Tetris trade dress is owned by Tetris Holding. Licensed to The Tetris Company.\nTetris Game Design by Alexey Pajitnov.\nTetris Logo Design by Roger Dean.\nAll Rights Reserved.\nAll other trademarks are the property of their respective owners.")
    wf = wave.open('title.wav', 'rb')
    p = pyaudio.PyAudio()
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
    stream.start_stream()
    any_key = input('')
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    return True


def end_screen(score):
    print('a game by clouds.')
    print('\n\n')
    print('{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}')
    print('\n\n')
    tm = [['[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '      [][][]      ',
           '[][][][][][][][][]'],
          ['[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '[][][][][][][][][]', '      [][][]      ',
           '[][][][][][][][][]'],
          ['      [][][]      ', '[][][]            ', '      [][][]      ', '[][][]      [][][]', '      [][][]      ',
           '[][][]            '],
          ['      [][][]      ', '[][][]            ', '      [][][]      ', '[][][]      [][][]', '      [][][]      ',
           '[][][]            '],
          ['      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH'],
          ['      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ', 'HHHHHHHHHHHH      ', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH'],
          ['      HHHHHH      ', 'HHHHHH            ', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           '            HHHHHH'],
          ['      HHHHHH      ', 'HHHHHH            ', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           '            HHHHHH'],
          ['      HHHHHH      ', 'HHHHHHHHHHHHHHHHHH', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH'],
          ['      HHHHHH      ', 'HHHHHHHHHHHHHHHHHH', '      HHHHHH      ', 'HHHHHH      HHHHHH', '      HHHHHH      ',
           'HHHHHHHHHHHHHHHHHH']]
    refresh_game(tm)
    print('')
    print('by: clouds')
    print('\n')
    print('                                                   {}.GAME OVER.{}')
    print('                                             THANK YOU FOR PLAYING TETRIS')
    print('                                                 your score was: ' + str(score))
    print('\n')
    playsound('game_over.mp3')


def get_user_input_with_timeout(prompt, timeout):
    print(prompt)

    user_input = None
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)

    if rlist:
        user_input = sys.stdin.readline().strip()

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


def start_game(gm, tetros, something_stored, stored, count_stored, temp):
    global game_fail
    global score
    something_stored_signal = False
    user_moving = True
    difficulty = 75
    if 'score' in globals():
        game_speed = 1 - (score / difficulty)
    else:
        game_speed = 1
    game_start = True
    tetro_list = ['i', 'o', 't', 'j', 'l', 's', 'z']
    if count_stored == 1:
        n = temp[0]
        st = temp[1]
    else:
        n = random.randint(0, 6)
        st = random.randint(0, len(tetros[tetro_list[n]]) - 1)  # randomize later
    t_matrix = tetros[tetro_list[n]][st]  # create initial block
    y = 1
    x = random.randint(1, 11 - len(t_matrix[0]))
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
        fast_empty = True
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
                            elif row != len(t_matrix) - 1 and t_matrix[row + 1][col] == '[]':
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
                        if x - 1 >= 1 and (
                                gm[y + row][x + col - 1] == '  ' or (col - 1 >= 0 and t_matrix[row][col - 1] == '[]')):
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
                        if x + col + 1 < len(gm[0]) - 1 and (
                                gm[y + row][x + col + 1] == '  ' or (
                                col + 1 <= len(t_matrix[0]) - 1 and t_matrix[row][col + 1] == '[]')):
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
                game_speed = 1 - (score / difficulty)
            else:
                game_speed = 1
            user_input = get_user_input_with_timeout("move: ", game_speed)
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
            elif user_input == 'a' and x > 1 and empty_left:
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
            elif user_input == 'd' and x + len(t_matrix[0]) < len(gm[0]) - 1 and empty_right:
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
            # if user wants to SLAM block down
            elif user_input == 's':
                while fast_empty:
                    # Check for empty space underneath
                    for row in range(len(t_matrix)):
                        for col in range(0, len(t_matrix[0])):
                            if t_matrix[row][col] != '  ':
                                # Calculate the position of the space directly below the current block
                                row_below = y + row + 1
                                col_below = x + col
                                if gm[row_below][col_below] != '  ':
                                    if gm[row_below][col_below] == '{}':
                                        fast_empty = False
                                        break
                                    elif row != len(t_matrix) - 1 and t_matrix[row + 1][col] == '[]':
                                        fast_empty = True
                                    elif gm[row_below][col_below] == '[]':
                                        fast_empty = False
                                        break
                        if not fast_empty:
                            break
                    if fast_empty:
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
            # store block
            elif user_input == 'r':
                if count_stored == 0:
                    if something_stored:
                        for i in range(len(t_matrix)):
                            for j in range(len(t_matrix[i])):
                                if t_matrix[i][j] != '  ':
                                    gm[y + i][x + j] = "  "
                        temp = stored
                        stored = [n, st]
                        something_stored_signal = True
                        count_stored = 1
                    else:
                        for i in range(len(t_matrix)):
                            for j in range(len(t_matrix[i])):
                                if t_matrix[i][j] != '  ':
                                    gm[y + i][x + j] = "  "
                        stored = [n, st]
                        something_stored = True
                        something_stored_signal = True
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
            refresh_game(gm)
        if something_stored_signal:
            break
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
        while end_empty:
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
        count_stored = 0
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
                gm[i] = gm[i - 1]
                gm[i - 1] = [br, x, x, x, x, x, x, x, x, x, x, br]
                i = i - 1
    return game_speed, something_stored, stored, count_stored, temp


def refresh_game(gm):
    gm_display = np.array(gm)
    for line in gm_display:
        print('  '.join(map(str, line)))

def play_audio():
    global stop_stream
    stop_stream = False
    # Define the WAV file to play
    file_path = "tetris.wav"
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    # Open the WAV file
    wf = wave.open(file_path, 'rb')
    # Get the audio stream parameters
    channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    frame_rate = wf.getframerate()
    # Create an audio stream
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)
    while not stop_stream:
        data = wf.readframes(1024)  # Read audio data in chunks
        if not data:
            wf.rewind()  # Reset the file position to the beginning when it reaches the end
            continue  # Restart the audio if it has reached the end
        stream.write(data)  # Play the audio data
    if stop_stream:
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()

if __name__ == '__main__':
    Return = title_screen()
    if Return:
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()
        game_fail = False
        count_stored = 0
        global something_stored
        something_stored = False
        global stored
        temp = []
        stored = ''
        tetros = init_tetrominos()
        gm = init_game()
        score = 0
        game_speed = 1
        while game_fail == False:
            game_data = start_game(gm, tetros, something_stored, stored, count_stored, temp)
            game_speed = game_data[0]
            something_stored = game_data[1]
            stored = game_data[2]
            count_stored = game_data[3]
            temp = game_data[4]
        stop_stream = True
        audio_thread.join()
        refresh_game(gm)
        game = False
        total_score = int(score * (100 * (2 - game_speed)))
        end_screen(total_score)
