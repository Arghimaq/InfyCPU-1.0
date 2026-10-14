import time
import json

#Initialize GPU

import GraphicalProcessor as GPU

GPU.load_data()

GPU.initialize()
VRAM = [0] * (GPU.Screen_Length * GPU.Screen_Width)

Blitter_Register = 0

#Sizes

with open('settings.json', 'r') as f:
	settings = json.load(f)
	

Instruction_Size = 3
ROM_SIZE = settings.get("ram_size")
RAM_SIZE = settings.get("rom_size")
VRAM_Base_Address = 129

#Initialize RAM and ROM

ROM = [0] * (Instruction_Size * ROM_SIZE)
RAM = [0] * RAM_SIZE

#Initialize Registers and PC

Accumulator = 0

Registers = {
	0: 0,	#A
	1: 0,	#B
	2: 0,	#C
	3: 0,	#D
	4: 0,	#E
	5: 0,	#F
	6: 0,	#G
	7: 0,	#H
	8: 0,	#0
	9: 0,
	10: 0,
	11: 0,
	12: 0,
	13: 0,
	14: 0,
	15: 0,
	16: 0,
} 

PC = 0

#Initialize flags

Machine_State = True

Jump_Flag = False
Zero_Flag = False
Input_Flag = False
CMP_Flag = False

#Functions

def get_rom():
	global ROM
	with open ("ROM.txt",'r') as f:
		
		content = f.read().split()
		
		print(f"Got ROM.txt: {content}")
		#Convert into intergers
		i = 0
		for instruction in content:
			content[i] = int(instruction)
			i+=1
		print(f"Converted into intergers: {content}")
			
		#Putting into ROM
		leftover = len(ROM) - len(content)
		if leftover >= 0:
			ROM = content
			for x in range(leftover):
				ROM.append(0)
		else:
			print("ROM.txt exeeds ROM size!")
			
def fetch():
	global ROM
	global PC
	global Machine_State
	try:
		return ROM[PC], ROM[PC+1], ROM[PC+2]
	except IndexError:
		print("Reached ROM end")
		Machine_State = False

def run():
	global RAM
	global Registers
	
	global Machine_State
	global Zero_Flag
	global Jump_Flag
	global Input_Flag
	global CMP_Flag
	
	global Blitter_Register
	
	global PC
	
	opcode, operand1, operand2 = fetch()
	
#Memory-----------------------------------------------------------------
	
	if opcode == 1:		    #ST. Store register value into RAM address
		RAM[operand1] = Registers[operand2]
	
	elif opcode == 2:		#LD. Load RAM value from address into register
		Registers[operand1] = RAM[operand2]
	
	elif opcode == 3:		#STI. Store value into RAM address
		RAM[operand1] = operand2
		
	elif opcode == 4:		#LDI. Load value into register
		Registers[operand1] = operand2
	
	elif opcode == 5:		#SWP. Swap register values
		Registers[operand1], Registers[operand2] = Registers[operand2], Registers[operand2]
		
	elif opcode == 6:		#COP. Copy register value
		Registers[operand2] = Registers[operand1]
		
#ALU--------------------------------------------------------------------

	elif opcode == 10:		#ADD. Add a register's value to a register
		Registers[operand1]+=Registers[operand2]
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
	
	elif opcode == 11:		#SUB. Subtract a register's value with a register
		Registers[operand1]-=Registers[operand2]
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
			
	elif opcode == 12:		#MUL. Multiply a register's value with a register
		Registers[operand1]*=Registers[operand2]
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
				
	elif opcode == 13:		#DIV. Divide a register's value with a register
		Registers[operand1]/=Registers[operand2]
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False	
			
	elif opcode == 14:		#ADDi. Add a register's value to a register
		Registers[operand1]+=operand2
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
				
	elif opcode == 15:		#SUBi. Subtract a register's value with a register
		Registers[operand1]-=operand2
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
					
	elif opcode == 16:		#MULi. Multiply a register's value with a register
		Registers[operand1]*=operand2
		if Registers[operand1] == 0:
			Zero_Flag = True
		else:
			Zero_Flag = False
				
	elif opcode == 17:		#DIVi. Divide a register's value with a register
		Registers[operand1]/=operand2
		
