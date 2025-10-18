import random
# limitations:
# no "board" list allowed


print("REMEMBER UP IS NEGATIVE, RIGHT IS POSITIVE")


def sum_tuple(a:tuple,b:tuple):
    return (a[0]+b[0],a[1]+b[1])
def sub_tuple(a:tuple,b:tuple):
    return (a[0]-b[0],a[1]-b[1])
def mult_tuple(a:tuple,b:float):
    return (a[0]*b,a[1]*b)
def div_tuple(a:tuple,b:float):
    return (a[0]/b,a[1]/b)


def compare_tuple(a,b):
    return a[0] == b[0] and a[1] == b[1]


def sort_pos(pos_list):
        #print(pos_list)
        if len(pos_list) == 1:
            #print("reached base case")
            return pos_list
            
        else:
            half = len(pos_list)//2
            a = pos_list[:half]
            b = pos_list[half:]

            sorted_a = sort_pos(a)
            sorted_b = sort_pos(b)

            sorted_join = []
            
            for i in range(len(pos_list)):
                if len(sorted_a) == 0:
                    sorted_join.append(sorted_b.pop(0))
                elif len(sorted_b) == 0:
                    sorted_join.append(sorted_a.pop(0))
                elif sorted_a[0][1] >= sorted_b[0][1]:
                    sorted_join.append(sorted_b.pop(0))
                elif sorted_a[0][1] <= sorted_b[0][1]:
                    sorted_join.append(sorted_a.pop(0))
                else:
                    print("something happened")


        return sorted_join




class Block_Shapes:

    def __init__(self,relPosList: list,):

        self.rot_amount = len(relPosList)
        self.rel_pos = relPosList
        self.current_shape = 0
    def get_rel_pos(self):
        return self.rel_pos[self.current_shape]
    def rotate_clock(self):
        if self.current_shape != self.rot_amount:

            self.current_shape += 1
        else:
            self.current_shape = 0
    def rotate_anticlock(self):
        if self.current_shape != 0:

            self.current_shape -= 1
        else:
            self.current_shape = self.rot_amount - 1


shapes_list = [Block_Shapes([[(0,0),(1,0),(0,1),(1,1)]]),#2x2 block
               Block_Shapes([[(0,-1),(0,0),(0,1),(0,2)],[(-1,0),(0,0),(1,0),(2,0)]]), #long stick
               Block_Shapes([[(0,-1),(0,0),(0,1),(1,0)],[(-1,0),(0,0),(0,1),(1,0)],[(0,-1),(0,0),(0,1),(-1,0)],[(-1,0),(0,0),(0,-1),(1,0)]]), #flat T block
               Block_Shapes([[(0,-1),(0,0),(0,1),(1,1)],[(1,0),(0,0),(-1,0),(-1,1)],[(-1,-1),(0,-1),(0,0),(0,1)],[(1,-1),(1,0),(0,0),(-1,0)]]), #L shape
               Block_Shapes([[(0,-1),(0,0),(0,1),(-1,1)],[(1,0),(0,0),(-1,0),(-1,-1)],[(1,-1),(0,-1),(0,0),(0,1)],[(1,1),(1,0),(0,0),(-1,0)]]), # reverse L Shape 
               Block_Shapes([[(-1,0),(0,0),(0,-1),(1,-1)],[(1,-1),(1,0),(0,0),(0,1)]]), # Stair (l->r)  _/-
               Block_Shapes([[(-1,-1),(0,-1),(0,0),(1,0)],[(0,-1),(0,0),(1,0),(1,1)]]), # Stair (r->l) -\_
               ]

class Block:
    def __init__(self,init_pos,shape,col=(255,0,0)):
        self.pos = init_pos
        self.shape:Block_Shapes = shape
        self.col = col
        self.gravity = (0,1)
        self.locking_next_step = False
    
    def colliding_after_grav(self,colliders_list):
        next_pos = sum_tuple(self.pos,self.gravity)
        for collider in colliders_list:
            for rel_pos in self.shape.get_rel_pos():
                if compare_tuple(sum_tuple(rel_pos,next_pos),collider):
                    return True
        
        return False


    def grav(self,col_list):
        #check for collisions:

        if not self.colliding_after_grav(col_list):
            self.pos = sum_tuple(self.pos,self.gravity)
            
        else:
            self.locking_next_step = True


#scoring in original tetris (at level 1) scales with level
#one line: 100
#two lines: 300
#three lines: 1000
#four lines (tetris): 1600

class Game:
    def __init__(self) -> None:
        self.locked_blocks = []
        self.score = 0
        self.lines = 0
        self.current_falling: Block
        self.next_block = self.generate_block()
    
    def update(self):
        if self.current_falling.locking_next_step:
            self.falling_to_static(self.current_falling)
            self.current_falling = self.next_block
            self.next_block = self.generate_block()
        else:

            self.current_falling.grav(self.locked_blocks)

    def generate_block(self):
        return Block((random.randint(2,5),2),random.choice(shapes_list))

    def init_block(self,bloc:Block):
        self.current_falling = bloc

    def debug_update_locked_blocks(self,new_list):
        self.locked_blocks = new_list

    def find_lines(self,pos_list):
        current_y = -1
        pos_in_line = 0
        lines_detected = []
        for idx,pos in enumerate(pos_list):
            if idx == 0:
                current_y = pos[1]
                pos_in_line = 1
            else:
                if pos[1] == current_y:
                    pos_in_line += 1
                    if pos_in_line == 8:
                        lines_detected.append(current_y)
                        current_y = -1
                        pos_in_line = 0
                        continue
                else:
                    pos_in_line = 1
                    current_y = pos[1]
        
        
        return lines_detected
    def update_pos_above(self,y:int):
        
        for idx,pos in enumerate(self.locked_blocks):
            #print()
            #print(pos)
            if pos[1] == y:
                self.locked_blocks[idx] = None

            if pos[1] < y:
                self.locked_blocks[idx] = sum_tuple(pos,(0,1))
    
        self.locked_blocks = list(filter(lambda a: a != None, self.locked_blocks))

    def falling_to_static(self,bloc:Block):
        for rel_pos in bloc.shape.get_rel_pos():
            self.locked_blocks.append(sum_tuple(bloc.pos,rel_pos))
        
        self.locked_blocks = sort_pos(self.locked_blocks)
        


    def remove_lines(self):
        lines_to_remove = self.find_lines(self.locked_blocks)
        if len(lines_to_remove) != 0:
            for line in lines_to_remove:
                self.update_pos_above(line)
                self.lines += 1
        



game = Game()

game.debug_update_locked_blocks([(6,13),(7,14),(2,14),(6,14),(3,15),(7,15),(0,15),(6,15),(2,15),(0,16),(7,16),(6,16),(2,16),(3,16),(7,17),(2,17),(3,17),(4,17),(0,17),(6,17)])
game.init_block(Block((5,2),shapes_list[2]))
#random.choice(shapes_list)
game.current_falling.shape.rotate_anticlock()
game.current_falling.shape.rotate_anticlock()



for i in range(80):
    game.update()
    print(game.locked_blocks)
    input()