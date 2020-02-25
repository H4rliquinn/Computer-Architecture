import sys

PRINT_BEEJ=1
HALT=2
PRINT_NUM=3
SAVE=4 #Save to register
PRINT_REGISTER=5 #Print val in registers
ADD=6 #Add 2 registers

memory=[
    # PRINT_BEEJ,
    # SAVE,
    # 65,
    # 2,
    # SAVE,
    # 20,
    # 3,
    # ADD,
    # 2,
    # 3,
    # PRINT_REGISTER,
    # 2,
    # PRINT_NUM,
    # 1,
    # PRINT_NUM,
    # 12,
    # PRINT_BEEJ,
    # PRINT_BEEJ,
    # PRINT_NUM,
    # 37,
    # PRINT_BEEJ,
    # HALT
0]*256

# print(sys.argv)
mem_pointer=0
if len(sys.argv)!=2:
    print("Error: No Filename")
    sys.exit(1)
try:
    with open(sys.argv[1]) as f:
        for line in f:
            # print(line)
            comment_split=line.split("#")
            value=comment_split[0].strip()
            if value=='':
                continue
            num=int(value)
            print(f"{num:08}:{num}")
            memory[mem_pointer]=num
            mem_pointer+=1
    print("MEM",memory)
except FileNotFoundError:
    print("File Not Found")
    sys.exit(2)

register=[0]*8

pc=0

while True:
    command=memory[pc]
    if command==PRINT_BEEJ:
        print("Beej!")
    elif command==PRINT_NUM:
        num=memory[pc+1]
        print(num)
        pc+=1
    elif command==HALT:
        sys.exit(0)
    elif command==SAVE:
        num=memory[pc+1]
        reg = memory[pc+2]
        register[reg]=num
        pc+=2
    elif command==PRINT_REGISTER:
        reg=memory[pc+1]
        print(register[reg])
        pc+=1
    elif command==ADD:
        reg_a=memory[pc+1]
        reg_b=memory[pc+2]
        register[reg_a]+=register[reg_b]
        pc+=2
    else:
        print("I did not understand that command")
        sys.exit(1)
    pc+=1