""""
Colin Weinshenker
9/15/2017

This program acts as an assembler for the HACK assembly language
used in the Coursera nand2tetris course
"""

import sys



def is_A(instruction):
    return instruction[0] == "@"

def is_label(instruction):
    return instruction[0] == "("

def is_C(instruction):
    return (not is_A(instruction)) and (not is_label(instruction))

def is_assignment(instruction):
    return "=" in instruction

def is_jump(instruction):
    return ";" in instruction

def get_assigning(instruction):
    return instruction.split("=")[1]

def get_jump(instruction):
    return instruction.split(";")[1]

def is_variable(instruction):
    try:
        return is_A(instruction) and not (type(instruction[1:]) is int)
    except Exception as e:
        return true


def load_file(fn):
    with open(fn, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            beg=line.find("//")
            if beg != -1:
                lines[i] = line[:beg]
        #lines = list(filter(lambda x : x.split("//"), lines))
        lines = list(map(lambda x : x.split(), lines))
        lines = list(map(lambda x : "".join(x), lines))
        lines = list(filter(lambda x: x != '', lines))
    print(lines)
    return lines


def preload_symbols():
    symbols = {}
    symbols["SP"] = 0
    symbols["LCL"] = 1
    symbols["ARG"] = 2
    symbols["THIS"] = 3
    symbols["THAT"] = 4
    symbols["SCREEN"] = 16384
    symbols["KBD"] = 24576
    for i in range(16):
        symbols["R" + str(i)] = i
    return symbols

def label_symbols(symbols, lines):
    i=0
    for _, instruction in enumerate(lines):
        if is_label(instruction):
            sym = instruction[1:-1]
            symbols[sym] = i
        else:
            i = i + 1
    return symbols

def variable_symbols(symbols, lines):
    cur_reg = 16
    for i, line in enumerate(lines):
        if is_variable(line):
            sym = line[1:]
            try:
                if int(sym) <= 15:
                    symbols[sym] = symbols["R" + str(sym)]
            except ValueError as e:
                if sym not in symbols:
                    symbols[sym] = cur_reg
                    cur_reg += 1
    return symbols


def assemble_A(symbols, instruction):
    sym = instruction[1:]
    try:
        binary = bin(symbols[sym])[2:]
    except KeyError as e:
        binary = bin(int(sym))[2:]
    binary = "0" * (16 - len(binary)) + binary
    print (sym, binary)
    return binary


def decode_dest(instruction):
    dest_table = {"null": "000",\
                "M"   : "001",\
                "D"   : "010",\
                "MD"  : "011",\
                "A"   : "100",\
                "AM"  : "101",\
                "AD"  : "110",\
                "AMD" : "111"}
    if not is_assignment(instruction):
        return dest_table["null"]
    else:
        dest = instruction.split("=")[0]
        return dest_table[dest]


def decode_jump(instruction):
    jump_table={"null" : "000",\
                "JGT"  : "001",\
                "JEQ"  : "010",\
                "JGE"  : "011",\
                "JLT"  : "100",\
                "JNE"  : "101",\
                "JLE"  : "110",\
                "JMP"  : "111"}
    if not is_jump(instruction):
        return jump_table["null"]
    else:
        return jump_table[get_jump(instruction)]


def decode_a(instruction):
    if is_assignment(instruction):
        if "M" in get_assigning(instruction):
            return "1"
        return "0"
    elif "M" in instruction:
        return "1"
    return "0"

def decode_comp(instruction, a_bit):
    comp_table = {"0" : "101010",\
                  "1" : "111111",\
                  "-1": "111010",\
                  "D" : "001100",\
                  "A" : "110000",\
                  "!D": "001101",\
                  "!A": "110001",\
                  "-D": "001111",\
                  "-A": "110011",\
                  "D+1":"011111",\
                  "A+1":"110111",\
                  "D-1":"001110",\
                  "A-1":"110010",\
                  "D+A":"000010",\
                  "D-A":"010011",\
                  "A-D":"000111",\
                  "D&A":"000000",\
                  "D|A":"010101"}
    if is_assignment(instruction):
        comp = get_assigning(instruction)
        if a_bit == "1":
            comp=comp.replace("M", "A")
        return comp_table[comp]
    elif is_jump(instruction) :
        return comp_table[instruction.split(";")[0]]
    else:
        return comp_table[instruction]



def assemble_C(instruction):
    prefix = "111"
    a_bit = decode_a(instruction)
    comp = decode_comp(instruction, a_bit)
    destination = decode_dest(instruction)
    jump = decode_jump(instruction)
    return prefix + a_bit + comp + destination + jump


def assemble(symbols, lines):
    assembly = []
    for instruction in lines:
        if is_A(instruction):
            assembly.append(assemble_A(symbols, instruction))
        elif is_C(instruction):
            assembly.append(assemble_C(instruction))
    print(assembly)
    return assembly



if __name__=="__main__":
    fn = sys.argv[1]
    lines = load_file(fn)
    symbols=preload_symbols()
    symbols=label_symbols(symbols, lines)
    symbols=variable_symbols(symbols, lines)
    print(symbols)
    assembly = assemble(symbols, lines)
    with open(fn[:-4] + "Out.asm", "w") as f:
        for line in assembly:
            f.write(line)
            f.write("\n")
