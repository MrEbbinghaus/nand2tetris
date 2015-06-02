from sys import argv

stack = []

def gen_gen(string):
	def gen():
		x = 0
		while (True):
			yield string.format(x)
			x = x +1
	return gen

functionTable = {
#tested: add, sub, neg, and, eq 
	"add": "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n",
	"sub": "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n",
	"neg": "@SP\nA=M\nM=-M\n",

	"eq" : gen_gen("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@EQ_End{0}\nD;JEQ\n@SP\nA=M-1\nM=0\n(EQ_End{0})\n")(),
	"gt" : gen_gen("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@GT_End{0}\nD;JGT\n@SP\nA=M-1\nM=0\n(GT_End{0})\n")(),
	"lt" : gen_gen("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@LT_End{0}\nD;JLT\n@SP\nA=M-1\nM=0\n(LT_End{0})\n")(),

	"and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n",
	"or" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n",
	"not": "@SP\nA=M-1\nM=!M\n",

	"push": ""
}

def parse():
	print( next(functionTable["eq"]) )

'''
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
'''
parse()
parse()
