import sys

LDI = 0b10000010  # load 
PRN = 0b01000111  # print 
HLT = 0b00000001  # halt 
MUL = 0b10100010  # multiply
PUSH = 0b01000101  # add on
POP = 0b01000110  # pop off
CALL = 0b01010000  # call
RET = 0b00010001  # return
ADD = 0b10100000  # add
CMP = 0b10100111  # compare
JMP = 0b1010100  # seconds
JEQ = 0b1010101  # if equal
JNE = 0b1010110  # if not equal


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.memory = [0]*256
        self.register = [0]*8
        self.pc = 0  # program counter
        self.register[7] = 0b11110100  # 244
        self.fl = 0b00000000
        self.run_logic = True

    def load(self):                                             

        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                comment_split = line.split('#')                     # extract number 
                num = comment_split[0].strip()

                if num != "":                                       # print instruction
                    print(f'{num}')                                 
                    value = int(num, 2)                             # save number if it is there
                    self.memory_write(value, address)
                    address += 1



    def alu(self, op, register_a, register_b):
        """
        ALU operations. (arithmetic/logic unit)
        """

        if op == "ADD":
            self.register[register_a] += self.register[register_b]
        elif op == "MUL":
            self.register[register_a] *= self.register[register_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.memory_read(self.pc),
            self.memory_read(self.pc + 1),
            self.memory_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

    def memory_read(self, MAR):
        return self.memory[MAR]

    def memory_write(self, MDR, MAR):
        self.memory[MAR] = MDR
        return

    def instruction_switch_run(self, IR, operand_a, operand_b):
        if IR == LDI:
            self.register[operand_a] = operand_b
            self.pc += 3  
        elif IR == PRN:
            print(self.register[operand_a])
            self.pc += 2
        elif IR == MUL:
            self.alu("MUL", operand_a, operand_b)
            self.pc += 3
        elif IR == HLT:
            self.run_logic = False
        elif IR == PUSH:
            value = self.register[operand_a]
            self.register[7] -= 1
            self.memory_write(value, self.register[7])
            self.pc += 2
        elif IR == POP:
            self.register[operand_a] = self.memory_read(self.register[7])
            value = self.register[operand_a]
            self.register[7] += 1
            self.pc += 2
        elif IR == CALL:
            call_address = self.pc + 2
            self.register[7] -= 1
            self.memory_write(call_address, self.register[7])
            self.pc = self.register[operand_a]
        elif IR == RET:
            ret_address = self.register[7]
            self.pc = self.memory_read(ret_address)
            self.register[7] += 1
        elif IR == ADD:
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3
        elif IR == CMP:                                                 # CMP for SPRINT
            if self.register[operand_a] < self.register[operand_b]:
                self.fl = 0b00000100
            elif self.register[operand_a] > self.register[operand_b]:
                self.fl = 0b00000010
            elif self.register[operand_a] == self.register[operand_b]:
                self.fl = 0b00000001
            self.pc += 3
        elif IR == JMP:                                                 # JMP for SPRINT
            self.pc = self.register[operand_a]
        elif IR == JEQ:                                                 # JEQ for sprint
            if (self.fl & 0b00000001) == 1:
                self.pc = self.register[operand_a]
            else:
                self.pc += 2
        elif IR == JNE:                                                 # JNE for sprint
            if (self.fl & 0b00000001) == 0:
                self.pc = self.register[operand_a]
            else:
                self.pc += 2
        else:
            print(f"{IR} - command is not available")
            sys.exit()

    def run(self):
        while self.run_logic:                                           # instructions
            IR = self.memory_read(self.pc)
            operand_a = self.memory_read(self.pc + 1)                   # read int in
            operand_b = self.memory_read(self.pc + 2)                   # receive instruction do task
            self.instruction_switch_run(IR, operand_a, operand_b)


# Test with : 'python ls8.py sctest.ls8'