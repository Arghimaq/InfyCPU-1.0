Instruction_List = {
    # Memory
    "ST": 1,
    "LD": 2,
    "STI": 3,
    "LDI": 4,
    "SWP": 5,
    "COP": 6,
    
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
    
    "CMPei": 50,
    "CMPgi": 51,
    "CMPli": 52,
    
    # Control
    
    "JMP": 20,
    "JZ": 21,
    "JINP": 22,
    "JCMP": 23,
    
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
    "PRINT": 1111
}

from tkinter import filedialog as fd

filename = fd.askopenfilename(title="Choose ROM(txt file)", filetypes = (
        ('text files', '*.txt'),
    ))

print(Instruction_List)

decompiled = []
compiled = []



with open(filename, 'r') as f:
	for line in f:
		decompiled += line.split(';')[0].split()

def compile():
	global Instruction_List
	for instruction in decompiled:
		key = instruction.upper()
		if key in Instruction_List.keys():
			compiled.append(Instruction_List.get(key))
		else:
			compiled.append(instruction)

			
compile()

with open('ROM.txt', 'w') as f:
	for instruction in compiled:
		f.write(str(instruction) + '\n')

print(decompiled)
print(compiled)
