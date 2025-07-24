from utilities import Pickaxe, Backpack, Player, Map

# init objects
backpack = Backpack()
pickaxe = Pickaxe()
player = Player(backpack, pickaxe)
board = Map()

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
            
    match shop_choice:
        case "B":
            # can buy
            if player.GP >= player.backpack.upgrade_price():
                player.backpack.upgrade()
                print("Congratulations! You can now carry {} items!".format(player.backpack.max_capacity))
            else:
                print("Insufficient GP.")
        case "L":
            # leave shop and return to town menu 
            town(init=False)

def town(init):
    if init:
        name = input("Greetings, miner! What is your name? ")
        print("Pleased to meet you, {}. Welcome to Sundrop Town!".format(name))
        player.name = name

    show_town_menu()

    town_choice = input("Your choice? ").upper()
    match town_choice:
        case "B":
            # enter shop
            shop()
        case "I":
            # display player information
            player.display_info()
            town(init=False)
        case "M":
            # load the board if this is the first time
            if len(board.board) == 0:
                board.load_map(filename="level1.txt")

            board.draw_map(player.pos)
            town(init=False)
        case "E":
            return NotImplemented
        case "V":
            return NotImplemented
        case "Q":
            return NotImplemented
        case _:
            return  


def main():
    show_main_menu()
    choice = input("Your choice? ").upper()
    match choice:
        case "N":
            # new game 
            town(init=True)
        case "L":
            # load game
            return NotImplemented
        case "Q":
            # exit game
            exit()
        case _:
            # invalid input 
            return NotImplemented

print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire and live happily ever after?")
print("-----------------------------------------------------------")
main()
