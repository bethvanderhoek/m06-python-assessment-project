#                                  ~Python Basics Assessment Project: Wheel of Fortune~

#import packages and config 
import random
import config 
from inputimeout import inputimeout, TimeoutOccurred 

#import variables from config
from config import vowel_cost
from config import chosen_word
from config import hidden_word
from config import new_line
from config import turn_number 
from config import round_number
from config import end_round

#import lists created from config
from config import vowels
from config import letters_already_guessed
from config import words_already_chosen
from config import words_list
from config import wheel_wedges
from config import prize_options 

#import dictionaries created from config
from config import turn_options
from config import player_order_options
from config import players_information

#define functions for game play

#reset variables for new game at beginning of game
def game_reset():
    global round_number
    global end_round
    global players_information
    round_number = 1
    end_round = False
    players_information = {'Player A':{'Name': '', 'Round Earnings': 0, 'Total Earnings': 0}, 
                       'Player B':{'Name': '', 'Round Earnings': 0, 'Total Earnings': 0},
                       'Player C':{'Name': '', 'Round Earnings': 0, 'Total Earnings': 0}}

#to make console look nice throughout code
def make_space():
    print('================================================================================')
 
#enter play names at beginning of game
def enter_player_name(player_letter_ABC):
    valid = True
    while valid == True:
        entered_name = ''
        entered_name = input(f'{new_line}Please enter the name of Player {player_letter_ABC}: ').title()
        if len(entered_name) > 50:
            print('\nToo long of a name entered. Try again.') 
            continue
        elif all(x.isalpha() or x.isspace() for x in entered_name): 
            print(f'{new_line}Welcome to Wheel of Fortune {entered_name}!')
            players_information[f'Player {player_letter_ABC}']['Name'] = entered_name
            valid = False
        else:
            print('Only letters and spaces for names please. Try again!')
            continue
    return players_information

#start game at beginning of game
def start_game():
    game_reset()
    print('\nWelcome to: WHEEL!! OF!! FORTUNE!!!\nWe are excited for you to be here today!\n\nHere is how to play:')
    print('\nThere are three players and three rounds (but only the player with the most money makes it to Round 3!)\nThe game will display a word in hangman format for you to guess.')
    print('\nA randomly chosen player will start. They can either: spin the wheel, buy a vowel (if they have at least $250), or guess the word.')
    print('\nSpinning the wheel may get you $ if you then guess a consonant correctly. \nEvery correct consonant or vowel will appear in the hangman word.')
    print('\nThe first round will continue until someone guesses the word correctly. The person who guesses the word correctly keeps their $ while other players lose their $.')
    print('\n Second round is the same. At the end, whoever has the most $ overall will continue to Round 3. We will get to those special rules later!')
    make_space()
    print('\n We will now get started by entering in player information!')
    enter_player_name('A')
    enter_player_name('B')
    enter_player_name('C')
    make_space()
    print('\nHere are the players and their starting round and total game earnings (none...lol):')
    for player_letter, player_info in players_information.items():
        print(new_line,player_letter)
        for key in player_info:
            print(key + ':', player_info[key])

#choose random word at beginning of rounds (1-3)
def choose_random_word():
    valid = True
    while valid == True:
        global chosen_word
        chosen_word = random.choice(words_list)
        if chosen_word in words_already_chosen:
            continue
        else:
            words_already_chosen.append(chosen_word)
            valid = False
    return chosen_word 

#make chosen word hidden at beginning of rounds (1-3)
def create_hidden_word():
    global hidden_word
    for i in range(0, (len(chosen_word) + 1)):
        hidden_word = (('_' * i))
    return hidden_word

#choose player order beginning of round 1-2
def choose_player_order():
    global player_order
    player_order = random.choice(list(player_order_options.values()))
    return player_order  

#reset round variables and round earnings at beginning of round
def round_reset():
    global players_information
    global letters_already_guessed
    players_information ['Player A']['Round Earnings'] = 0
    players_information ['Player B']['Round Earnings'] = 0
    players_information ['Player C']['Round Earnings'] = 0
    letters_already_guessed = []
    choose_player_order()
    choose_random_word()
    create_hidden_word()

