'''
###### replay with GUI ######
def set_replay(idx):
    print("replay function called")
    if not os.path.exists(board.TEMP_LOG_PATH):
        print("No saved game states to replay.")
        return

    with open(board.TEMP_LOG_PATH, "rb") as file:
        log = pickle.load(file)

    if not log:
        print("Log is empty. Nothing to replay.")
        return

    # Save current state
    current_state = {
        'board_size': board.get_board_size(),
        'positions': board.get_positions(),
        'player_turn': board.get_player_turn(),
        'active_mills': board.get_active_mills(),
        'remaining_turns': board.get_remaining_turns(),
        'permissible_moves': board.get_permissible_moves(),
    }
    currentstuff = [log,current_state]
    return currentstuff

def replay_handler(replay_option,log,replay_state,current_state):
    print("replay_option: ", replay_option)
    print("replay_state: ", replay_state)
    print("current_state: ", current_state)
    index = replay_state
    if log is None or current_state is None:
        print("Error: Log or current state is None")
        return
    if replay_option == 0: # rewind a move button
        if index != 0:
            index -= 1
            replay_state = index
        else:
            index = 0
            replay_state = index
        state = log[index]
        board.set_positions(state['positions'])
        board.set_player_turn(state['player_turn'])
        board.set_active_mills(state['active_mills'])
        board.set_remaining_turns(state['remaining_turns'])
        return replay_state

    if replay_option == 2:
        if index != (len(log)-1): # fast forward button
            index += 1
            replay_state = index
        else:
            index = 0
            replay_state = index
        print("log length: ", len(log))
        print("index: ", index)
        state = log[index]
        board.set_positions(state['positions'])
        board.set_player_turn(state['player_turn'])
        board.set_active_mills(state['active_mills'])
        board.set_remaining_turns(state['remaining_turns'])
        return replay_state
    
    if replay_option == 3: # exit replay button
        #reset current state
        current_state = current_state
        board.set_positions(current_state['positions'])
        board.set_player_turn(current_state['player_turn'])
        board.set_active_mills(current_state['active_mills'])
        board.set_remaining_turns(current_state['remaining_turns'])

def game_loop(variable_load, computer):

    print("Initializing game window...")
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    #print("Entering main game loop...")

    running = True
    startpos = None
    endpos = None
    removepos = False
    gameover = False
    replay = False
    replay_state = 0
    play = False
    pause = False
    sleep = False
    boardImg = None
    game_mode_selection = False
    plr_turn = 1
    loop_check = False
    selections = [0,0]
    while running:
        try:
            # Event handling
            if game_mode_selection == False:
                if play == False:
                    for event in pygame.event.get():
                        print(f"Event: {event}")  # This will print out each event captured
                        if event.type == pygame.QUIT:
                            print("Quit event detected. Closing game window...")
                            running = False
                            break
                        if event.type == pygame.MOUSEBUTTONUP:
                            if replay == True:
                                for idx, rect in enumerate(replay_clickables):
                                    if rect.collidepoint(event.pos):
                                        if idx == 0: # rewind a move button
                                            replay_state = replay_handler(idx, currentstuff[0], replay_state, currentstuff[1])
                                            break
                                        if idx == 1: # play button
                                            play_loop = 0
                                            play = True
                                            play_length = len(currentstuff[0])
                                            counter = time.time()
                                            break
                                        if idx == 2: # fast forward
                                            replay_state = replay_handler(idx  , currentstuff[0], replay_state, currentstuff[1])
                                            break
                                        if idx == 3: # exit replay button
                                            #print("here exit replay")
                                            replay_handler(idx  , currentstuff[0],  replay_state, currentstuff[1])
                                            replay = False
                                            break
                            if replay == False:
                                for idx, rect in enumerate(clickables):
                                    # print("the clickables are: ", enumerate(clickables))
                                    # print("The idx is: ", idx)
                                    # print("The rect is: ", rect)
                                    # print("here1")
                                    # print("event.pos: ", event.pos)
                                    if rect.collidepoint(event.pos):
                                        if(board.get_board_size() == 9):
                                            if(idx == 24):
                                                currentstuff = set_replay(idx)
                                                replay = True
                                                break
                                            elif(idx == 25):
                                                board.save()
                                                break
                                            elif(idx == 26):
                                                board.load()
                                                break
                                            elif(idx == 27):
                                                board.new_restart_game()
                                                gameover = False
                                                break
                                        elif(board.get_board_size() == 6):
                                            if(idx == 16):
                                                currentstuff = set_replay(idx)
                                                replay = True
                                                break
                                            elif(idx == 17):
                                                board.save()
                                                break
                                            elif(idx == 18):
                                                board.load()
                                                break
                                            elif(idx == 19):
                                                board.new_restart_game()
                                                gameover = False
                                                break
                                        elif(board.get_board_size() == 3):
                                            if(idx == 9):
                                                currentstuff = set_replay(idx)
                                                replay = True
                                                break
                                            elif(idx == 10):
                                                board.save()
                                                break
                                            elif(idx == 11):
                                                board.load()
                                                break
                                            elif(idx == 12):
                                                board.new_restart_game()
                                                gameover = False
                                                break
                                        if removepos == True:
                                            if board.form_mill(idx):
                                                board.check_remove_active_mill()
                                                removepos = False
                                                board.save_current_state_to_log()
                                                if board.is_game_over() and board.get_remaining_turns() == 0 and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                    gameover = True
                                                break
                                            break
                                        if board.get_remaining_turns() != 0:
                                            #print("here2")
                                            #print(f"Clicked on position: {idx}")
                                            if board.place_piece(idx):
                                                board.check_remove_active_mill()
                                                #print("here passed place piece")
                                                if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                    removepos = True
                                                    break
                                                elif board.form_mill_GUI() and board.get_board_size() == 3:
                                                    #print("Game over!")
                                                    board.save_current_state_to_log()
                                                    #print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                    gameover = True
                                                    break
                                                board.save_current_state_to_log()
                                                #print("Form mill GUI = ", board.form_mill_GUI())
                                                #print("Board size: ", board.get_board_size())
                                                break
                                        if board.get_remaining_turns() == 0:
                                                if board.is_game_over():
                                                    #print("Game over!")
                                                    #print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                    gameover = True
                                                    break
                                                if startpos == None:
                                                    startpos = idx
                                                    #print("startpos: ", startpos)
                                                    #print("Starting position (piece selected to move): ", startpos)
                                                    break
                                                else:
                                                    if startpos == idx:
                                                        break
                                                    endpos = idx
                                                    #print("Ending position (position to move to): ", endpos)
                                                    #print("endpos: ", endpos)
                                                    if board.player_piece_count() == 3 and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                        if board.fly_piece(startpos, endpos):
                                                            board.check_remove_active_mill()
                                                            if board.form_mill_GUI():
                                                                removepos = True
                                                                startpos = None
                                                                endpos = None
                                                                break
                                                            board.save_current_state_to_log()
                                                            startpos = None
                                                            endpos = None
                                                            break
                                                        else:
                                                            startpos = None
                                                            endpos = None
                                                    else:
                                                        if board.move_piece(startpos, endpos):
                                                            print("Moved piece from ", startpos, "to ", endpos)
                                                            board.check_remove_active_mill()
                                                            if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                                removepos = True
                                                                startpos = None
                                                                endpos = None
                                                                break
                                                            elif board.form_mill_GUI() and board.get_board_size() == 3:
                                                                #print("Game over!")
                                                                board.save_current_state_to_log()
                                                                #print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                                gameover = True
                                                                break
                                                            board.save_current_state_to_log()
                                                            startpos = None
                                                            endpos = None
                                                            break
                                                        else:
                                                            startpos = None
                                                            endpos = None
                                break
                if play == True:
                    for event in pygame.event.get():
                        print(f"Event: {event}")  # This will print out each event captured
                        if event.type == pygame.QUIT:
                            print("Quit event detected. Closing game window...")
                            running = False
                            break
                            
                        print("event.type: ", event.type)
                        if event.type == pygame.MOUSEBUTTONUP:
                            for idx, rect in enumerate(play_clickables):
                                if rect.collidepoint(event.pos):
                                    if idx == 0:
                                        pause = False
                                        counter = time.time()
                                        break
                                    if idx == 1:
                                        pause = True
                                        pause_play_loop = play_loop
                                        break
                                    if idx == 2:
                                        play = False
                                        break
                    if play_loop == (play_length-1):
                        counter = time.time()
                        sleep = True
                    state = currentstuff[0][play_loop]
                    board.set_board_size(state['board_size'])
                    board.set_positions(state['positions'])
                    board.set_player_turn(state['player_turn'])
                    board.set_active_mills(state['active_mills'])
                    board.set_remaining_turns(state['remaining_turns'])
                    board.set_permissible_moves(state['permissible_moves'])
                    if pause == True:
                        play_loop = pause_play_loop
                    if pause == False:
                        play_loop = round( time.time() - counter )

                # if player == 2's turn, then call the computer's turn
                # if(board.get_player_turn() == 2 and board.get_remaining_turns() == 0):
                #     plr_turn = board.get_player_turn()
                # print("Player turn: ", plr_turn)
                if board.get_player_turn() == 2 and computer == 1:
                    if board.get_remaining_turns() != 0:
                        board.computer_place_piece()

                        if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                            removepos = True
                            remove_piece = board.computer_remove_piece()

                        if board.form_mill_GUI() and board.get_board_size() == 3:
                            print("Game over!")
                            print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                            gameover = True
                            break

                        if removepos == True:
                            print("yo we here at computer remove piece")
                            if board.form_mill(remove_piece):
                                removepos = False
                                board.check_remove_active_mill()
                                print("we gotz problemz")
                    print("we here now where's next")
                    if board.get_remaining_turns() == 0:
                        if board.player_piece_count() != 3:
                            loop_check = True
                            selections = board.computer_move_piece()
                            # # exit the program if selections is None
                            # if computer == 1 and selections != [17,16]:
                            #     print("still failing!")
                            #     gameover = True
                            #     break


                        if board.player_piece_count() == 3 and (board.get_board_size() == 6 or board.get_board_size() == 9):
                            board.computer_fly_piece() # gotta write the method for this

                        if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                            removepos = True
                            remove_piece = board.computer_remove_piece()
                            print("remove piece on: ", removepos)
                            print("and the remove piece is: ", remove_piece)

                        if board.form_mill_GUI() and board.get_board_size() == 3:
                            print("Game over!")
                            print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                            gameover = True
                            break

                        if removepos == True:
                            if board.form_mill(remove_piece):
                                removepos = False
                                board.check_remove_active_mill()
                                print("apples smell good")
                        print(f"Player Turn is: {2 if board.get_player_turn() == 2 else 1}")
                    board.save_current_state_to_log()
                

            if game_mode_selection == True:
                for event in pygame.event.get():
                    print(f"Event: {event}")  # This will print out each event captured
                    if event.type == pygame.QUIT:
                        print("Quit event detected. Closing game window...")
                        running = False
                        break
                    #print("event.type: ", event.type)
                    #print("pygame.MOUSEBUTTONUP: ", pygame.MOUSEBUTTONUP)
                    if event.type == pygame.MOUSEBUTTONUP:
                        for idx, rect in enumerate(selection_clickables):
                            if rect.collidepoint(event.pos):
                                if idx == 0:    
                                    computer = 1
                                    game_mode_selection = False
                                    break
                                if idx == 1:
                                    computer = 0
                                    game_mode_selection = False
                                    break


            #print("startpos: ", startpos)
            #print("endpos: ", endpos)
            print("removepos: ", removepos)
            print("gameover: ", gameover)
            #print("Print test: ", test)
            # print("replay: ", replay)
            # print("play: ", play)
            # print("board positions: ", board.get_positions())
            #print("board player turn (after computer turn): ", board.get_player_turn())
            #print("Loop check: ", loop_check)
            print("computer move from: ", selections[0])
            print("computer move to: ", selections[1])
            #print("board positions: ", board.get_positions())
            #     # Add more event handling logic here for other phases
            # print("remaining turns: ", board.get_remaining_turns())
            # Drawing the game state
            #print("Calling draw_board()...")

            #print("Computer: ", computer)

            if variable_load == 'True':
                board.load()
                
                # save load == false in load_game.txt
                variable_load = open("load_game.txt", "w+")
                variable_load.write('False')
                variable_load.close()

                variable_load = 'False'

                game_mode_selection = True



                print(f'This is: {variable_load}')

                # open("load_game.txt", "r")
                # variable_load = variable_load.read()
                # print(variable_load)
            
            screen.fill(WHITE)
            if(board.get_board_size() == 9):
                boardImg = boardImg9
            elif(board.get_board_size() == 6):
                boardImg = boardImg6
            elif(board.get_board_size() == 3):
                boardImg = boardImg3
            
            draw_board(screen, boardImg, board.get_positions(), coords, replay, play, game_mode_selection, startpos)
            if sleep == True:
                time.sleep(1)
                sleep = False
            
            #print("Calling draw_game_info()...")
            draw_game_info(screen, board, gameover, removepos, replay, game_mode_selection)

            # Updating the display
            #print("Updating display...")
            pygame.display.flip()

            # Frame rate
            clock.tick(60)
            
        except Exception as e:
            print(f"Error in game loop: {e}")
            running = False

    print("Exiting game...")

    pygame.quit()
    sys.exit()


game_loop(variable_load, computer)




'''
