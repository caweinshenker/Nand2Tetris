// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


@R2   // Iniitalize R2 to 0
M=0

@R0   // Check if R0 = 0
D=M;
@END
D;JEQ

@R1   // Check if R1 = 0
D=M
@END
D;JEQ


(LOOP)
@R1      //  Else, load R1
D=M
@R2
M=D+M  // R2 = R2 + R1
@R0
M=M-1 // R0 = R0 - 1
D=M
@END
D;JEQ
@LOOP
0;JMP



(END)
@END
0;JMP
