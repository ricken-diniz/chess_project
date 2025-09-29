from utils import get_arrange,show_chessboard,show_movies,stalemate
import os

def output_message(message, multiplayer, fw):
    print(message)
    if multiplayer:
        try:
            fw.write(message)
            fw.flush()
        except Exception as e:
            print(e)
    
def input_message(message, multiplayer, fw, fr, turn):
    if not multiplayer or turn == -1:
        return input(message)
    else:
        try:
            fw.write(message)
            fw.flush()
            return fr.readline()
        except Exception as e:
            print(e)

def init_chat(multiplayer, fw, fr):
    turns = [None, 'pretas', 'brancas']
    turn = -1 
    cleaner = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    if multiplayer and fw is not None and fr is not None:
        output = cleaner + 'Partida iniciada!'
        output_message(output,True,fw)
    
    else:
        os.system('clear')
        print('Partida iniciada!')

    return turns, turn, cleaner

def init_play(multiplayer, game, turn, turns, fw, fr, cleaner):
    output = game.alert_check()
    if output:
        output_message(output,multiplayer,fw)

    output = '\nPretas: ' + " ".join(game.black_kills) + '\n'
    output += show_chessboard(game.chessboard)
    output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
    output += f'\nVez das {turns[turn]}, aguarde o oponente.'
    output_message(output,multiplayer,fw)

    if stalemate(turn, game.chessboard):
        output = f'\n\n\033[95mEmpate\033[0m por afogamento das {turns[turn]}.'
        output_message(output,multiplayer,fw)
        return 'break'

    inputmessage = '\nSelecione sua peça: '
    response = input_message(inputmessage,multiplayer,fw,fr,turn)

    if 'desisto' in response.lower():
        output = f'\n\n\033[95mDesistência das {turns[turn]}\033[0m, vitória das {turns[-turn]}'
        output_message(output,multiplayer,fw)
        return 'break'

    elif 'empate' in response.lower():
        inputmessage = f'\nO oponente sugeriu empate, aceitar? (sim/não): '
        draw_response = input_message(inputmessage,multiplayer,fw,fr,turn)

        if 'sim' in draw_response.lower():
            output = f'\n\n\033[95mEmpate\033[0m, ninguém venceu.'
            output_message(output,multiplayer,fw)
            return 'break'

        else:
            output = cleaner + 'Empate negado'
            output_message(output,multiplayer,fw)
            return 'continue'
    
    return response

def conclude_movement(multiplayer, game, turn, turns, fw, fr, cleaner, piece_arrange, i, j):
    if game.chessboard[i][j] == '.':
        output = cleaner + 'Selecione uma peça, você selecionou um espaço vazio...'
        output_message(output,multiplayer,fw)
        return

    elif game.chessboard[i][j].piece_color != turn:
        output = cleaner + f'Agora é vez das {turns[turn]}, jogue com uma peça válida!'
        output_message(output,multiplayer,fw)
        return
    
    output_message(cleaner,multiplayer,fw)
    output = game.alert_check()
    if output:
        output_message(output,multiplayer,fw)

    output = '\nPretas: ' + " ".join(game.black_kills) + '\n'
    output += show_movies(game.chessboard, game.chessboard[i][j].piece_map)
    output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
    output += f'\nVez das {turns[turn]}, aguarde o oponente.'
    output_message(output,multiplayer,fw)
    
    inputmessage = '\nSelecione o destino (ou digite C para escolher outra peça): '
    response = input_message(inputmessage,multiplayer,fw,fr,turn)

    if response.lower() == 'c':
        output_message(cleaner,multiplayer,fw)
        return

    elif (arrange := get_arrange(response)) != False:
        movement = arrange

    else:
        output = cleaner + 'Selecione uma coordenada válida!'
        output_message(output,multiplayer,fw)
        return

    if not (log := game.move_piece(piece_arrange, movement, turn)) is False:

        if log == 'End Game':
            check_mate(multiplayer, game, turn, turns, fw, cleaner)
            return 'break'

        elif log == 'Você não pode mover para essa casa, seu rei ficará em xeque!':
            output = cleaner + log
            output_message(output,multiplayer,fw)
            return
        
        output = cleaner + 'Movimentando...'
        output_message(output,multiplayer,fw)
        return 'ok'

    else:
        output = cleaner + 'Tente novamente'
        output_message(output,multiplayer,fw)
        return

def check_mate(multiplayer, game, turn, turns, fw, cleaner):
    output = cleaner
    output += '\nPretas: ' + " ".join(game.black_kills) + '\n'
    output += show_chessboard(game.chessboard)
    output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
    output += f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[turn]}\n'
    output_message(output,multiplayer,fw)

