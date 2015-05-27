#python3
from sys import argv
from os import path
from re import sub

memoryCounter = 16

symbolTable = {
	"SCREEN":int("4000",16), 
	"SP":0,
	"LCL":1,
	"ARG":2,
	"THIS":3,
	"THAT":4,
	"KBD":int("6000",16), 
}

jmpTable = {
	"null":"000",
	"JGT":"001",
	"JEQ":"010",
	"JGE":"011",
	"JLT":"100",
	"JNE":"101",
	"JLE":"110",
	"JMP":"111"
}

cmdTable = {
	"0":"101010",
	"1":"111111",
	"-1":"111010",
	"D":"001100",
	"A":"110000",
	"!D":"001101",
	"!A":"110001",
	"-D":"001111",
	"-A":"110011",
	"D+1":"011111",
	"A+1":"110111",
	"D-1":"001110",
	"A-1":"110010",
	"D+A":"000010",
	"D-A":"010011",
	"A-D":"000111",
	"D&A":"000000",
	"D|A":"010101" 
}

def buildDict(lines):
	for x in range(0,15):
		symbolTable["R"+str(x)] = x

	lineCounter = 0
	for line in lines:
		if line[0] == '(' :
			foo = 1
			line = line.strip('()')
			if line not in symbolTable:
				symbolTable[line] = lineCounter

		else:
			lineCounter += 1

def IToXbitBin(y, bit):
	ret = bin( int(y) )[2:]
	x = bit - len(ret)
	while x > 0 :
		ret = '0' + ret
		x -= 1
	return ret

def parseA(line):
	ret = "0"
	if line[1].isdigit():
		ret += IToXbitBin(line[1:], 15)
	else:
		if line[1:] in symbolTable.keys():
			value = symbolTable[line[1:]]
			ret += IToXbitBin(value, 15)
		else:
			memoryCounter = 0
			while( memoryCounter in symbolTable.values() and memoryCounter < int("4000",16) ):
				memoryCounter += 1
			symbolTable[ line[1:] ] = memoryCounter
			ret += IToXbitBin(memoryCounter,15)
				
	
	return ret + '\n'

def parseDest(i):

	dest = ""
	if 'A' in i:
		dest += '1'
	else:
		dest += '0'

	if 'D' in i:
		dest += '1'
	else:
		dest += '0'

	if 'M' in i:
		dest += '1'
	else:
		dest += '0'
	return dest

def parseC(line):
	ret = "111"
	dest = "000"
	jmp = "000"
	a = "0"

	if ';' in line:
		sp_line = line.split(';')
		jmp = jmpTable[sp_line[1]]
		line = sp_line[0]

	if '=' in line:
		sp_line = line.split('=')
		dest = parseDest( sp_line[0] )
		if 'M' in sp_line[1]:
			a = "1"
		cmd_line = sp_line[1].replace("M","A")
		cmd = cmdTable[ cmd_line ]

	else:
		cmd = cmdTable[ line ]


	return ret + a + cmd + dest + jmp + '\n'

def parse(line):
	if line[0] == '@':
		return parseA(line)
	else:
		return parseC(line)

# start!

if len(argv) > 1:
	in_file = argv[1]
	output_name = path.splitext(in_file)[0] + ".hack"
	if len(argv) > 2: 
		output_name = argv[2]
else:
	print(	"Input format wrong!\n"+
			"Correct input format (output optional): \n"+
			"python3 assembler.py input (output)")
	exit(1)
	

file_input = open (in_file, "r")

lines = file_input.readlines()

lines = map (lambda line: sub(r"//.*","", line), lines) #clear comments
lines = list ( filter(None, map(str.strip, lines) ) ) #clear whitespace & empty lines
file_input.close()
buildDict(lines)

lines = filter(lambda line: not(line.startswith("(")), lines) #clear lables

out_lines = list( map(parse, lines) )

file_output = open( output_name, "w")
file_output.writelines( out_lines )
file_output.close()
print ( "Done!" )


	









