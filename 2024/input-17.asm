
2,4  BST A   B = A & 7          ; B = A (lowest 3 bits)
1,7  BXL 7   B = B ^ 7          ; Invert B; B is inverse of lowest 3 bits of A
7,5  CDV B   C = A // (2 ** B)  ; C = A >> B; C is A shifted right by inverse lowest 3 bits of A
1,7  BXL 7   B = B ^ 7          ; Invert B; B is back to lowest 3 bits of A
4,6  BXC     B = B ^ C          ; B ^= C; invert B by C
0,3  ADV 3   A = A // (2 ** 3)  ; A = A >> 3; dump lowest 3 bits of A
5,5  OUT B   OUTPUT B & 7       ; Output lowest 3 bits of B
3,0  IF A != 0 JMP to 0         ; Restart until A is 0.

A is 48 bits

Output is lowest 3 bits of A xor with 3 bits in A at the inverse of its lowest 3 bits.
So only lowest 10 bits count.

AB_CDEF_G000 = 000 ^ ABC
AB_CDEF_G001 = 001 ^ BCD 
AB_CDEF_G010 = 010 ^ CDE
AB_CDEF_G011 = 011 ^ DEF
AB_CDEF_G100 = 100 ^ EFG
AB_CDEF_G101 = 101 ^ FG1 = 100 ^ FG0
AB_CDEF_G110 = 110 ^ G11 = 100 ^ G01
AB_CDEF_G111 = 111 ^ 111 = 000

000 011 101 101 011 000 110 100 111 001 101 111 111 001 100 010
xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx xxx

