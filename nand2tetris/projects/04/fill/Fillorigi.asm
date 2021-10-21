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

@8192
D=A
@limit
M=D

@color
M=0
(WHILE)
    @color
    D=!M
    @KBD
    D=D&M
    @ELSE
    D;JEQ
    @color
    M=-1
    @PAINT
    0;JMP

    (ELSE)
        @KBD
        D=!M
        @color
        D=D&M
        @CONTINUE
        D;JEQ
        @color
        M=0
        @PAINT
        0;JMP

    (CONTINUE)
    @WHILE
    0;JMP

(PAINT)
    @j
    M=0
    (LOOP)
        @limit
        D=M
        @j
        D=D-M
        @WHILE
        D;JLT

        @SCREEN
        D=A
        @j
        A=D+M
        M=!M
        @j
        M=M+1
        @LOOP
        0;JMP


