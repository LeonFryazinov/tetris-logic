

#debug terminal based ui,


test_text =  "hello\nHow do you do"
test_text2 = "                   \n                   \n          ▉▉       \n          ▉▉       \n          ▉▉       \n          ▉▉       \n                   \n                   \n                   \n                   \n                   \n                   \n                   \n            ▉▉     \n    ▉▉      ▉▉▉▉   \n▉▉  ▉▉▉▉    ▉▉▉▉   \n▉▉  ▉▉▉▉    ▉▉▉▉   \n▉▉  ▉▉▉▉▉▉  ▉▉▉▉\n"
test_text_3 = "NEXT BLOCK\n\n▉▉▉▉    \n  ▉▉▉▉  \n        \n        \n"
hold_text = "HOLD\n\n    ▉▉            \n    ▉▉▉▉          \n    ▉▉\n"

test_text_4 = "\n SCORE          \n\n  0    \n\n LINES\n\n 0"

#print(test_text2 + test_text_3)
#print(test_text2.split("\n"))


def join_text(a:str,b:str,x_offset=5,y_offset=0):
    split_a = a.split("\n")
    split_b = b.split("\n")
    combined_string = ""
    max_len_a = 0
    for line in split_a:
        if len(line) > max_len_a:
            max_len_a = len(line)
    print(max_len_a)
    for i in range(len(split_a)): #(len(split_a) if len(split_a) > len(split_b)+y_offset else len(split_b)+y_offset)
        combined_string += split_a[i]
        combined_string += " " * ((max_len_a-len(split_a[i]))+x_offset)
        print(len(split_a[i])-max_len_a)

        if i - y_offset >= 0 and i-y_offset < len(split_b):
            combined_string += split_b[i-y_offset]
        
        combined_string += "\n"
    
    return combined_string



test_text = "hello\nHow do you do"
test_text2 = "AAAAAAAAA\n1"

print(join_text(test_text,test_text2,3,0))

        

