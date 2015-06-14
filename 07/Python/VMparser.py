from sys import argv
from os import listdir
from os.path import join, basename, splitext, isdir, normpath
from re import sub

counter = -1
retCounter = -1

error = False

currFunction = ""
currClass = ""

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
	"push_static"	: "@{0}\nD=M\n",

	"pop"			: "\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
	"pop_local"		: "@LCL\nD=M\n@{0}\nD=A+D",
	"pop_argument"	: "@ARG\nD=M\n@{0}\nD=A+D",
	"pop_this"		: "@THIS\nD=M\n@{0}\nD=A+D",
	"pop_that"		: "@THAT\nD=M\n@{0}\nD=A+D",
	"pop_temp"		: "@5\nD=A\n@{0}\nD=A+D",
	"pop_pointer"	: "@THIS\nD=A\n@{0}\nD=A+D",
	"pop_static"	: "@{0}\nD=A",

	"label"			: "({0})\n",
	"goto"			: "@{0}\n0;JMP\n",
	"if-goto"		: "@SP\nAM=M-1\nD=M\n@{0}\nD;JNE\n",

	"call"			: "@{0}$return\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n"+
						"@LCL\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n"+
						"@ARG\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n"+
						"@THIS\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n"+
						"@THAT\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n"+
						"@{1}\nD=A\n@5\nD=D+A\n@SP\nA=M\nD=A-D\n@ARG\nM=D\n"+
						"@Sp\nA=M\nD=M\n@LCL\nM=D\n"+
						"@{2}\n0;JMP\n"+
						"({0}$return)\n",

	"return"		: "@LCL\nD=M\n@R13\nM=D\n"+
						"@5\nD=A\n@R13\nA=M-D\nD=M\n@R14\nM=D\n"+
						"@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n"+
						"@ARG\nD=M\n@SP\nM=D+1\n"+
						"@R13\nAM=M-1\nD=M\n@THAT\nM=D\n"+
						"@R13\nAM=M-1\nD=M\n@THIS\nM=D\n"+
						"@R13\nAM=M-1\nD=M\n@ARG\nM=D\n"+
						"@R13\nAM=M-1\nD=M\n@LCL\nM=D\n"+
						"@R14\nA=M\n0;JMP\n"
}


def parseLine(cmd):
	global currFunction
	orgCmd = cmd
	cmd = cmd.split()

	if cmd[0] in primitves:
		return functionTable[cmd[0]]

	elif cmd[0] in primitves_c:
		global counter
		counter += 1
		return functionTable[cmd[0]].format(counter)

	elif cmd[0] in memOps:
		if cmd[1] == "static":
			print( currClass +'.'+ cmd[2] )
			return functionTable[ cmd[0]+"_"+cmd[1] ].format( currClass +'.'+ cmd[2] ) + functionTable[cmd[0]]
		else:
			return functionTable[ cmd[0]+"_"+cmd[1] ].format( int(cmd[2]) ) + functionTable[cmd[0]]

	elif cmd[0] == "function":
		currFunction = cmd[1]
		pushes = ""
		for i in range( 0, int(cmd[2]) ):
			pushes += parseLine("push constant 0")
		return functionTable["label"].format(currFunction) + pushes

	elif cmd[0] in jmpOps:
		return functionTable[cmd[0]].format(currFunction + '$' + cmd[1] )

	elif cmd[0] == "call":
		global retCounter
		retCounter += 1
		return functionTable[ cmd[0] ].format(currFunction+'.'+cmd[1]+str(retCounter), cmd[2], cmd[1])

	elif cmd[0] == "return":
		return functionTable["return"]

	else:
		global error
		error = True
		print ("ERROR: invalid command: \"" + orgCmd+"\"")
		return orgCmd + "\t\t\t<=== ERROR\n"

def parseFile(file):
	currClass = file.split(".")[0]
	file_input = open (file, "r")

	lines = file_input.readlines()

	lines = map (lambda line: sub(r"//.*","", line), lines) #clear comments
	lines = list ( filter(None, map(str.strip, lines) ) ) #clear whitespace & empty lines
	file_input.close()

	return list( map(parseLine, lines) )

#start!
def main():
	if len(argv) > 1:
		inFile = argv[1]
		if not isdir(inFile):
			output_name = splitext( basename( normpath(inFile) ))[0] + ".asm"
			output = parseFile(inFile)

		else:
			output = ["@256\nD=A\n@0\nM=D\n", functionTable["call"].format("Pre.pre", "0", "Sys.init") ]
			for file in listdir(inFile):

				if file.endswith(".vm"):
					print("Parsing: "+str(file))
					global currClass
					currClass = splitext(file)[0]
					output += parseFile(join(inFile, file))
					#print ( output )

		output_name = join(inFile,  basename( normpath(inFile) ) + ".asm")


		if len(argv) > 2:
			output_name = argv[2]
	else:
		print(	"Input format wrong!\n"+
				"Correct input format (output optional):\n"+
				"python3 VMparser.py input (output)\n" )
		exit(1)


	file_output = open( output_name, "w" )
	print ( "Save to: " + output_name )
	file_output.writelines( output )
	file_output.close()

	endmsg = "Done"

	if error:
		endmsg += ", but an error occured. To find the broken line, please review the output file."
	else:
		endmsg += "!"

	print ( endmsg )

if __name__ == "__main__":
	main()