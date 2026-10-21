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
    "POP": 9
    
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

def readfile(file):
	with open(file, 'r') as f:
		lines = [s.replace('\n', '') for s in f.readlines()]
		for i, line in enumerate(lines):
			lines[i] = line.split(';')[0]
			
		return lines

def pass1(rom):
	d = {}
	address = 0
	for instruction in rom:
		try:
			if instruction[0] == '$':	#Label prefix
				full = instruction[1:-1]
				d.update({full: address})
			address+=3 
		except IndexError:
			continue
	return d
	
def remove_labels(rom):
	cleared = []
	for line in rom:
		try:
			if line[0] == '$':
				cleared.append("0 0 0")
			else:
				cleared.append(line)
		except IndexError:
			continue
	return cleared
	
def split_rom(rom):
	decompiled = []
	for instruction in rom:
		for op in instruction.split():
			decompiled.append(op)
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
		machine_code[i] = int(instruction)
	
	return machine_code
	

