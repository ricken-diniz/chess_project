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

def stream_normal_game(multiplayer,game,fw=None,fr=None):
    turns = [None, 'pretas', 'brancas']
    turn = -1 
    cleaner = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    if multiplayer and fw is not None and fr is not None:
        output = cleaner + 'Partida iniciada!'
        output_message(output,True,fw)
    
    else:
        os.system('clear')
        print('Partida iniciada!')

    while True:
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
            break

        inputmessage = '\nSelecione sua peça: '
        response = input_message(inputmessage,multiplayer,fw,fr,turn)

        if 'desisto' in response.lower():
            output = f'\n\n\033[95mDesistência das {turns[turn]}\033[0m, vitória das {turns[-turn]}'
            output_message(output,multiplayer,fw)
            break

        elif 'empate' in response.lower():
            inputmessage = f'\nO oponente sugeriu empate, aceitar? (sim/não): '
            draw_response = input_message(inputmessage,multiplayer,fw,fr,turn)

            if 'sim' in draw_response.lower():
                output = f'\n\n\033[95mEmpate\033[0m, ninguém venceu.'
                output_message(output,multiplayer,fw)
                break

            else:
                output = cleaner + 'Empate negado'
                output_message(output,multiplayer,fw)
                continue

        if (arrange := get_arrange(response)) != False:
            i, j = arrange
            piece_arrange = arrange
            
        else:
            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue

        if game.chessboard[i][j] == '.':
            output = cleaner + 'Selecione uma peça, você selecionou um espaço vazio...'
            output_message(output,multiplayer,fw)
            continue

        elif game.chessboard[i][j].piece_color != turn:
            output = cleaner + f'Agora é vez das {turns[turn]}, jogue com uma peça válida!'
            output_message(output,multiplayer,fw)
            continue
        
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
            continue

        if (arrange := get_arrange(response)) != False:
            movement = arrange

        else:
            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue

        if not (log := game.move_piece(piece_arrange, movement, turn)) is False:

            if log == 'End Game':
                output = cleaner
                output += '\nPretas: ' + " ".join(game.black_kills) + '\n'
                output += show_chessboard(game.chessboard)
                output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
                output += f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[turn]}\n'
                output_message(output,multiplayer,fw)
                break

            elif log == 'Você não pode mover para essa casa, seu rei ficará em xeque!':
                output = cleaner + log + '\n'
                output_message(output,multiplayer,fw)
                continue
            
            output = cleaner + 'Movimentando...\n'
            output_message(output,multiplayer,fw)
            turn = turn * -1

        else:
            output = cleaner + 'Tente novamente\n'
            output_message(output,multiplayer,fw)

def stream_crazy_game(multiplayer,game,fw=None,fr=None):
    turns = [None, 'pretas', 'brancas']
    turn = -1 
    cleaner = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    if multiplayer and fw is not None and fr is not None:
        output = cleaner + 'Partida iniciada!'
        output_message(output,True,fw)
    
    else:
        os.system('clear')
        print('Partida iniciada!')

    while True:
        captured_pieces = [None, game.black_kills, game.white_kills]

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
            break

        inputmessage = '\nSelecione sua peça: '
        response = input_message(inputmessage,multiplayer,fw,fr,turn)

        if 'desisto' in response.lower():
            output = f'\n\n\033[95mDesistência das {turns[turn]}\033[0m, vitória das {turns[-turn]}'
            output_message(output,multiplayer,fw)
            break

        elif 'empate' in response.lower():
            inputmessage = f'\nO oponente sugeriu empate, aceitar? (sim/não): '
            draw_response = input_message(inputmessage,multiplayer,fw,fr,turn)

            if 'sim' in draw_response.lower():
                output = f'\n\n\033[95mEmpate\033[0m, ninguém venceu.'
                output_message(output,multiplayer,fw)
                break

            else:
                output = cleaner + 'Empate negado'
                output_message(output,multiplayer,fw)
                continue

        if (arrange := get_arrange(response)) != False:
            i, j = arrange
            piece_arrange = arrange
            
        else:

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
                            output = cleaner
                            output += '\nPretas: ' + " ".join(game.black_kills) + '\n'
                            output += show_chessboard(game.chessboard)
                            output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
                            output += f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[turn]}'
                            output_message(output,multiplayer,fw)
                            break

                        output = cleaner + 'Colocando peça...'
                        output_message(output,multiplayer,fw)
                        turn = turn * -1
                        continue

            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue

        if game.chessboard[i][j] == '.':
            output = cleaner + 'Selecione uma peça, você selecionou um espaço vazio...'
            output_message(output,multiplayer,fw)
            continue

        elif game.chessboard[i][j].piece_color != turn:
            output = cleaner + f'Agora é vez das {turns[turn]}, jogue com uma peça válida!'
            output_message(output,multiplayer,fw)
            continue
        
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
            continue

        if (arrange := get_arrange(response)) != False:
            movement = arrange

        else:
            output = cleaner + 'Selecione uma coordenada válida!'
            output_message(output,multiplayer,fw)
            continue

        if not (log := game.move_piece(piece_arrange, movement, turn)) is False:

            if log == 'End Game':
                output = cleaner
                output += '\nPretas: ' + " ".join(game.black_kills) + '\n'
                output += show_chessboard(game.chessboard)
                output += '\nBrancas: ' + " ".join(game.white_kills) + '\n'
                output += f'\n\n\033[95mXeque mate\033[0m, vitória das {turns[turn]}'
                output_message(output,multiplayer,fw)
                break

            elif log == 'Você não pode mover para essa casa, seu rei ficará em xeque!':
                output = cleaner + log
                output_message(output,multiplayer,fw)
                continue
            
            output = cleaner + 'Movimentando...'
            output_message(output,multiplayer,fw)
            turn = turn * -1

        else:
            output = cleaner + 'Tente novamente'
            output_message(output,multiplayer,fw)
 