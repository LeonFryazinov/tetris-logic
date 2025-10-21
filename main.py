import random
import time
import keyboard
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

def join_text(a:str,b:str,x_offset=5,y_offset=0):
    split_a = a.split("\n")
    split_b = b.split("\n")
    combined_string = ""
    max_len_a = 0
    for line in split_a:
        if len(line) > max_len_a:
            max_len_a = len(line)

    for i in range(len(split_a)): #(len(split_a) if len(split_a) > len(split_b)+y_offset else len(split_b)+y_offset)
        combined_string += split_a[i]
        combined_string += " " * ((max_len_a-len(split_a[i]))+x_offset)
        if i - y_offset >= 0 and i-y_offset < len(split_b):
            combined_string += split_b[i-y_offset]
        
        combined_string += "\n"
    
    return combined_string



class Block_Shapes:

    def __init__(self,relPosList: list,):

        self.rot_amount = len(relPosList)
        self.rel_pos = relPosList
        self.current_shape = 0
    @staticmethod
    def NONE():
        return Block_Shapes([])
    def is_none(self):
        if len(self.rel_pos) == 0:
            #print(self.rot_amount)
            return True
        else:
            #print("rot ammount: " + str(self.rot_amount))
            return False
    def get_rel_pos(self):
        return self.rel_pos[self.current_shape]
    
    def is_colliding(self,pos,locked_pos):
        for rel_pos in self.get_rel_pos():
            if sum_tuple(pos,rel_pos) in locked_pos:
                return True
        
        return False


    def calculate_pos_list(self,abs_pos):
        cell_pos = []
        for pos in self.rel_pos[self.current_shape]:
            cell_pos.append(sum_tuple(abs_pos,pos))
        return cell_pos


shapes_list = [Block_Shapes([[(0,0),(1,0),(0,1),(1,1)]]),#2x2 block
               Block_Shapes([[(0,-1),(0,0),(0,1),(0,2)],[(-1,0),(0,0),(1,0),(2,0)]]), #long stick
               Block_Shapes([[(0,-1),(0,0),(0,1),(1,0)],[(-1,0),(0,0),(0,1),(1,0)],[(0,-1),(0,0),(0,1),(-1,0)],[(-1,0),(0,0),(0,-1),(1,0)]]), #flat T block
               Block_Shapes([[(0,-1),(0,0),(0,1),(1,1)],[(1,0),(0,0),(-1,0),(-1,1)],[(-1,-1),(0,-1),(0,0),(0,1)],[(1,-1),(1,0),(0,0),(-1,0)]]), #L shape
               Block_Shapes([[(0,-1),(0,0),(0,1),(-1,1)],[(1,0),(0,0),(-1,0),(-1,-1)],[(1,-1),(0,-1),(0,0),(0,1)],[(1,1),(1,0),(0,0),(-1,0)]]), # reverse L Shape 
               Block_Shapes([[(-1,-1),(0,-1),(0,0),(1,0)],[(0,-1),(0,0),(-1,0),(-1,1)]]), # Stair (l->r)  _/-
               Block_Shapes([[(-1,0),(0,0),(0,-1),(1,-1)],[(1,1),(1,0),(0,0),(0,-1)]]), # Stair (r->l) -\_
               ]

