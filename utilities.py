from random import randint

class Pickaxe:
    pickaxe_price = [50, 150]
    minerals = ["copper", "silver", "gold"]

    def __init__(self, level=1):
        self.level = level
    
    # def max_mine(self):
    #     # returns the highest mineral that it can mine
    #     # TODO: SHOWS COPPER SILVER AND GOLD
    #     return self.minerals[self.level - 1]

    def can_mine(self):
        # returns the items that it can mine 
        return self.minerals[:self.level] 

    def upgrade(self):
        return NotImplemented 

    
class Backpack:
    def __init__(self, contents={}, max_capacity=10):
        # stores the contents of the bag in dictionary
        self.contents = contents
        self.max_capacity = max_capacity
    
    def remaining_capacity(self):
        return self.max_capacity - self.capacity()

    def capacity(self):
        if len(self.contents) == 0:
            return 0
        return sum(self.contents.values())
    
    def upgrade_price(self):
        return self.max_capacity * 2

    def upgrade(self):
        self.max_capacity += 2

    def add(self, quantity, mineral):
        # add the mineral into the bag
        if mineral in self.contents:
            self.contents[mineral] += quantity
        else:
            self.contents[mineral] = quantity

class Player:
    TURNS_PER_DAY = 20
    TOWN_POS = 0 + 0j

    def __init__(self, backpack: Backpack, pickaxe: Pickaxe, name="", pos = TOWN_POS, GP = 0, day = 1, steps = 0, turns = TURNS_PER_DAY, portal=None):
        self.pos = pos
        self.backpack = backpack
        self.GP = GP
        self.day = day
        self.steps = steps
        self.turns = turns
        self.pickaxe = pickaxe
        self.name = name
        self.portal = portal
   
    def display_info(self, in_town):
        print("----- Player Information -----")
        print("Name:", self.name)
        if in_town:
            if self.portal == None:
                print("Portal Position: Not Placed")
            else:
                print("Portal Position: ({x}, {y})".format(x=int(self.portal.real), y=int(self.portal.imag)))
        else:
            print("Current Position: ({x}, {y})".format(x=int(self.pos.real), y=int(self.pos.imag)))

        # can_mine()[-1] returns the last ore in the list, which is of the highest level
        print("Pickaxe level: {level} ({limit})".format(level=self.pickaxe.level, limit=self.pickaxe.can_mine()[-1]))
        
        # if in the mines, display the ores in the backpack if it is not empty
        if not in_town and len(self.backpack.contents) > 0:
            for ore in ["gold", "silver", "copper"]:
                if ore in self.backpack.contents: 
                    print(ore.capitalize() + ": " + str(self.backpack.contents[ore]))
                else:
                    print(ore.capitalize() + ": 0")

        print("------------------------------")
        print("Load: {}/{}".format(self.backpack.capacity(), self.backpack.max_capacity))
        print("------------------------------")
        print("GP:", self.GP)
        print("Steps taken:", self.steps)
        print("------------------------------")

    def move(self, direction, board_width, board_height):
        # returns the position 
        match direction:
            # move up
            case "W":
                if self.pos.real == 0:
                    # cannot move up
                    return float("inf") 
                else:
                    return self.pos - 1
            # move left
            case "A":
                if self.pos.imag == 0:
                    return float("inf")
                else:
                    return self.pos - 1j
            # move down
            case "S":
                if self.pos.real == board_height - 1:
                    return float("inf")
                else:
                    return self.pos + 1
            case "D":
                if self.pos.imag == board_width - 1:
                    return float("inf")
                else:
                    return self.pos + 1j

    def mine_mineral(self, mineral):
        # returns the randomly generated quantity of mineral mined
        match mineral:
            case "copper":
                return randint(1, 5)
            case "silver":
                return randint(1, 3)
            case "gold":
                return randint(1, 2)

    def sell(self):
        # sell all items
        sell_text = "You sell "
        sell_text += ", ".join(["{} {} ore".format(self.backpack.contents[i], i) for i in self.backpack.contents])
        total = 0
        for mineral in self.backpack.contents:
            # sell_text += "{quantity} {mineral} ore ".format(quantity=self.backpack[item], mineral=item)
            match mineral:
                case "copper":
                    price = randint(1, 3)
                case "silver":
                    price = randint(5, 8)
                case "gold":
                    price = randint(10, 18)
            
            total += price * self.backpack.contents[mineral]
        
        sell_text += " for {} GP.".format(total)
        print(sell_text)

        # update self
        self.GP += total
        self.backpack.contents = {}

        print("You now have {} GP!".format(self.GP))
        print()


class Map:
    def __init__(self, width=0, height=0, explored={0+0j, 0+1j, 1+0j, 1+1j}, board=[]):
        self.width = width
        self.height = height
        self.explored = explored
        self.board = board

    def load_map(self, filename):
        map_file = open(filename, 'r')
        map_parsed = map_file.read().split("\n")
        
        # store the map into a 2d array 
        for i in range(len(map_parsed)):
            row = []
            for j in range(len(map_parsed[i])):
                row.append(map_parsed[i][j])
            self.board.append(row)

        self.width = len(map_parsed[0])
        self.height = len(map_parsed)

        map_file.close()
    
    def draw_viewport(self, pos):
        print("+---+")
        # loop through the coords -1, 0, 1
        for i in range(-1, 2):
            row = "|"
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    # player pos 
                    row += "M"
                elif pos.real + i < 0 or pos.real + i >= self.height or pos.imag + j < 0 or pos.imag + j >= self.width:
                    # border 
                    row += "#"
                else:
                    row += self.board[int(pos.real + i)][int(pos.imag + j)]
            row += "|"
            print(row)
        print("+---+")
    
    def draw_map(self, player_pos, portal):
        # print borders 
        print("+" + "-" * self.width + "+")
        for i in range(self.height):
            row = "|"
            for j in range(self.width):
                current = i + j * 1j
                # if current pos has been explored, print it
                if current == player_pos:
                    row += "M"
                # if this is in town and there is a portal stone, print it 
                elif portal != None and portal == current:
                    row += "P"
                else:
                    if current in self.explored:
                        row += self.board[int(i)][int(j)]
                    else:
                        row += "?"
            row += "|"
            print(row)
        # print borders 
        print("+" + "-" * self.width + "+")

    def clear_fog(self):
        return NotImplemented

