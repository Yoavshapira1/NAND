// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

@i
M=0

//check if only one number
@R15
D=M
@END
D-1;JEQ

(OUTERLOOP)
    @swapped
    M=0
    @j
    M=0

    (INNERLOOP)
    //find num 1
        @R14
        D=M
        @j
        A=M+D
        D=M
        @num1
        M=D

    //find num 2
        @R14
        D=M
        @j
        A=M+D
        A=A+1
        D=M
        @num2
        M=D

    //check if need to swap
        @num1
        D=D-M
        @SWAP
        D;JGT

        @INNERCONTINUE
        0;JMP

        (SWAP)
            @R14
            D=M
            @j
            A=M+D
            D=A
            @address
            M=D

            @num2
            D=M
            @address
            A=M
            M=D

            @num1
            D=M
            @address
            A=M+1
            M=D

            @swapped
            M=1

            @INNERCONTINUE
            0;JMP

        (INNERCONTINUE)
        // increment j
            @j
            M=M+1
            D=M
            @R15
            D=D-M
            @INNERLOOP
            D+1;JLT

            @OUTERCONTINUE
            0;JMP

    (OUTERCONTINUE)
        @swapped
        D=M
        @END
        D;JEQ

    //increment i
        @i
        M=M+1
        D=M
        @R15
        D=D-M
        @OUTERLOOP
        D+1;JLT

        @END
        0;JMP

(END)
    @END
    0;JMP