class Block:
    def __init__(self,init_pos,shape,col=(255,0,0)):
        self.pos = init_pos
        self.init_pos = init_pos
        self.shape:Block_Shapes = shape
        self.shape.current_shape = 0
        self.col = col
        self.gravity = (0,1)
        self.locking_next_step = False
        

        
        
    
    def reset_to_init(self):
        self.pos = self.init_pos

    def colliding_after_grav(self,colliders_list):
        next_pos = sum_tuple(self.pos,self.gravity)
        for rel_pos in self.shape.get_rel_pos():

            if sum_tuple(rel_pos,next_pos) in colliders_list or sum_tuple(next_pos,rel_pos)[1] == 18:

                return True
        
        return False
    def collide_after_vect(self,vect,colliders_list):
        next_pos = sum_tuple(self.pos,vect)
        for rel_pos in self.shape.get_rel_pos():
            summed_next_pos = sum_tuple(rel_pos,next_pos)
            if summed_next_pos[0] == -1 or summed_next_pos[0] == 8 or summed_next_pos[1] > 17:
                return True              
            if summed_next_pos in colliders_list:
                return True
            
        return False
    
    def move_left(self,col_list):
        if not self.collide_after_vect((-1,0),col_list):
            self.pos = sum_tuple(self.pos,(-1,0))
            self.locking_next_step = False
    
    
    def move_right(self,col_list):
        if not self.collide_after_vect((1,0),col_list):
            self.pos = sum_tuple(self.pos,(1,0))
            self.locking_next_step = False
    def rotate_clock(self,locked_list):
        if self.shape.current_shape != self.shape.rot_amount-1:
            
            self.shape.current_shape += 1
            if self.shape.is_colliding(self.pos,locked_list):
                self.shape.current_shape -= 1
            else:
                self.locking_next_step = False

        else:
            self.shape.current_shape = 0
            if self.shape.is_colliding(self.pos,locked_list):
                self.shape.current_shape = self.shape.rot_amount-1
            else:
                self.locking_next_step = False
    def rotate_anticlock(self,locked_list):

        if self.shape.current_shape != 0:
            self.shape.current_shape -= 1
            if self.shape.is_colliding(self.pos,locked_list):
                self.shape.current_shape += 1
            else:
                self.locking_next_step = False

            
        else:
            self.shape.current_shape = self.shape.rot_amount - 1
            if self.shape.is_colliding(self.pos,locked_list):
                self.shape.current_shape = 0
            else:
                self.locking_next_step = False

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
        self.level = 1
        self.BREAK = False
        self.current_falling: Block
        self.next_block = self.generate_block()
        self.hold = Block((-1,-1),Block_Shapes.NONE())
        self.can_hold = True
    
    def check_loss(self):
        if self.current_falling.shape.is_colliding(self.current_falling.pos,self.locked_blocks):
            return True
        else:
            return False

    def move_block_left(self):
        self.current_falling.move_left(self.locked_blocks)
    def move_block_right(self):
        self.current_falling.move_right(self.locked_blocks)
    def rotate_block(self,dir=1): # direction is either clockwise (represented by a 1) and anticlockwise (represented by a -1)
        if dir != 1 and dir != -1:
            print("CANT ROTATE AS NO DIRECTION GIVEN")
            return -1
        else:
            match dir:
                case 1:
                    self.current_falling.rotate_clock(self.locked_blocks)
                case -1:
                    self.current_falling.rotate_anticlock(self.locked_blocks)

    def update(self):
        
        if self.current_falling.locking_next_step:
            self.lock_block()
        else:

            self.current_falling.grav(self.locked_blocks)
            
    def swap_hold(self):
        
        if self.hold.shape.is_none():
            #print(self.hold.shape.is_none())
            
            self.hold = self.current_falling
            self.current_falling = self.next_block
            self.next_block = self.generate_block()

        else:
            if self.can_hold:
                self.can_hold = False
                temp = self.hold
                self.hold = self.current_falling
                self.current_falling = temp
                self.current_falling.reset_to_init()
                self.check_loss()

    def generate_block(self):
        return Block((random.randint(2,5),2),random.choice(shapes_list))

    def init_block(self,bloc:Block):
        self.current_falling = bloc

    def debug_update_locked_blocks(self,new_list):
        self.locked_blocks = new_list
    def lock_block(self):
        self.falling_to_static(self.current_falling)
        self.current_falling = self.next_block
        self.next_block = self.generate_block()
        self.remove_lines()
        self.can_hold = True

        if self.check_loss():
            self.BREAK = True



    def drop_block(self):
        pos_list = self.current_falling.shape.get_rel_pos()
        min_dist = 1000000000
        for rel_pos in pos_list:
            abs_pos = sum_tuple(self.current_falling.pos,rel_pos)
            for i in range(18):
                if self.current_falling.collide_after_vect((0,i),self.locked_blocks):
                    if i-1 < min_dist:
                        min_dist = i-1
            
        self.current_falling.pos = sum_tuple(self.current_falling.pos,(0,min_dist))
        self.lock_block()
        self.score += ((i-2)*5)




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
        
    def update_score(self,line_amount):
        match line_amount:
            case 1:
                self.score += 100 * (1.5*(self.level-1))
            case 2:
                self.score += 300 * (1.5*(self.level-1))
            case 3:
                self.score += 1000 * (1.5*(self.level-1))
            case 4:
                self.score += 1600 * (1.5*(self.level-1))

    def remove_lines(self):
        lines_to_remove = self.find_lines(self.locked_blocks)
        if len(lines_to_remove) != 0:
            for line in lines_to_remove:
                self.update_pos_above(line)
                self.lines += 1
        
            self.update_score(len(lines_to_remove))
    
    def __str__(self):
        display = ""
        main_game_txt = ""
        next_block_txt = ""
        hold_txt = ""
        score_txt = ""
        for y in range(18):
            for x in range(8):
                if (x,y) in self.locked_blocks or (x,y) in self.current_falling.shape.calculate_pos_list(self.current_falling.pos):
                    main_game_txt += "▉▉"
                else:
                    main_game_txt += "  "
            
            main_game_txt += "\n"

        next_block_txt += "NEXT BLOCK\n\n"
        temp = self.next_block.shape.current_shape
        self.next_block.shape.current_shape = 0
        next_shape = self.next_block.shape.get_rel_pos()
        self.next_block.shape.current_shape = temp
        for i in range(4):
            for j in range(4):
                if (j-1,i-1) in next_shape:
                    next_block_txt += "▉▉"
                else:
                   next_block_txt += "  "

            next_block_txt += "\n"
        
        hold_txt += " HOLD\n\n"
        

        if not self.hold.shape.is_none():
            temp = self.hold.shape.current_shape
            self.hold.shape.current_shape = 0
            HOLD = self.hold.shape.get_rel_pos()
            self.hold.shape.current_shape = temp
            #print(self.hold.shape)
            for i in range(4):
                for j in range(4):
                    if (j-1,i-1) in HOLD:
                        hold_txt += "▉▉"
                    else:
                        hold_txt += "  "

                hold_txt += "\n"
        else:
            hold_txt += "\n" * 5
            
        score_txt += join_text(f" SCORE        \n\n   {int(round(self.score))}",f" LINES    \n\n   {self.lines}",3,0)
        top_right_txt = join_text(next_block_txt,hold_txt,3,0)
        right_side = top_right_txt + ("\n" * 2) + score_txt

        border = "|\n"*18
        main_game_with_borders = join_text(border,join_text(main_game_txt,border,0,0),0,0)
        display += "\n" *15


        display += join_text(main_game_with_borders,right_side,10,3)



        display += "\n" *5

        return display
    
