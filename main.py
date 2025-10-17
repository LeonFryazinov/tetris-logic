
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

class block_shapes:

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
            self.current_shape = self.rot_amount


shapes_list = [block_shapes([[(0,0),(1,0),(0,1),(1,1)]]),#2x2 block
               block_shapes([[(0,-1),(0,0),(0,1),(0,2)],[(-1,0),(0,0),(1,0),(2,0)]]), #long stick
               block_shapes([[(0,-1),(0,0),(0,1),(1,0)],[(-1,0),(0,0),(0,1),(1,0)],[(0,-1),(0,0),(0,1),(-1,0)],[(-1,0),(0,0),(0,-1),(1,0)]]), #flat T block
               block_shapes([[(0,-1),(0,0),(0,1),(1,1)],[(1,0),(0,0),(-1,0),(-1,1)],[(-1,-1),(0,-1),(0,0),(0,1)],[(1,-1),(1,0),(0,0),(-1,0)]]), #L shape
               block_shapes([[(0,-1),(0,0),(0,1),(-1,1)],[(1,0),(0,0),(-1,0),(-1,-1)],[(1,-1),(0,-1),(0,0),(0,1)],[(1,1),(1,0),(0,0),(-1,0)]]), # reverse L Shape 
               block_shapes([[(-1,0),(0,0),(0,-1),(1,-1)],[(1,-1),(1,0),(0,0),(0,1)]]), # Stair (l->r)  _/-
               block_shapes([[(-1,-1),(0,-1),(0,0),(1,0)],[(0,-1),(0,0),(1,0),(1,1)]]), # Stair (r->l) -\_
               ]

class block:
    def __init__(self,init_pos,shape):
        self.pos = init_pos
        self.shape:block_shapes = shape
        self.gravity = (0,1)
    
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
    
    