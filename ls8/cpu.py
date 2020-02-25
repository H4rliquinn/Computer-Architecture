"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram=[0b00000000]*256
        self.registers={0b00000000:0b00000000,
                        0b00000001:0b00000000
                        }
        self.PC=0b00000000   # * `PC`: Program Counter, address of the currently executing instruction
        self.MAR=0b00000000  # * `MAR`: Memory Address Register, holds the memory address we're reading or writing
        self.MDR=0b00000000  # * `MDR`: Memory Data Register, holds the value to write or the value just read
        self.IR=0b00000000   # * `IR`: Instruction Register, contains a copy of the currently executing instruction
        self.FL=0b00000000   # * `FL`: Flags, see below
        # self.R0=0b00000000
        # self.R1=0b00000000
        # self.R2=0b00000000
        # self.R3=0b00000000
        # self.R4=0b00000000
        # self.R5=0b00000000   # * R5 is reserved as the interrupt mask (IM)
        # self.R6=0b00000000   # * R6 is reserved as the interrupt status (IS)
        # self.R7=0b00000000   # * R7 is reserved as the stack pointer (SP)
        
    def ram_read(self):
        self.MDR=self.ram[self.MAR]

    def ram_write(self):
        self.ram[self.MAR]=self.MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b00011111, #Beej
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address+= 1


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
                self.PC+=1
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

                self.PC+=3
            elif self.IR==0b01000111:
                #PRN
                self.MAR=self.PC+1
                self.ram_read()
                operand_a=self.MDR 

                print(self.registers[operand_a])

                self.PC+=2             
            elif self.IR==0b00000001:
                sys.exit(0)
            else:
                print("I did not understand that command")
                sys.exit(1)
