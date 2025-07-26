# Nicole Tan (IT01)

from utilities import Pickaxe, Backpack, Player, Map, print_colour
import pickle

# init objects
backpack = Backpack()
pickaxe = Pickaxe()
player = Player(backpack, pickaxe)
board = Map()
board.load_map(filename="level1.txt")

# define variables
SAVED_FILE_DIR = "saved_games.pkl"
win = False

def save_game(filename):
    # save the player and board objects using pickle 
    with open(filename, "wb") as f:
        game = {"player": player, "board": board}
        pickle.dump(game, f)

    print("Game saved.")

def load_game(filename):
    # load the game and store it in variables
    with open(filename, "rb") as f:
        game = pickle.load(f)
        global player, board
        player = game["player"]
        board = game["board"]


def show_main_menu():
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    print("DAY", player.day)
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

def show_shop_menu():
    print("----------------------- Shop Menu -------------------------")

    # if player.pickaxe.level < 3:
        # print("(P)ickaxe upgrade to Level {} to mine silver ore for {} GP".format(player.pickaxe.level, player.pickaxe.upgrade_price()))

    print("(B)ackpack upgrade to carry {capacity} items for {price} GP".format(capacity = player.backpack.max_capacity + 2, price=player.backpack.upgrade_price()))

    print("(L)eave shop")
    print("-----------------------------------------------------------")
    # print currency
    print("GP:", player.GP)
    print("-----------------------------------------------------------")

def shop():
    show_shop_menu()
    shop_choice = input("Your choice? ").upper()
            
    # input validation
    while len(shop_choice) == 0 or shop_choice not in "BL":
       print_colour("Invalid input. Input should be either (B) or (L).", "red")
       shop_choice = input("Your choice? ").upper() 

    match shop_choice:
        case "B":
            # can buy
            if player.GP >= player.backpack.upgrade_price():
                player.GP -= player.backpack.upgrade_price() 
                player.backpack.upgrade()
                print("Congratulations! You can now carry {} items!".format(player.backpack.max_capacity))
            else:
                print("Insufficient GP.")
            shop()

        case "L":
            # leave shop and return to town menu 
            town(init=False)

def use_portal():
    print("You place your portal stone here and zap back to town.")
                
    player.portal = player.pos

    if len(player.backpack.contents) > 0:
        player.sell()
        # check for game win 
        if player.GP >= 500:
            global win
            win = True
            print("-------------------------------------------------------------")
            print_colour("Woo-hoo! Well done, {name}, you have {GP} GP!".format(name=player.name, GP=player.GP), "green")
            print("You now have enough to retire and play video games every day.")
            print("And it only took you {days} days and {steps} steps! You win!".format(days=player.day, steps=player.steps))
            print()
            return
    else:
        print("You don't have anything to sell.")

    # start next day
    player.day += 1
    player.turns = player.TURNS_PER_DAY
    