#check input for vowels, consonants, words, ensure right format and if already guessed (each turn and round 3 choices)
def check_input(prompt, vowel_consonant_word):
    global player_guess
    player_guess = ''
    invalid_input = True
    while invalid_input == True:
        player_guess = input(prompt).lower()
        if player_guess.isalpha() == False:
            print('\nPlease use letters only. Try again')
            continue
        if vowel_consonant_word == 'vowel':
            if len(player_guess) != 1:
                print('\nPlease only buy one vowel at a time')
                continue
            if player_guess not in vowels:
                print('\nYou can only buy vowels (a e i o u). Try again')
                continue
            elif player_guess in letters_already_guessed:
                print('\nThis vowel has already been bought. Try again')
                continue
            else: 
                letters_already_guessed.append(player_guess)
                invalid_input = False
        if vowel_consonant_word == 'consonant':
            if len(player_guess) != 1:
                print('\nPlease only guess one consonant at a time')
                continue
            if player_guess in vowels:
                print('\nYou can only guess consonants NOT vowels (vowels = a e i o u). Try again')
                continue
            elif player_guess in letters_already_guessed:
                print('\nThis consonant has already been guessed. Try again')
                continue
            else: 
                letters_already_guessed.append(player_guess)
                invalid_input = False
        if vowel_consonant_word == 'word':
            if len(player_guess) != len(chosen_word):
                print('\nYour guess is not the same length as the hidden word. Try again!')
                continue
            else:
                invalid_input = False
    return player_guess

#guess word at turn in rounds 1-2
def turn_guess_word():
    check_input('Guess the word: ', 'word')
    global stay_in_turn
    global round_winner 
    global end_round
    if player_guess == chosen_word:
        print(player_guess)
        print(f'{new_line}Congratulations {turn_player_name} you are correct: {chosen_word} was the right word! You won the round!')
        for i in players_information:
            if players_information[i]['Name'] == turn_player_name:
                round_winner = i
        print(f'{new_line}End of round {round_number}!')
        end_round = True
        stay_in_turn = False
        
    else:
        print(f'{new_line}Sorry {turn_player_name} that was not the correct word. Your turn is over.')
        end_round = False
        stay_in_turn = False

#guess consonant at turn
def turn_guess_consonant():
    check_input('Guess a consonant: ', 'consonant')
    global hidden_word
    global stay_in_turn 
    global round_winner
    global turn_player_round_earnings
    global players_information
    global end_round
    if player_guess in chosen_word:
        letter_location = []
        for i in range(len(chosen_word)):
            if (chosen_word[i] == player_guess):
                letter_location.append(i)

        for location in letter_location:
            hidden_word = hidden_word[:location] + player_guess + hidden_word[location + 1:]
        if hidden_word == chosen_word:
            print(hidden_word)
            for i in players_information:
                if players_information[i]['Name'] == turn_player_name:
                    round_winner = i
            print(f'{new_line}Congratulations {turn_player_name} you are correct: {chosen_word} was the right word! You get ${len(letter_location) * wheel_wedge_chosen} more dollars AND you won the round!')  
            turn_player_round_earnings = turn_player_round_earnings + (len(letter_location) * wheel_wedge_chosen)
            players_information[player_order[turn_number]]['Round Earnings']= turn_player_round_earnings
            end_round = True
            stay_in_turn = False
        else:
            print(hidden_word)
            print(f'{new_line}Congrats {turn_player_name}! {player_guess} is in the word. You get ${len(letter_location) * wheel_wedge_chosen} more dollars and your turn continues!')
            turn_player_round_earnings = turn_player_round_earnings + (len(letter_location) * wheel_wedge_chosen)
            players_information[player_order[turn_number]]['Round Earnings']= turn_player_round_earnings
            end_round = False
            stay_in_turn = True
    else:
        print(hidden_word)
        print(f'{new_line}Sorry {turn_player_name} that consonant is not in the word. You get $0 and your turn is over.')
        end_round = False
        stay_in_turn = False

#spin the wheel at turn at rounds (1-2)
def turn_spin_wheel ():
    global wheel_wedge_chosen
    global stay_in_turn
    global turn_player_round_earnings
    global players_information
    global end_round
    wheel_wedge_chosen = random.choice(wheel_wedges)
    if wheel_wedge_chosen == 'BANKRUPT!!!!':
        print(f'Oh no {turn_player_name}! You spun {wheel_wedge_chosen} All of your round earnings are now gone :( And your turn is over!')
        turn_player_round_earnings = 0
        players_information[player_order[turn_number]]['Round Earnings']= turn_player_round_earnings
        end_round = False
        stay_in_turn = False
    elif wheel_wedge_chosen == 'Lose a Turn!!!!':
        print(f'Oh no {turn_player_name}! You spun {wheel_wedge_chosen} :( Your turn is over!')
        end_round = False
        stay_in_turn = False
    else:
        print(f'{new_line}You spun ${wheel_wedge_chosen}. Time to guess a consonant. You will earn ${wheel_wedge_chosen} for every letter in the word that matches your chosen consonant')
        wheel_wedge_chosen = int(wheel_wedge_chosen)
        turn_guess_consonant()
        return wheel_wedge_chosen

