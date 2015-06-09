from sys import argv
from os import path
from re import sub

counter = -1

currF = ""

primitves = {"add","sub","neg","and","or","not"}
primitves_c = {"eq","gt","lt"}
memOps = {"push", "pop" }
jmpOps = {"label", "goto", "if-goto"}

functionTable = {
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
	"push_that"		: "@{0}\nD=A\n@THAT\nA=M+D\nD=M\n",
	"push_temp"		: "@{0}\nD=A\n@5\nA=A+D\nD=M\n",
	"push_pointer"	: "@{0}\nD=A\n@THIS\nA=A+D\nD=M\n",
	"push_static"	: "@{0}\nD=A\n@16\nA=A+D\nD=M\n",

	"pop"			: "\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
	"pop_local"		: "@LCL\nD=M\n@{0}",
	"pop_argument"	: "@ARG\nD=M\n@{0}",
	"pop_this"		: "@THIS\nD=M\n@{0}",
	"pop_that"		: "@THAT\nD=M\n@{0}",
	"pop_temp"		: "@5\nD=A\n@{0}",
	"pop_pointer"	: "@THIS\nD=A\n@{0}",
	"pop_static"	: "@16\nD=A\n@{0}",

	"label"			: "({0})\n",
	"goto"			: "@{0}\n0;JMP\n",
	"if-goto"		: "@SP\nAM=M-1\nD=M\n@{0}\nD;JNE\n",

	"call"			: """
@{0}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D
@LCL\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D
@ARG\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D
@THIS\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D
@THAT\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D
@{1}\nD=A\n@5\nD=D-A\n@SP\nA=M\nD=A-D\n@ARG\nM=D
@Sp\nA=M\nD=M\n@LCL\nM=D
@{2}\n0;JMP
({0})\n
""",

	"return"		: """
@LCL\nD=M\n@R13\nM=D
@5\nD=A\n@R13\nD=M-D\n@R14\nM=D
@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D
@ARG\nD=M\n@SP\nM=D+1
@R13\nAM=M-1\nD=M\n@THAT\nM=D
@R13\nAM=M-1\nD=M\n@THIS\nM=D
@R13\nAM=M-1\nD=M\n@ARG\nM=D
@R13\nAM=M-1\nD=M\n@LCL\nM=D
@R14\nA=M\n0;JMP\n"""
}


def parseLine(cmd):
	global currF
	cmd = cmd.split()

	if cmd[0] in primitves:
		return functionTable[cmd[0]]

	elif cmd[0] in primitves_c:
		global counter
		counter += 1
		return functionTable[cmd[0]].format(counter)

	elif cmd[0] in memOps:
		return functionTable[ cmd[0]+"_"+cmd[1] ].format( int(cmd[2]) ) + functionTable[cmd[0]]

	elif cmd[0] == "function":
		currF = cmd[1]
		pushes = ""
		for i in range( 0, int(cmd[2]) ):
			pushes += parseLine("push constant 0")
		return functionTable["label"].format(currF) + pushes

	elif cmd[0] in jmpOps:
		return functionTable[cmd[0]].format(currF + '$' + cmd[1] )

	elif cmd[0] == "call":
		return functionTable[ cmd[0] ].format(currF, cmd[2], cmd[1])

	elif cmd[0] == "return":
		return functionTable["return"]


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

out_lines = list( map(parseLine, lines) )

#print(out_lines)

file_output = open( output_name, "w")
file_output.writelines( out_lines )
file_output.close()
print ( "Done!" )
