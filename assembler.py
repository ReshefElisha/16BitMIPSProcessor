##################################################################
#                                                                #
#assembler.py                                                    #
#Created by: R.H. Elisha     Date: 07-29-2015                    #
#Inputs: assemby input to assm.txt                               #
#Outputs: binary format instructions to instMem.txt              #
#Description: This is an assembler written to quickly convert    #
#           human readable assembly to computer code binary      #
#Side Effects: instMem.txt will be modified                      #
##################################################################

import sys
#OPEN FILES NEEDED FOR READING AND WRITING
try:
    assm = list(open("assm.txt", 'r')) #read from assm.txt
    instMem = open("instMem.txt", 'w') #write to instMem.txt
except:
    sys.exit("Error in the file system somewhere") #Catch the error if it happens and exit

def toTwosComp(dec): #dec is a decimal int
    return format(2**8+dec, '008b') if dec<0 else format(2**8+dec, '008b')[1:9] #return two's complement string

for line in assm: #for each line in the assembly code
    l = line.partition(' ') #separate it at the first space
    comm = l[0] #command is before the space
    args = l[2].replace(' ','') #remove spaces from arguments
    args = l[2].replace('\n','') #remove newlines from arguments
    print comm
    if comm == 'addi': #addi instruction
        parts = args.partition(',')
        rA = format(int(parts[0]),'004b')
        rA = rA[len(rA)-4:len(rA)]
        imm = toTwosComp(int(parts[2]))
        inst = '0000'+rA+imm
    elif comm == 'beq': #beq instruction, etc...
        parts = args.partition(',')
        rA = format(int(parts[0]),'004b')
        rA = rA[len(rA)-4:len(rA)]
        imm = toTwosComp(int(parts[2]))
        inst = '0001'+rA+imm
    elif comm == 'add':
        parts = args.partition(',')
        rA = format(int(parts[0]),'004b')
        rA = rA[len(rA)-4:len(rA)]
        rB = format(int(parts[2]),'004b')
        rB = rB[len(rB)-4:len(rB)]
        inst = '0100'+rA+rB+'0000'
    elif comm == 'sub':
        parts = args.partition(',')
        rA = format(int(parts[0]),'004b')
        rA = rA[len(rA)-4:len(rA)]
        rB = format(int(parts[2]),'004b')
        rB = rB[len(rB)-4:len(rB)]
        inst = '0101'+rA+rB+'0000'
    elif comm == 'nor':
        parts = args.partition(',')
        rA = format(int(parts[0]),'004b')
        rA = rA[len(rA)-4:len(rA)]
        rB = format(int(parts[2]),'004b')
        rB = rB[len(rB)-4:len(rB)]
        inst = '0110'+rA+rB+'0000'
    elif comm == 'la':
        parts = args.partition(',')
        rA = format(int(parts[0]),'004b')
        rA = rA[len(rA)-4:len(rA)]
        imm = format(int(parts[2]),'008b')
        imm = imm[len(imm)-8:len(imm)]
        inst = '1000'+rA+imm
    elif comm == 'lw':
        rA = format(int(args),'004b')
        rA = rA[len(rA)-4:len(rA)]
        inst = '1001'+rA+('0'*8)
    elif comm == 'sw':
        rA = format(int(args),'004b')
        rA = rA[len(rA)-4:len(rA)]
        inst = '1010'+rA+('0'*8)
    elif comm == 'j':
        jVal = format(int(args),'012b')
        jVal = jVal[len(jVal)-12:len(jVal)]
        inst = '1100'+jVal
    else: #something else, just leave a NOP
        inst = '0'*16
    instMem.write(inst+'\n') #write the line to instruction memory

print 'DONE' #print DONE if everything went well
        
    
