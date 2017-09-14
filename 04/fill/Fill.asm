// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(LOOP)
@INIT_LOOP
0;JMP
(LOOP_START)
@KBD
D=M
@BLACK
D;JNE
@WHITE
D;JEQ
@LOOP
0;JMP

(INIT_LOOP)
@SCREEN
D=A
@addr    //Load a register with the register number
M=D
@SCREEN  // Compute the difference between the screen and keyboard addresses and store it
D=A
@KBD
D=A-D
@i
M=D
@LOOP_START
0;JMP


(BLACK)
@addr //Set a row to zero
A=M
M=-1
@addr //Increment the address
M=M+1
@i   //Increment the counter
M=M-1
D=M
@LOOP
D;JEQ
@BLACK
0;JMP


(WHITE)
@addr //Set a row to zero
A=M
M=0
@addr //Increment the address
M=M+1
@i   //Increment the counter
M=M-1
D=M
@LOOP
D;JEQ
@WHITE_LOOP
0;JMP
