
class Pickaxe:
    pickaxe_price = [50, 150]
    minerals = ["copper", "silver", "gold"]

    def __init__(self, level=1):
        self.level = level
    
    def max_mine(self):
        # returns the highest mineral that it can mine
        # TODO: SHOWS COPPER SILVER AND GOLD
        return self.minerals[self.level - 1]

    def can_mine(self):
        return NotImplemented

    def upgrade(self):
        return NotImplemented 

    
class Backpack:
    def __init__(self, contents={}, max_capacity=10):
        # stores the contents of the bag in dictionary
        self.contents = contents
        self.max_capacity = max_capacity
    
    def return_capacity(self) -> int:
        return sum(self.contents.values())
    
    def upgrade_price(self):
        return self.max_capacity * 2

    def upgrade(self):
        self.max_capacity += 2

class Player:
    TURNS_PER_DAY = 20

    def __init__(self, backpack, pickaxe, name="", pos = 0+0j, GP = 0, day = 1, steps = 0, turns = TURNS_PER_DAY):
        self.pos = pos
        self.backpack = backpack
        self.GP = GP
        self.day = day
        self.steps = steps
        self.turns = turns
        self.pickaxe = pickaxe
        self.name = name
   
    def display_info(self):
        print("----- Player Information -----")
        print("Name:", self.name)
        print("Portal Position: ({x}, {y})".format(x=int(self.pos.real), y=int(self.pos.imag)))
        print("Pickaxe level: {level} ({limit})".format(level=self.pickaxe.level, limit=self.pickaxe.max_mine()))
        print("------------------------------")
        print("Load: {}/{}".format(self.backpack.return_capacity(), self.backpack.max_capacity))
        print("------------------------------")
        print("GP:", self.GP)
        print("Steps taken:", self.steps)
        print("------------------------------")


class Map:
    def __init__(self, width=0, height=0, explored={0+0j, 0+1j, 1+0j, 1+1j}, board=[], portal=None):
        self.width = width
        self.height = height
        self.explored = explored
        self.board = board
        self.portal = portal

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
    
    def draw_viewport(self):
        return NotImplemented
    
    def draw_map(self, player_pos):
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
                elif self.portal != None and self.portal == current:
                    row += "P"
                else:
                    if current in self.explored:
                        row += self.board[i][j]
                    else:
                        row += "?"
            row += "|"
            print(row)
        # print borders 
        print("+" + "-" * self.width + "+")

    def clear_fog(self):
        return NotImplemented

