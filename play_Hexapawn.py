from dlgo import minimax
from dlgo import hexapawn

import textwrap

from six.moves import input


def print_board(board):
    print('    C1   C2   C3')
    for row in (1, 2, 3):
        pieces = []
        for col in (1, 2, 3):
            minion = board.get(hexapawn.Point(row, col))
            pieces.append(minion or '  ')
        print('R%d  %s' % (row, ' | '.join(pieces)))
    print()


def main():
    game = hexapawn.GameState.new_game()

    human_player = hexapawn.Player.x

    bot = minimax.MinimaxAgent()
    print("\n=====================================================================")
    print("===========================HEXAPAWN==================================")
    print("=====================================================================\n")
    print(textwrap.fill(
            'HEXAPAWN IS PLAYED WITH CHESS PAWNS ON A 3 BY 3 BOARD. THE '
            'PAWNS ARE MOVED AS IN CHESS - ONE SPACE FORWARD TO AN EMPTY '
            'SPACE OR ONE SPACE FORWARD AND DIAGONALLY TO CAPTURE AN '
            'OPPOSING MAN. ON THE BOARD, YOUR PAWNS ARE \'X\', THE '
            'COMPUTER\'S PAWNS ARE \'0. TO ENTER A MOVE, TYPE THE LEGAL' 
            ' MOVE FROM THE OPTIONS PROVIDED BELOW AS A HINT. GOOD LUCK!'), '\n'
        )
    print("=====================================================================\n")
    while not game.is_over():
       
        try:
            if game.next_player == human_player:

                print_board(game.board)
                print("Your Turn - Agent")
                print("===================")
                moves = game.legal_moves()
                print('\n'.join('{} {}'.format(idx, m) for idx, m in enumerate(moves)))
                human_select = int(input('-- ').strip())
                move = moves[human_select]
            else:
                print("===================")
                print_board(game.board)
                print("AI's turn")
                print("===================")
                move = bot.select_move(game)
        except:
            print('\n====================================')
            print('Invalid Selection.. Please try again')
            print('====================================\n')
            continue
        game = game.apply_move(move)

    print_board(game.board)
    winner = game.winner()
    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()