#Control----------------------------------------------------------------

	elif opcode == 20:		#JMP. Jump.
		PC = operand1
		Jump_Flag = True
	
	elif opcode == 21:		#JZ. Jump if last operation was zero. if operand1 is not zero, inverse
		if operand2 == 0:
			if Zero_Flag:
				PC = operand1
				Jump_Flag = True
		else:
			if not Zero_Flag:
				PC = operand1
				Jump_Flag = True
				
	elif opcode == 22:		#JINP. Jump if Input Flag is on. if operand1 is not zero, inverse
		if operand2 == 0:
			if Input_Flag:
				PC = operand1
				Jump_Flag = True
		else:
			if not Input_Flag:
				PC = operand1
				Jump_Flag = True
	
	elif opcode == 23:		#JCMP. Jump if Compare flag is true. if operand1 is not zero, inverse
		if operand2 == 0:
			if CMP_Flag:
				PC = operand1
				Jump_Flag = True
		else:
			if not CMP_Flag:
				PC = operand1
				Jump_Flag = True
		
#Video Memory-----------------------------------------------------------

	elif opcode == 30:		#VST.	Store register value into VRAM address
		VRAM[Registers[operand1]] = Registers[operand2]
	
	elif opcode == 31:		#VSTI. Store value into VRAM address
		VRAM[Registers[operand1]] = operand2
		
	elif opcode == 32:		#BLTi. Store calculated x y position from blitter into blitter register
		Blitter_Register = GPU.blitter(operand1, operand2)
		
	elif opcode == 33:		#BLT. Use blitter on Registers
		Blitter_Register = GPU.blitter(Registers[operand1], Registers[operand2])
		
	elif opcode == 34:		#BLTr. Load blitter value into register
		Registers[operand1] = Blitter_Register
	
#IO---------------------------------------------------------------------

	elif opcode == 40:		#INP. Listen for input without blocking
		keyboard = GPU.listen()
		if keyboard is not None:
			Input_Flag = True
			Registers[operand1] = keyboard
			print("Received input")
		else:
			Input_Flag = False
			
#Comparision------------------------------------------------------------

	elif opcode == 50:		#CMPEi. Turn on compare flag if equal
		if Registers[operand1] == operand2:
			CMP_Flag = True
		else:
			CMP_Flag = False
	
	elif opcode == 51:		#CMPGi. Turn on compare flag if greater
		if Registers[operand1] > operand2:
			CMP_Flag = True
		else:
			CMP_Flag = False
			
	elif opcode == 51:		#CMPLi. Turn on compare flag if greater
		if Registers[operand1] < operand2:
			CMP_Flag = True
		else:
			CMP_Flag = False

#Malicious--------------------------------------------------------------

	elif opcode == 999:		#Halt
		Machine_State = False
		
	elif opcode == 1111:	#Print
		print(Registers[operand1])
	
def tickCPU():
	global PC
	global Jump_Flag
	run()
	if not Jump_Flag:	
		PC+=3
	else:
		Jump_Flag = False

def tickGPU():
	global VRAM
	global Machine_State
	GPU.update(VRAM)
	if GPU.check_quit():
		Machine_State = False
	
def cycle():
	tickCPU()
	tickGPU()
	

get_rom()

print("Running...")
	
while Machine_State:
	cycle()
			
print("Halted")
#Final Results

print(f"""Final Results:
	
	ROM = {ROM}
	
	RAM = {RAM}""")

print("\nRegisters:")
	
for key in Registers:
	print(f"{key}: {Registers[key]}")
