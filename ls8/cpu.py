"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram=[0b00000000]*256
        self.PC=0b00000000   # * `PC`: Program Counter, address of the currently executing instruction
        self.MAR=0b00000000  # * `MAR`: Memory Address Register, holds the memory address we're reading or writing
        self.MDR=0b00000000  # * `MDR`: Memory Data Register, holds the value to write or the value just read
        self.IR=0b00000000   # * `IR`: Instruction Register, contains a copy of the currently executing instruction
        self.FL=0b00000000   # * `FL`: Flags, see below
        R0=0b00000000
        R1=0b00000001
        R2=0b00000010
        R3=0b00000011
        R4=0b00000100
        R5=0b00000101   # * R5 is reserved as the interrupt mask (IM)
        R6=0b00000110   # * R6 is reserved as the interrupt status (IS)
        R7=0b00000111   # * R7 is reserved as the stack pointer (SP)
        self.registers=[0]*8
        
    def ram_read(self):
        self.MDR=self.ram[self.MAR]

    def ram_write(self):
        self.ram[self.MAR]=self.MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        #COMMANDS
        HLT=0b00000001
        BEEJ=0b00011111
        LDI=0b10000010
        PRN=0b01000111
        MUL=0b10100010

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b00011111, # Beej
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # program2 = [
        #     BEEJ,
        #     LDI,
        #     R0,
        #     8,
        #     PRN,
        #     R0,
        #     HLT,
        # ]
        
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
                    # print(value)
                    if value=='':
                        continue

                    num=int(value,2)
                    # num=bin(num)
                    # print(f"{num:08}:{num}")
                    self.ram[mem_pointer]=num
                    mem_pointer+=1
            # print("MEM",self.ram)
        except FileNotFoundError:
            print("File Not Found")
            sys.exit(2)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address+= 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            self.IR=self.ram[self.PC]
            # print("IR",self.IR)
            if self.IR==0b00011111:
                #BEEJ
                print("Beej!")
            elif self.IR==0b10000010:
                #LDI
                self.MAR=self.PC+1
                self.ram_read()
                # print("RAM",self.PC,self.ram[self.PC],self.ram[self.PC+1],self.ram[self.PC+2])
                operand_a=self.MDR
                self.MAR=self.PC+2
                self.ram_read()
                operand_b=self.MDR
                self.registers[operand_a]=operand_b
                # print("REG",operand_a,operand_b,self.registers)
            elif self.IR==0b01000111:
                #PRN
                self.MAR=self.PC+1
                self.ram_read()
                operand_a=self.MDR 
                print(self.registers[operand_a])
            elif self.IR==0b10100010:
                #MUL
                self.MAR=self.PC+1
                self.ram_read()
                operand_a=self.MDR 
                self.MAR=self.PC+2
                self.ram_read()
                operand_b=self.MDR 
                self.registers[operand_a]=self.registers[operand_a]*self.registers[operand_b]
            elif self.IR==0b00000001:
                sys.exit(0)
            else:
                print("I did not understand that command")
                sys.exit(1)
            self.PC+=(self.IR>>6)+1
