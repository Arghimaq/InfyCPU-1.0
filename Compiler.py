ISA = {
    # Memory
    "ST": 1,
    "LD": 2,
    "STI": 3,
    "LDI": 4,
    "SWP": 5,
    "COP": 6,
    "PUSH": 7,
    "PUSHI": 8,
    "POP": 9,
    
    # ALU
    "ADD": 10,
    "SUB": 11,
    "MUL": 12,
    "DIV": 13,
    
    # ALUi
    "ADDI": 14,
    "SUBI": 15,
    "MULI": 16,
    "DIVI": 17,
    
    # Comparision
    
    "CMPEI": 50,
    "CMPGI": 51,
    "CMPLI": 52,
    "CMPE": 53,
    "CMPG": 54,
    "CMPL": 55,
    
    # Control
    
    "JMP": 20,
    "JZ": 21,
    "JINP": 22,
    "JCMP": 23,
    "CALL": 24,
    "CLLZ": 25,
    "CLLNP": 26,
    "CLLCMP": 27,
    "RET": 28,
    
    # Video
    
    "VST": 30,
    "VSTI": 31,
    "BLTI": 32,
    "BLT": 33,
    "BLTR": 34,
    
    # Input Output
    
    "INP": 40,
    
    # Malicious
    "HALT": 999,
    "PRINT": 1111,
    "VFRAME": 2222
    

        
}

labels = {
		
}

import sys
import os

def readfile(file):
	with open(file, 'r') as f:
		lines = [s.replace('\n', '') for s in f.readlines()]
		for i, line in enumerate(lines):
			lines[i] = line.split(';')[0]
		print(f"readed from file: {lines}")
		return lines

def pass1(instructions):
    labels = {}
    address = 0

    for instruction in instructions:
        instruction = instruction.strip()

        if not instruction:
            continue

        if instruction.startswith("$") and instruction.endswith(":"):
            label = instruction[1:-1]

            if label in labels:
                raise ValueError(f"Duplicate label: {label}")

            labels[label] = address
        else:
            address += 3
    print(labels)
    return labels
	
def remove_labels(rom):
	cleared = []
	for line in rom:
		try:
			if line[0] == '$':
				continue
			else:
				cleared.append(line)
		except IndexError:
			continue
	print(f"removed labels: {cleared}")
	return cleared
	
def split_rom(rom):
	decompiled = []
	for instruction in rom:
		for op in instruction.split():
			decompiled.append(op)
	print(f"split: {decompiled}")
	return decompiled

def pass2(rom):
	global ISA
	global labels
	compiled = []
	
	for instruction in rom:
		key = instruction.upper()
		if key in ISA.keys():
			compiled.append(ISA.get(key))
			print("got an opcode: " + key)
		
		else:	#If it starts with $
			if instruction[0] == '$':
				print("got a address: " + instruction)
				if instruction[1:] in labels.keys():
					print("instruction is in labels")
					compiled.append(labels[instruction[1:]])
			else:
				compiled.append(instruction)
	
	return compiled
	
	#Assembling to machine code
	
def compile(file):
	global labels
	
	try:
		machine_code = readfile(file)
	except FileNotFoundError:
		print(f"File '{file}' not found")
		return False
		
	labels = pass1(machine_code)
	
	machine_code = remove_labels(machine_code)
	machine_code = split_rom(machine_code)
	machine_code = pass2(machine_code)
	for i, instruction in enumerate(machine_code):
		try:
			machine_code[i] = int(instruction)
		except ValueError:
			machine_code[i] = instruction
	
	return machine_code
	
if len(sys.argv) < 2:
	pass
else:	
	print("got arguement!")

	with open(f"{os.path.splitext(sys.argv[1])[0]}.iexe", 'w') as f:
		for line in compile(sys.argv[1]):
			f.write(f"{line}\n")
		