def stream_normal_game(multiplayer,game,fw=None,fr=None):
    turns, turn, cleaner = init_chat(multiplayer, fw, fr)

    while True:
        response = init_play(multiplayer, game, turn, turns, fw, fr, cleaner) 
        if response == 'break':
            break
        elif response == 'continue':
            continue

        if (arrange := get_arrange(response)) != False:
            i, j = arrange
            piece_arrange = arrange
            
        else:
            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue

        response = conclude_movement(multiplayer, game, turn, turns, fw, fr, cleaner, piece_arrange, i, j)
        if response == 'break':
            break
        if response == 'ok':
            turn = turn * -1

def stream_crazy_game(multiplayer,game,fw=None,fr=None):
    turns, turn, cleaner = init_chat(multiplayer, fw, fr)

    while True:
        response = init_play(multiplayer, game, turn, turns, fw, fr, cleaner) 
        if response == 'break':
            break
        elif response == 'continue':
            continue

        if (arrange := get_arrange(response)) != False:
            i, j = arrange
            piece_arrange = arrange
            
        else:
            captured_pieces = [None, game.black_kills, game.white_kills]

            if response[0] in captured_pieces[turn]:
                inputmessage = '\nSelecione a casa (ou digite C para cancelar): '
                arrange = input_message(inputmessage,multiplayer,fw,fr,turn)

                if arrange.lower() == 'c':
                    output_message(cleaner,multiplayer,fw)
                    continue

                elif (arrange := get_arrange(arrange)) != False:
                    i, j = arrange
                    piece_arrange = arrange

                    if (log := game.insert_piece(response[0],arrange,turn)) != False:
                        if log == 'End Game':
                            check_mate(multiplayer, game, turn, turns, fw, cleaner)
                            break

                        output = cleaner + 'Colocando peça...'
                        output_message(output,multiplayer,fw)
                        turn = turn * -1
                        continue

            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue

        response = conclude_movement(multiplayer, game, turn, turns, fw, fr, cleaner, piece_arrange, i, j)
        if response == 'break':
            break
        if response == 'ok':
            turn = turn * -1

def stream_duck_game(multiplayer,game,fw=None,fr=None):
    turns, turn, cleaner = init_chat(multiplayer, fw, fr)
    duck_position = 3,3

    while True:
        response = init_play(multiplayer, game, turn, turns, fw, fr, cleaner) 
        if response == 'break':
            break
        elif response == 'continue':
            continue

        if (arrange := get_arrange(response)) != False:
            i, j = arrange
            piece_arrange = arrange
            
        else:
            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue                

        response = conclude_movement(multiplayer, game, turn, turns, fw, fr, cleaner, piece_arrange, i, j)
        if response == 'ok' or response == 'break':

            end_game = False
            while True:
                output = game.alert_check()
                if output:
                    output_message(output,multiplayer,fw)

                output = '\nPretas: ' + " ".join(game.black_kills) + '\n'
                output += show_chessboard(game.chessboard)
                output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
                output += f'\nVez das {turns[turn]}, aguarde o oponente.'
                output_message(output,multiplayer,fw)

                inputmessage = '\nSelecione o destino do pato chato (sim, é obrigatório fazer isso): '
                arrange = input_message(inputmessage,multiplayer,fw,fr,turn)

                if (arrange := get_arrange(arrange)) != False:
                    i, j = arrange
                    movement = arrange
                else:
                    output = cleaner + 'Selecione uma coordenada válida!'
                    output_message(output,multiplayer,fw)
                    continue
                    
                if (i,j) != duck_position and game.chessboard[i][j] == '.':
                    if (log := game.move_duck(duck_position, movement, turn)) != False:

                        if log == 'Você não pode mover para essa casa, seu rei ficará em xeque!' or log == 'End Game':
                            id, jd = duck_position
                            game.chessboard[i][j],game.chessboard[id][jd] = game.chessboard[id][jd],game.chessboard[i][j]
                            end_game = True
                            suicide = True if log != 'End Game' else False
                            break

                        output = cleaner + 'Movimentando o pato...'
                        output_message(output,multiplayer,fw)
                        game.chessboard[i][j].piece_color = game.chessboard[i][j].piece_color * -1 
                        duck_position = i, j
                        break
                    else:
                        output = cleaner + 'Ocorreu algo de errado... ' + str(log)
                        output_message(output,multiplayer,fw)
                        continue
                    
                output = cleaner + 'Tente novamente'
                output_message(output,multiplayer,fw)
                continue
            
            if end_game:
                turn = -turn if suicide else turn
                check_mate(multiplayer, game, turn, turns, fw, cleaner)
                output = 'O pato é traiçoeiro! Ele sempre tem que ser movido e pode deixar seu rei na mão!\nPor isso, você perdeu o jogo!'
                output_message(output,multiplayer,fw)
                return 'break'

            turn = turn * -1
