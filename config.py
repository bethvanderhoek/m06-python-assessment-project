# Locations
words_list_location = 'words-alpha.txt'
wheel_data_location = 'wheel-data.txt'
# (unsure if will use) roundstatusloc = 'roundstatus.txt'
final_prize_options_location = 'final-prize.txt'

# Variables
vowel_cost = int(250)
round_number = 1
play_again = 'Yes'
chosen_word = ''
hidden_word = '' 
new_line = '\n'
turn_number = 0
end_round = False


# Lists
vowels = ['a', 'e', 'i', 'o', 'u']
letters_already_guessed = []
words_already_chosen = []

# Created lists from files (open, read, split into list, close)
f = open(words_list_location)
words = f.read()
words_list = words.split('\n')
f.close

wheel = open(wheel_data_location)
wedges = wheel.read()
wheel_wedges = wedges.split('\n')
wheel.close

prize = open(final_prize_options_location)
prizes = prize.read()
prize_options = prizes.split('\n')
prize.close

# Dictionaries
players_information = {'Player A':{'Name': '', 'Round Earnings': 0, 'Total Earnings': 0}, 
                       'Player B':{'Name': '', 'Round Earnings': 0, 'Total Earnings': 0},
                       'Player C':{'Name': '', 'Round Earnings': 0, 'Total Earnings': 0}}
turn_options = ['1: Spin the wheel', '2: Buy a vowel for $250 (only if you have the money!)', '3: Guess the word']
player_order_options = {1: ['Player A', 'Player B', 'Player C'], 2: ['Player B', 'Player C', 'Player A'], 3: ['Player C', 'Player A', 'Player B']}