#buy a vowel at turn (rounds 1-2)
def turn_buy_vowel():
    global stay_in_turn
    global round_winner
    global players_information
    global turn_player_round_earnings
    global end_round
    if turn_player_round_earnings < vowel_cost:
        print(f'{new_line}Sorry {turn_player_name} you do not have enough money yet to buy a vowel. Either spin the wheel or guess a word.')
        end_round = False
        stay_in_turn = True
    else:    
        check_input('Purchase one vowel: ', 'vowel')
        global hidden_word
        if player_guess in chosen_word:
            turn_player_round_earnings = turn_player_round_earnings - vowel_cost
            players_information[player_order[turn_number]]['Round Earnings']= turn_player_round_earnings 
            letter_location = []
            for i in range(len(chosen_word)):
                if (chosen_word[i] == player_guess):
                    letter_location.append(i)

            for location in letter_location:
                hidden_word = hidden_word[:location] + player_guess + hidden_word[location + 1:]
            if hidden_word == chosen_word:
                for i in players_information:
                    if players_information[i]['Name'] == turn_player_name:
                        round_winner = i
                print(f'{new_line}You bought {player_guess} for $250. Congrats {turn_player_name} that is in the word! Congratulations {turn_player_name} you are correct: {chosen_word} was the right word! You won the round!')  
                end_round = True 
                stay_in_turn = False
               
            else:
                print(hidden_word)
                print(f'{new_line}You bought {player_guess} for $250. Congrats {turn_player_name} that is in the word, and your turn continues!')
                end_round = False
                stay_in_turn = True
        else:
            turn_player_round_earnings = turn_player_round_earnings - vowel_cost
            players_information[player_order[turn_number]]['Round Earnings']= turn_player_round_earnings
            print(hidden_word)
            print(f'{new_line}You bought {player_guess} for $250. Sorry {turn_player_name} that is not in the word. Your turn is over.')
            end_round = False
            stay_in_turn = False
    return turn_player_round_earnings

#check turn option integer at turn
def check_turn_option():
    invalid_turn_option = True
    while invalid_turn_option == True:
        try:
            global turn_chosen_option
            turn_chosen_option = int(input((f'{new_line}Select an option from the menu above! {new_line}{new_line}{turn_player_name} chooses: ')))
            if turn_chosen_option > 3:
                print('Choose a number option within range!')
                continue
            else:
                return turn_chosen_option
        except ValueError:
            print('Choose a number!')

#player turn for rounds 1-2 
def turns():
    global turn_number
    turn_number = 1
    while True:
        global turn_player_name
        turn_player_name = players_information[player_order[turn_number]]['Name']
        global turn_player_round_earnings
        turn_player_round_earnings = players_information[player_order[turn_number]]['Round Earnings']
        make_space()
        print(f'{new_line}{turn_player_name} it is your turn! You have ${turn_player_round_earnings} in round earnings.{new_line}{new_line}Remember you can only buy a vowel if you have at least $250 in round earnings!')
        print(f'{new_line}Here is your word to guess:{new_line}{hidden_word}{new_line}')
        print(*turn_options, sep = '\n')
        check_turn_option()
        if turn_chosen_option == 1:
            turn_spin_wheel()
            if end_round == True:
                break
            if stay_in_turn == True:
                continue
            else:
                if turn_number == 0 or turn_number == 1:
                    turn_number = turn_number + 1
                else:
                    turn_number = turn_number - 2
                continue
        elif turn_chosen_option == 2:
            turn_buy_vowel()
            if end_round == True:
                break
            if stay_in_turn == True:
                continue
            else:
                if turn_number == 0 or turn_number == 1:
                    turn_number = turn_number + 1
                else:
                    turn_number = turn_number - 2
                continue
        else:
            turn_guess_word()
            if end_round == True:
                break
            if stay_in_turn == True:
                continue
            else:
                if turn_number == 0 or turn_number == 1:
                    turn_number = turn_number + 1
                else:
                    turn_number = turn_number - 2
                continue

 #end of round  
def round_end():
    global round_number
    global new_round
    global players_information
    players_information [round_winner]['Total Earnings'] = players_information [round_winner]['Total Earnings'] + players_information [round_winner]['Round Earnings'] 
    players_information ['Player A']['Round Earnings'] = 0
    players_information ['Player B']['Round Earnings'] = 0
    players_information ['Player C']['Round Earnings'] = 0
    print('\nWe have reset round earnings to $0 for the next round. Here are the players and their total game earnings:')
    for player_letter, player_info in players_information.items():
        print(new_line,player_letter)
        for key in player_info:
            print(key + ':', player_info[key])
    if round_number == 1:
        round_number = round_number + 1
        new_round = True
        #start another round
    else:
        new_round = False 
        #move on to round 3

