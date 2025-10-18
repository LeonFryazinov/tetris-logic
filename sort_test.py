#File created to help testing with sorting the "locked blocks" from game class in main 
import random

def sum_tuple(a:tuple,b:tuple):
    return (a[0]+b[0],a[1]+b[1])
def sub_tuple(a:tuple,b:tuple):
    return (a[0]-b[0],a[1]-b[1])
def mult_tuple(a:tuple,b:float):
    return (a[0]*b,a[1]*b)
def div_tuple(a:tuple,b:float):
    return (a[0]/b,a[1]/b)


#set up for a list that would be expected to show up.

test_list = []


for i in range(50):
    poss_pos = (random.randint(0,7),random.randint(5,17))
    if not poss_pos in test_list:
        test_list.append(poss_pos)


#print(test_list)
all_down = False

while not all_down:
    check_amount = 0
    for idx,pos in enumerate(test_list):

        new_pos = sum_tuple(pos,(0,1))
        if (not new_pos in test_list) and (new_pos[1] != 18):
            test_list[idx] = new_pos
            check_amount += 1
    if check_amount == 0:
        all_down = True
        continue



#print(test_list)


#sorting

def sort_pos(pos_list):
    print(pos_list)
    if len(pos_list) == 1:
        print("reached base case")
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

sorted_test_list = sort_pos(test_list)
print(sorted_test_list)


#detecting lines
def find_lines(pos_list):
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

print(find_lines(sorted_test_list))           



