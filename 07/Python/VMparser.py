from sys import argv
from os import path
from re import sub

counter = -1

def gen_gen(string):
	def gen():
		x = 0
		while (True):
			yield string.format(x)
			x = x + 1
	return gen

primitves = {"add","sub","neg","and","or","not"}
primitves_c = {"eq","gt","lt"}
memoryCMDs = {"push"}

functionTable = {
#tested: add, sub, neg, and, eq 
	"add": "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n",
	"sub": "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n",
	"neg": "@SP\nA=M-1\nM=-M\n",

	"eq" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@EQ_End{0}\nD;JEQ\n@SP\nA=M-1\nM=0\n(EQ_End{0})\n",
	"gt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@GT_End{0}\nD;JGT\n@SP\nA=M-1\nM=0\n(GT_End{0})\n",
	"lt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@LT_End{0}\nD;JLT\n@SP\nA=M-1\nM=0\n(LT_End{0})\n",

	"and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n",
	"or" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n",
	"not": "@SP\nA=M-1\nM=!M\n",

	"push"			: "@SP\nAM=M+1\nA=A-1\nM=D\n",
	"push_constant"	: "@{0}\nD=A\n",
	"push_local"	: "@{0}\nD=A\n@LCL\nA=M+D\nD=M\n",
	"push_argument"	: "@{0}\nD=A\n@ARG\nA=M+D\nD=M\n",
	"push_this"		: "@{0}\nD=A\n@THIS\nA=M+D\nD=M\n",
	"push_that"		: "@{0}\nD=A\n@THAT\nA=M+D\n\nD=M\n",
	"push_temp"		: "@{0}\nD=A\n@5\nA=A+D\n\nD=M\n",
	"push_pointer"	: "@{0}\nD=A\n@THIS\nA=A+D\nD=M\n",
	"push_static"	: "@{0}\nD=A\n@16\nA=A+D\nD=M\n",

	"pop"			: "@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
	"pop_local"		: "@LCL\nD=M\n@{0}\nD=A+D\n@R13\nM=D\n",
	"pop_argument"	: "@ARG\nD=M\n@{0}\nD=A+D\n@R13\nM=D\n",
	"pop_this"		: "@THIS\nD=M\n@{0}\nD=A+D\n@R13\nM=D\n",
	"pop_that"		: "@THAT\nD=M\n@{0}\nD=A+D\n@R13\nM=D\n",
	"pop_temp"		: "@5\nD=A\n@{0}\nD=A+D\n@R13\nM=D\n",
	"pop_pointer"	: "@THIS\nD=A\n@{0}\nD=A+D\n@R13\nM=D\n"

}

def functionTableWrapper(cmd):
	cmd = cmd.split()
	if cmd[0] in primitves:

		return functionTable[cmd[0]]
	elif cmd[0] in primitves_c:
		global counter
		counter += 1
		return functionTable[cmd[0]].format(counter)
	elif cmd[0] == "push":
		return functionTable[cmd[0]+"_"+cmd[1]].format(int(cmd[2])) + functionTable[cmd[0]]
	elif cmd[0] == "pop":
		return functionTable[cmd[0]+"_"+cmd[1]].format(int(cmd[2])) + functionTable[cmd[0]]


def parse(string):
	return( functionTableWrapper(string) )

#start!
if len(argv) > 1:
	in_file = argv[1]
	output_name = path.splitext(in_file)[0] + ".asm"
	if len(argv) > 2: 
		output_name = argv[2]
else:
	print(	"Input format wrong!\n"+
			"Correct input format (output optional): \n"+
			"python3 VMparser.py input (output)")
	exit(1)
	

file_input = open (in_file, "r")

lines = file_input.readlines()

lines = map (lambda line: sub(r"//.*","", line), lines) #clear comments
lines = list ( filter(None, map(str.strip, lines) ) ) #clear whitespace & empty lines
file_input.close()

out_lines = list( map(parse, lines) )

#print(out_lines)

file_output = open( output_name, "w")
file_output.writelines( out_lines )
file_output.close()
print ( "Done!" )