class keyboard_listener:
    def __init__(self,listen) -> None:
        self.listen_list = listen
        self.held_down = []
        self.just_down = []
    
    def update(self):
        self.just_down.clear()
        for key in self.listen_list:
            if keyboard.is_pressed(key) and (not key in self.held_down):
                self.just_down.append(key)
                self.held_down.append(key)
            elif (not keyboard.is_pressed(key)) and (key in self.held_down):
                self.held_down.remove(key)
    def key_just_pressed(self,key):
        if key in self.just_down:
            return True
        else:
            return False





game = Game()
key_listen = keyboard_listener(["W","A","S","D","E"])

#game.debug_update_locked_blocks([(6,13),(7,14),(2,14),(6,14),(3,15),(7,15),(0,15),(6,15),(2,15),(0,16),(7,16),(6,16),(2,16),(3,16),(7,17),(2,17),(3,17),(4,17),(0,17),(6,17)]) # debug
game.init_block(game.generate_block())
game.hold = Block((-1,-1),Block_Shapes.NONE())
 #debug
#random.choice(shapes_list)

grav_time = 0.0
fps = 5
spf = 1/fps
redraw_time = 0.0
key_update_time = 0.0
previous_time = time.time()

while True:
    
    dt = time.time() - previous_time
    previous_time = time.time()
    
    redraw_time += dt
    grav_time += dt
    key_update_time += dt

    if key_update_time >= spf//2:
        
        key_listen.update()
        if key_listen.key_just_pressed("A"):
            game.move_block_left()
        if key_listen.key_just_pressed("D"):
            game.move_block_right()
        if key_listen.key_just_pressed("W"):
            game.rotate_block()
        if key_listen.key_just_pressed("S"):
            game.drop_block() # send current block down
        if key_listen.key_just_pressed("E"):
            game.swap_hold()
        key_update_time = 0.0

    if redraw_time >= spf:
        print(game)
        redraw_time = 0.0
        if grav_time >= 0.5:
            game.update()
            grav_time = 0.0
    
    if game.BREAK:
        print(game)
        break



print(f"You lost\n Your Final score: {game.score}")