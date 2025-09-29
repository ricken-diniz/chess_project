import os
from gamemods.chess import Chess
from gamemods.atomic_chess import AtomicChess
from gamemods.crazy_chess import CrazyChess
from gamemods.duck_chess import DuckChess
from streams import stream_normal_game, stream_crazy_game, stream_duck_game

def main():
    os.system('clear')
    initial_alert = '''
    XADREZ

    Como jogar?

    Para jogar, você informa apenas coordenadas, exemplo "A8", "g7".
    Primeiro você seleciona uma peça, depois você orienta qual casa quer ir.
    Também há mensagens de controle como "desisto" e "empate" para quando um
    oponente quiser desistir ou sugerir um empate. Aparecerá mensagens 
    informando as peças capturadas por cada time e mensagens de logs!

    Se for jogar localmente, faça sua jogada e passe a vez, aparecerá uma
    mensagem instruindo de quem é a vez.

    Se for jogar no Multiplayer, o outro jogador deve conectar-se a mesma
    máquina (ou VM), mas pode estar em outro usuário, ele deverá ir ao
    diretório temporário com o comando:

    `\033[94mcd /tmp\033[0m`

    ... e abrir 2 arquivos,
    *fifow* para ver em tempo real as atualizações do tabuleiro, aconselho
    usar tmux para dividir a tela e deixar mais espaço para esta sessão,
    fora isso, basta executar o comando:

    `\033[94mcat fifow\033[0m`
    
    e o arquivo *fifor*, para dar os comandos de jogadas em tempo real, para
    este, precisa de pouco espaço de tela, basta o comando:

    `\033[94mtee -a fifor\033[0m`

    ALERTA: Se for jogar multiplayer, por questões de permissões, é preferível
    que se use o prefixo \033[94msudo\033[0m, para conceder permissões de super-
    usuário e evitar problemas de permissões, caso contrário, talvez seja neces-
    sário configurar manualmente as permissões de criação dos arquivos.
    '''

    print(initial_alert)

    while True:
        connection = input('(L)ocal ou (M)ultiplayer? ')
        if connection.lower() in ['l','m']:
            break
        elif connection == 'exit':
            print('\nAté mais!')
            return
        else:
            print('Digite uma resposta válida (`exit` para sair).')

    while True:
        os.system('clear')
        gamemod = input('Qual modo de jogo?\n1. Normal Game\n2. Atomic Chess\n3. Crazy Chess\n4. Duck Chess\n\nR: ')

        if gamemod == '1':
            print('\nModo de jogo padrão com as regras tradicionais do xadrez.\n')
            confirm = input('Confirmar? (Yes/No): ')
            if confirm.lower() in 'yes':
                game = Chess()
                stream_game = stream_normal_game
                break

        elif gamemod == '2':
            print('\nXadrez atômico, quando uma peça for capturada, tudo ao redor vai embora, exceto o rei aliado.\nNote que você pode eliminar o rei inimigo, e isso será cheque mate! Uma dica? \nO cavalo é melhor do que parece...\n')
            confirm = input('Confirmar? (Yes/No): ')
            if confirm.lower() in 'yes':
                game = AtomicChess()
                stream_game = stream_normal_game
                break

        elif gamemod == '3':
            print('\nXadrez maluco, você pode realocar uma peça capturada para o seu exército, ao invés de fazer\num movimento padrão de jogo. Para isso, basta digitar a letra da peça capturada em sua jogada. \nNote que há diferenciação de maiúsculas e minúsculas, exemplo: "p" é um peão preto.\n')
            confirm = input('Confirmar? (Yes/No): ')
            if confirm.lower() in 'yes':
                game = CrazyChess()
                stream_game = stream_crazy_game
                break

        elif gamemod == '4':
            print('\nNo Xadrez do Pato você passará muita raiva, o conceito desse modo é que você sempre é obrigado a mover um "pato chato", e o mover pode trazer o seu fim!\nPreste atenção nas jogadas, pois nesse modo você tem a capacidade de atirar no próprio pé.\n')
            confirm = input('Confirmar? (Yes/No): ')
            if confirm.lower() in 'yes':
                game = DuckChess()
                stream_game = stream_duck_game
                break

        elif gamemod == 'exit':
            print('\nAté mais!')
            return
        
        else:
            print('Digite uma resposta válida (`exit` para sair).')


    if connection.lower() == 'm':
        if os.path.exists('/tmp/fifow'):
            os.remove('/tmp/fifow')
        if os.path.exists('/tmp/fifor'):
            os.remove('/tmp/fifor')
        os.mkfifo('/tmp/fifow')
        os.mkfifo('/tmp/fifor')
        os.system('chmod a+rwx /tmp/fifow')
        os.system('chmod a+rwx /tmp/fifor')
        os.system('clear')
        print('Esperando o oponente conectar...')
        fr = open('/tmp/fifor')
        with open('/tmp/fifow', 'w') as fw:
            stream_game(True,game,fw,fr)
    else:
        stream_game(False,game,None,None)

        


if __name__ == '__main__':
    main()