#choose prize as bonus round 3
def choose_random_prize():
    global chosen_prize 
    chosen_prize = random.choice(prize_options)
    return chosen_prize

#determine the player who will play in round 3 (who has highest total game earnings)
def find_round3_player():
    global round_3_player_name
    global round_3_player_earnings
    global players_game_earnings
    players_game_earnings = {}
    for keys in players_information:
        player_earning = players_information[keys]['Total Earnings']
        players_game_earnings.update({keys: player_earning})
    round_3_player_earnings = max(players_game_earnings.values())
    for i in players_game_earnings:
        if players_game_earnings[i]==round_3_player_earnings:
            round_3_player_name = players_information[i]['Name']

#round 3 hidden word with rstlne filled in
def round_3_hidden_word():
    choose_random_word()
    create_hidden_word()
    global letters_already_guessed
    global hidden_word
    provided_letters = ['r', 's', 't', 'l', 'n', 'e']
    letters_already_guessed = provided_letters
    letter_location = []
    present_provided_letters = []
    for i in range(len(chosen_word)):
        if (chosen_word[i] in provided_letters):
            letter_location.append(i)
            present_provided_letters.append(chosen_word[i])
    for location in letter_location:
        hidden_word = hidden_word[:location] + provided_letters[provided_letters.index(chosen_word[location])] + hidden_word[location + 1:]
    return hidden_word

#add in 3 consonants and 1 vowel player guesses if present in round 3
def check_r3_guess():
    global hidden_word
    if player_guess in chosen_word:
            letter_location = []
            for i in range(len(chosen_word)):
                if (chosen_word[i] == player_guess):
                    letter_location.append(i)
            for location in letter_location:
                hidden_word = hidden_word[:location] + player_guess + hidden_word[location + 1:]

#round 3 play
def round_3():
    choose_random_prize()
    find_round3_player()
    round_3_hidden_word()
   
    make_space()
    print(f'Welcome to Round 3 {round_3_player_name}! The rules are different for you in this round.{new_line}We have chosen a random prize for you; if you guess the word, you recieve your total earnings AND the prize!')
    print('\nWe will fill in the letters RSTLNE before you begin, and we will show you the word.\nThen you will guess 3 consonants and one vowel (no spin or purchase required).\n...')
    print(f'{new_line}Then you have TEN SECONDS to guess the word!! {round_3_player_name}, you CAN do this! :)')
    make_space()
    print(f'{new_line}Here is the word with letters RSTLNE already filled in:{new_line}{hidden_word}')
    
    check_input('Choose your first consonant: ', 'consonant')
    #maybe make this a repeated function
    check_r3_guess()
    check_input('Choose your second consonant: ', 'consonant')
    check_r3_guess()
    check_input('Choose your third consonant: ', 'consonant')
    check_r3_guess()
    check_input('Choose your one vowel: ', 'vowel')
    check_r3_guess()
    make_space()
    
    print(hidden_word)
    print('\nYou will have five seconds to guess the word.')
    make_space()
    make_space()
    print('Starting now!')
    try:
        player_guess = inputimeout('Guess the word: ', timeout=5)
    except TimeoutOccurred:
        player_guess = ''
    
    if player_guess == chosen_word:
        print(f'Congratulations you got it! The word was {chosen_word}!{new_line}You win ${round_3_player_earnings} and the {chosen_prize}!!')
        print(f'Yay {round_3_player_name} I knew you could do it!!')
        make_space()
    else:
        print(f'Aww man that was not the word! Do not worry {round_3_player_name}, you still get ${round_3_player_earnings}!')

#does player want new game after round 3 ends    
def play_again_response():
    global play_again
    play_again = ''   
    stay_in_game = ''
    stay_in_game = input('Would you like to play again? Yes/No: ')
    if stay_in_game == 'Yes':
        print('Wheel of Fortune will start anew!')
        play_again = True
        #stay in game loop
    else:
        print('It was nice playing with you! WHEEL!! OF!! FORTUNE!!!')
        play_again = False


#main game code

while True:
    start_game()
    
    while True:
        round_reset()
        turns()
        round_end()
        if new_round == False:
            break
        else:
            continue

    round_3()

    play_again_response()
    if play_again == True:
        print('We are playing again!')
        continue
    if play_again == False:
        print('All good things must come to an end, goodbye!')
        break
