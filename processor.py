##################################################################
#                                                                #
#processor.py                                                    #
#Created by: R.H. Elisha     Date: 07-29-2015                    #
#Inputs: instructions input to instMem.txt                       #
#Outputs: Processor result, data output to dMem.txt              #
#Description: This is a processor simulation written to emulate  #
#   a processor I designed.                                      #
#Side Effects: dMem.txt may be modified                          #
##################################################################

import sys

#READING INSTRUCTION AND DATA MEMORY
try:
    instMm = open("instMem.txt", 'r')
except:
    sys.exit("No instruction Memory")
try:
    dMm = open("dMem.txt", 'r')
except:
    sys.exit("No data Memory")
instMem = list(instMm) #initializing instruction memory list
dMem = list(dMm)#initializing data memory list
dMem = [m.replace('\n','') for m in dMem] #removing all unnecessary line breaks and empty lines from the data memory
instMm.close() #closing the file as we are done with it
dMm.close() #closing the file as we are done with it
pC = 0 #starting the program counter off at 0

#GLOBAL CONTROL VARIABLES
rRead = False
rWrite = False
imm = False
func = 0
la = False
mRead = False
mWrite = False
beq = False
j = False
registerFile = ['0000000000000000']*16
MAR = '0'*16
#END GLOBAL CONTROL

def control(opCode): #takes a 4 bit opcode, changes global flag variables and function code
    global func, rRead, rWrite, imm, la, mRead, mWrite, beq, j, registerFile, MAR
    func = int(opCode[2:4],2)
    if opCode[0:2] == '01': #r-type
        rRead,rWrite,imm,la,mRead,mWrite,beq,j = True,True,False,False,False,False,False,False
    elif opCode[0:2] == '00': #i-type
        rRead,rWrite,imm,la,mRead,mWrite,beq,j = True,func == 0,True,False,False,False,func==1,False
    elif opCode[0:2] == '10': #i-type section 2
        rRead,rWrite,imm,la,mRead,mWrite,beq,j = opCode[3]=='0',opCode[3]=='1',func==0,func==0,opCode[3]=='1',func==2,False,False
    elif opCode[0:2] == '11': #j-type
        rRead,rWrite,imm,la,mRead,mWrite,beq,j = False,False,False,False,False,False,False,True

def regFileRead(rA, rB): #rA, rB are 4 bit binary strings
    return {'rA':registerFile[int(rA,2)],'rB':registerFile[int(rB,2)]}if rRead else{'rA':'0'*16,'rB':'0'*16}
def regFileWrite(rA, val): #rA is a string, val is a string
    registerFile[int(rA,2)] = val if rWrite else registerFile[int(rA,2)]
def signExt(immd): #immd is an 8 bit binary string
    return immd[0]*8+immd
def twosComp(bitString): #bitstring is any length binary string
    return int(bitString,2) if bitString[0]=='0' else int(bitString,2) - (2**len(bitString))
def toTwosComp(dec): #dec is a decimal int
    return format(2**16+dec, '008b') if dec<0 else format(2**16+dec, '008b')[1:17]
def bitwiseNOR(bsA, bsB): #takes to bitStrings and does a bitwise NOR on them
    return ''.join('1' if bsA[x] == '0' and bsB[x] == '0' else '0' for x in range(0,len(bsA)))
def ALU(rA,rB): #rA, rB are strings, returns a dictionary with string value for 'out' and boolen 'zero'
    if func == 0: #function add
        result = twosComp(rA)+twosComp(rB) #result is int
        return {'out': toTwosComp(result), 'zero': result==0}
    elif func == 1: #function subtract
        result = twosComp(rA)-twosComp(rB)
        return {'out': toTwosComp(result), 'zero': result==0}
    elif func == 2: #function NOR
        result = bitwiseNOR(rA, rB)
        return {'out': result, 'zero': result=='0'*16}
def MEM(rA): #rA is a string
    if mRead:
        return {'out':dMem[int(MAR,2)]} #read from memory, returns a dictionary
    elif mWrite:
        dMem[int(MAR,2)] = rA #write to memory
        return None

while pC < len(instMem): #main program loop, runs until the PC reaches the end of the instructions
    line = instMem[pC][0:16].replace('\n','') #gets the instruction memory line
    opCode = line[0:4] #opcode is 4 MSB
    rA = line[4:8] #Register A
    rB = line[8:12] #Register B
    immd = line[8:16] #immidiate value
    jV = line[4:16] #jump value
    control(opCode) #opCode is a 4bit string
    regs = regFileRead(rA, rB) #rA, rB are 4 bit strings
    A = ALU(regs['rA'],(signExt(immd) if imm else regs['rB'])) #ALU takes in register A's value and either register B's value or the immediate
    MAR = A['out'] if la else MAR #MAR is set only if la flag is set
    dM = MEM(regs['rA']) #get dataMemory
    val = dM['out'] if mRead else A['out'] #pick which value to write to registers (memory or ALU)
    regFileWrite(rA, val) #write to register file
    print "\n\nPC: "+str(pC) #print the PC
    print registerFile #show the registers
    print 'MAR: ' + MAR
    if mWrite: #if a data memory value was modified
        print 'Modified Memory: value:' + dMem[int(MAR,2)] + ' at address: ' + MAR #print it
    print '--------------------------------------------------------------------------------' #aesthetic separator
    pC += 1 #increment PC
    pC = pC + twosComp(signExt(immd)) if (beq and int(regs['rA'],2)==0) else pC #if beq flag is set, add extra value to PC
    pC = int((format(pC, '016b')[0:4]+jV),2) if j else pC #if j flag is set, set the PC to the jump value
    
dMm = open("dMem.txt",'w') #reopen the data memory file
for line in dMem: #write each line to it.
    print line #print written line at the end of the program
    dMm.write(line[0:16]+"\n") #write the word
dMm.close() #clsoe the file after writing
