import sys

PRINT_BEEJ=1
HALT=2


memory=[
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    HALT
]

pc=0

while True:
    command=memory[pc]
    if command==PRINT_BEEJ:
        print("Nrrj!")
        pc+=1
    elif command==HALT:
        sys.exit(0)
    else:
        print("I did not understand that command")