def enter_mine():
    print("DAY", player.day)

    board.draw_viewport(player.pos)

    print("Turns left: {turns} \t Load: {curr_load}/{max_load} \t Steps: {steps}".format(turns=player.turns, curr_load=player.backpack.capacity(), max_load=player.backpack.max_capacity, steps=player.steps))
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

    action = input("Action? ").upper()

    # input validation
    while len(action) == 0 or  action not in "WASDMIPQ":
        print_colour("Invalid input. Choice should be either (W), (A), (S), (D), (M), (I), (P) or (Q)", "red")
        action = input("Action? ").upper()    

    match action:
        case "W" | "A" | "S" | "D":
            # move the player
            # decrement turns and steps regardless if move is valid
            player.turns -= 1
            player.steps += 1
            
            new_pos = player.move(action, board.width, board.height)
            can_move = True

            if new_pos == float("inf"):
                # cannot move here
                print_colour("That's outside the border, so you can't go that way", "red")
            else:
                cell = board.board[int(new_pos.real)][int(new_pos.imag)]

                # if player steps on a mineral
                if cell in "CSG":
                    mineral = "copper" if cell == "C" else "silver" if cell == "S" else "gold"

                    # check if backpack is full
                    if player.backpack.capacity() == player.backpack.max_capacity:
                        can_move = False
                        print_colour("You can't carry any more, so you can't go that way.", "red")
                    
                    # check if pickaxe can mine this item
                    elif mineral not in player.pickaxe.can_mine():
                        can_move = False
                        print_colour("Cannot mine this item, upgrade your pickaxe first!", "red")
                    
                    else:
                        # can mine item
                        quantity = player.mine_mineral(mineral)
                        # remove ore from the map
                        board.board[int(new_pos.real)][int(new_pos.imag)] = " "

                        print("---------------------------------------------------")
                        print_colour("You mined {quantity} piece(s) of {mineral}.".format(quantity=quantity, mineral=mineral), "green")

                        if quantity > player.backpack.remaining_capacity():
                            print("... but you can only carry {} more piece(s)!".format(player.backpack.remaining_capacity()))
                            quantity = player.backpack.remaining_capacity()

                        player.backpack.add(quantity, mineral)
                        
                if can_move:
                    # set the new pos of the player
                    player.pos = new_pos
                    # update explored cells
                    board.explored.add(player.pos)
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= int(player.pos.real + i) < board.height or 0 <= int(player.pos.imag + j) < board.width:
                                board.explored.add(player.pos + i + j * 1j)

                    # if player steps on T, will return to town 
                    if player.pos == player.TOWN_POS:
                        town(init=False)


            # use portal 
            if player.turns == 0:
                print_colour("You are exhausted.", "red")
                use_portal()
                if win:
                    main()
                else:
                    town(init=False)
            else:
                enter_mine()
        case "M":
            # display the map
            board.draw_map(player_pos=player.pos, portal=player.portal)
            # show ui for entering mine again
            enter_mine()
        case "I":
            player.display_info(in_town=False)
            enter_mine()
        case "P":
            # place a portal stone 
            use_portal()
            if win:
                main()                
            else:
                town(init=False)
        case "Q":
            main()


def town(init):
    if init:
        name = input("Greetings, miner! What is your name? ")
        # input validation
        while len(name) == 0:
            name = input("Please enter a valid name: ")

        print("Pleased to meet you, {}. Welcome to Sundrop Town!".format(name))
        player.name = name

    show_town_menu()

    town_choice = input("Your choice? ").upper()

    # input validation
    while len(town_choice) == 0 or town_choice not in "BIMEVQ":
       print_colour("Invalid input. Choice should be either (B), (I), (M), (E), (V), (Q)", "red")
       town_choice = input("Your choice? ").upper() 

    match town_choice:
        case "B":
            # enter shop
            shop()
        case "I":
            # display player information
            player.display_info(in_town=True)
            town(init=False)
        case "M":
            # display the map
            # set player_pos to 0+0j as player is back in town
            board.draw_map(player_pos=0+0j, portal=player.portal)
            town(init=False)
        case "E":
            # enter mine 
            print("---------------------------------------------------")
            # align the day count in the middle
            print("{:^51}".format("DAY " + str(player.day)))
            print("---------------------------------------------------")
            enter_mine() 
        case "V":
            # save game 
            save_game(SAVED_FILE_DIR)
        case "Q":
            # go back to main menu 
            print()
            main()

def main():
    show_main_menu()
    choice = input("Your choice? ").upper()

    # input validation
    while len(choice) == 0 or choice not in "NLQ":
        print_colour("Invalid input. Choice should be either (N), (L) or (Q).", "red")
        choice = input("Your choice? ").upper() 

    match choice:
        case "N":
            # new game 
            town(init=True)
        case "L":
            # load game
            load_game(SAVED_FILE_DIR)
            town(init=False)
        case "Q":
            # exit game
            exit()

# introduction text
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire and live happily ever after?")
print("-----------------------------------------------------------")
main()
