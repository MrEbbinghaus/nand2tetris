// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.


(Loop)

//check for keyboard input
@24576 //0x4000
D=M

@White
D;JEQ

@1
D=-1
@R0
M=D

@EndWhite
0;JMP

(White)
@0
D=A
@R0
M=D
(EndWhite)

@SCREEN
D=A
@R1
M=D-1

(BlackLoop)
@R1
M=M+1

//fill pixel
@R0
D=M
@R1
A=M
M=D


//jump back
@R1
D=M
@24575
D=D-A
@BlackLoop
D;JLT

@Loop
0;JMP

@0
D=A
@SCREEN
M=D


@Loop
0;JMP