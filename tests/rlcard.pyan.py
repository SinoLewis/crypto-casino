# from rlcard.games.limitholdem.game import LimitHoldemGame as Game
# from rlcard.utils import print_card
# from pprint import pprint

# game = Game()

# # test raise
# def testRaise():
#     game.init_game()
#     init_raised = game.round.have_raised
#     print('GAME BEFOUR: ', init_raised)
#     game.step('raise')
#     step_raised = game.round.have_raised
#     print('GAME AFTER: ', step_raised)
    
#     return game

# def get_hands(self, player_hands, public_card):
#     hands = []
#     for hand in player_hands:
#         hands.append(hand + public_card)
#     return hands        

# game = testRaise()

# print("GAME TYPE: ", type(game.public_cards))
# print("GAME: ", dir(game.public_cards))

# hands = get_hands(game.players[0].hand, game.public_cards())
# print("GAME HANDS: ", hands)
# print_card(hands)

# import pyan

# callgraph = pyan.create_callgraph('../examples/human/limit_holdem_human.py', format='html')

# with open('tests/limit_holdem_human.html', 'w') as f:
#     f.write(callgraph)

import pyan
from IPython.display import HTML
HTML(pyan.create_callgraph(filenames="../examples/human/limit_holdem_human.py", format="html"))