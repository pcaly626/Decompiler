"""Title: Project 1 (Disassembler)
   Authors: Paul Clay(ptc20)
            Christina Haynes-Zaragoza(cmh174)
   Class: CS 3339 (Computer Architecture)
   Section: 264
   Description: The program is a disassembler that is meant
                to decode a file filled with binary code into the their
                proper assembly instructions.
                """
import sys

inputFileName = 'None'
outputFileName = 'None'

# add the parsing of rgv here:

"""Method Name: printRegister:
   Arguments: instructType, arg3, arg1,arg2
   Description: the function will print to the out put file the name of
                of the indtruction in a formatted way."""
def printRegister(instructionType, arg3, arg1, arg2):
    description.append(instructionType)
    return instructionType + '\tR' + str(int(arg3[index], 2)) + ', R' + str(int(arg1[index], 2)) + ', R' + str(
        int(arg2[index], 2))

"""Method Name: sllFormat
   Arguments: instructionType, arg2, arg1, compliment 
   Description: the function will display the proper formatted out put to 
                the output file."""
def sllFormat(instructionType, arg2, arg3, sa):
    description.append(instructionType)
    return instructionType + '\tR' + str(int(arg3[index], 2)) + ', R' + str(int(arg2[index], 2)) + ', #' + str(int(sa[index],2))

"""Method Name: addiFormat
   Arguments: instructionType, arg2, arg1, compliment
   Description: the function will display the addi instruction to the ouput put 
                file in the proper format."""
def addiFormat(instructionType, arg2, arg1, compliment):
    description.append(instructionType)
    return instructionType + '\tR' + str(int(arg2[index], 2)) + ', R' + str(int(arg1[index], 2)) + ', #' + str(twosCompliment(compliment, 16))

"""Method Name: store Format
   Arguments: instructionType, arg1, arg2, compliment
   Description: handles the proper out put format for store."""
def storeFormat(instructionType, arg1, arg2, compliment):
    description.append(instructionType)
    return instructionType + '\tR' + str(int(arg2[index], 2)) + ', ' + str(twosCompliment(compliment, 16)) + '(R' + str(
        int(arg1[index], 2)) + ')'

"""Method Name: twosCompliment
   Arguments: val, bits
   Description: the function will handle the out put format the 
                2's compliment numbers."""
def twosCompliment(val, bits):
    val = int(val, 2)
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

"""Method Name: printBinary
 Arguments: showCode, validation 
 Description: will return two arguments in a formated fation."""
def printBinary(showCode, validation):
    return showCode + validation

def changeRegister(value, regChange, r):
    for i in range(0, 31):
        if i == regChange:
            r[i] = value
    return r

def outputRegisters(outFile, r, cycleCount):
    outFile.write("=" * 21 + "\n")
    outFile.write('cycle:' + str(cycleCount) + '\t' + str(PC) + '\t' + str(mipsTranslation[index] + '\n\n'))
    outFile.write("registers:\n")
    outFile.write('r00:')
    for i in range(0,32):
        if i == 7:
            outFile.write('\t' + str(r[i]) + '\n' + 'r08:')
        elif i == 15:
            outFile.write('\t' + str(r[i]) + '\n' + 'r16:')
        elif i == 23:
            outFile.write('\t' + str(r[i]) + '\n' + 'r24:')
        elif i == 31:
            outFile.write('\t' + str(r[i]) + '\n\n')
        else:
            outFile.write('\t' + str(r[i]))

def outputData(data, outFile):
    outFile.write('data:\n')
    for i, index in enumerate(data):
        if i == 0:
            outFile.write(str(pcCounter[i]) + ':' + '\t' + str(data[i]))
        elif i == 8:
            outFile.write('\n' + str(pcCounter[i]) + ':' + '\t' + str(data[i]))
        elif i == 16:
            outFile.write('\n' +str(pcCounter[i]) + ':' + '\t' + str(data[i]))
        elif i == 23:
            outFile.write('\t' + str(data[i]))
        else:
            outFile.write('\t' + str(data[i]))
    outFile.write('\n\n')


def findMemLocation(memLocation, pcCounter):
    for index, i in enumerate(pcCounter):
        if i == memLocation:
            return index

def findRegLocation(regLocation, r):
		for index, i in enumerate(r):
				if i == regLocation:
						return index

if __name__ == "__main__":
    for i in range(len(sys.argv)):
        if(sys.argv[i] == '-i' and i < (len(sys.argv)-1)):
            inputFileName = sys.argv[i+1]
            print inputFileName
        elif(sys.argv[i] == '-o' and i < (len(sys.argv)-1)):
            outputFileName = sys.argv[i+1]


arg1 = []
arg2 = []
arg3 = []
opcode = []
offSet = []
function = []
valid = []
mipsTranslation = []
data = []
pcCounter = []
description = []
address = []
PC = 96
isBreak = False
listCounter = 0
instruction = [line.rstrip() for line in open(inputFileName, 'rb')]
outFile = open(outputFileName + "_dis.txt", 'w')

#
#Here is what the for loop will do
#
#

for index, i in enumerate(instruction):
    valid.append(i[0])
    opcode.append(i[1:6])
    arg1.append(i[6:11])
    arg2.append(i[11:16])
    arg3.append(i[16:21])
    offSet.append(i[21:26])
    function.append(i[26:])

    #showCode is the format for all of the mips instructions
    showCode = valid[index] + " " + opcode[index] + " " + arg1[index] + " " + arg2[index] + " " + arg3[index] + " " + \
               offSet[index] + " " + function[index] + "  " + str(PC) + "\t\t"

    #nonFormattedCode is the format for code after the break
    nonFormattedCode = valid[index] + opcode[index] + arg1[index] + arg2[index] + arg3[index] + offSet[index] + \
                       function[index] + "\t" + str(PC) + "\t\t"

    #--------------------------------------------------------------------
    #These are a series of if/elif statements that determine the Mips
    #instructions. There are 3 different sections that check:
    #1. if the Opcode is 00000 or 0
    #   - Then the instruction is decided from the function section's
    #     decimal equivalent
    #2. if the Opcode's decimal equivalent is less than or equal to 3 or
    #   1
    #3. if the Opcode's decial equivalent is either 2 or 3
    #--------------------------------------------------------------------

    if valid[index] == '0' and isBreak == False:
        mipsTranslation.append('Invalid')
        description.append('Invalid')
        listCounter += 1
        outFile.write(printBinary(showCode, 'Invalid Instruction' + "\n"))
    elif int(function[index], 2) == 13 or isBreak == True:
        isBreak = True
        if int(function[index], 2) != 13:
            if valid[index] == '1':
                compliment = valid[index] + opcode[index] + arg1[index] + arg2[index] + arg3[index] + offSet[index] + \
                             function[index]
                data.append(twosCompliment(compliment, 32))
                pcCounter.append(PC)
                mipsTranslation.append(twosCompliment(compliment, 32))
            else:
                compliment = valid[index] + opcode[index] + arg1[index] + arg2[index] + arg3[index] + offSet[index] + \
                             function[index]
                data.append(twosCompliment(compliment, 32))
                pcCounter.append(PC)
                mipsTranslation.append(twosCompliment(compliment, 32))
            outFile.write(nonFormattedCode + str(mipsTranslation[listCounter]) + '\n')
            listCounter += 1
        else:
            description.append('BREAK')
            mipsTranslation.append('BREAK')
            outFile.write(showCode + str(mipsTranslation[listCounter]) + '\n')
            listCounter += 1
    elif valid[index] == '1':
        if int(opcode[index], 2) == 0 and isBreak == False:
            if int(function[index], 2) == 36:
                mipsTranslation.append(printRegister('AND', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 37:
                mipsTranslation.append(printRegister('OR', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 38:
                mipsTranslation.append(printRegister('XOR', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 10:
                mipsTranslation.append(printRegister('MOVZ', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 0:
                if int(arg3[index], 2) != 0:
                    mipsTranslation.append(sllFormat('SLL', arg2, arg3, offSet))
                    outFile.write(showCode + mipsTranslation[listCounter] + '\n')
                else:
                    description.append('NOP')
                    mipsTranslation.append('NOP')
                    outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 34:
                mipsTranslation.append(printRegister('SUB', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 32:
                mipsTranslation.append(printRegister('ADD', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 8 and int(arg1[index], 2) != 0:
                description.append('JR')
                mipsTranslation.append('JR' + '\tR' + str(int(arg1[index], 2)))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(function[index], 2) == 2:
                description.append('SRL')
                mipsTranslation.append(
                    'SRL' + '\tR' + str(int(arg3[index], 2)) + ', R' + str(int(arg2[index], 2)) + ', #' + str(
                        twosCompliment(offSet[index], 5)))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            listCounter += 1
        elif int(opcode[index], 2) >= 3 or int(opcode[index], 2) <= 1 and isBreak == False:
            if int(opcode[index], 2) == 8:
                compliment = arg3[index] + offSet[index] + function[index]
                mipsTranslation.append(addiFormat('ADDI', arg2, arg1, compliment))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(opcode[index], 2) == 28:
                mipsTranslation.append(printRegister('MUL', arg3, arg1, arg2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(opcode[index], 2) == 11:
                compliment = arg3[index] + offSet[index] + function[index]
                mipsTranslation.append(storeFormat('SW', arg1, arg2, compliment))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(opcode[index], 2) == 3:
                compliment = arg3[index] + offSet[index] + function[index]
                mipsTranslation.append(storeFormat('LW', arg1, arg2, compliment))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(opcode[index], 2) == 6:
                off = int(arg3[index] + offSet[index] + function[index],2)
                description.append('BLEZ')
                mipsTranslation.append(
                    'BLEZ' + '\tR' + str(int(arg1[index], 2)) + ', #' + str(off << 2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(opcode[index], 2) == 4:
                description.append('BEQ')
                off = int(arg3[index] + offSet[index] + function[index],2)
                mipsTranslation.append(
                    'BEQ' + '\tR' + str(int(arg1[index], 2)) + ', R' + str(int(arg2[index], 2)) + ', #' + str(off << 2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            elif int(opcode[index], 2) == 5:
                description.append('BNE')
                off = int(arg3[index] + offSet[index] + function[index],2)
                mipsTranslation.append('BNE' + '\tR' + str(int(arg1[index], 2)) + ', R' + str(int(arg2[index], 2)) + ', #' + str(off << 2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            listCounter += 1
        elif int(opcode[index], 2) == 2 or int(opcode[index], 2) == 3 and isBreak == False:
            if int(opcode[index], 2) == 2 and int(arg1[index], 2) == 0:
                description.append('J')
                instrIndex = int(arg1[index] + arg2[index] + arg3[index] + offSet[index] + function[index], 2)
                mipsTranslation.append('J' + '\t#' + str(instrIndex << 2))
                outFile.write(showCode + mipsTranslation[listCounter] + '\n')
            listCounter += 1
    address.append(PC)
    PC += 4

#######################################################################################################################
# PART 2 BEGINS HERE
#######################################################################################################################
outFile.close
r = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
outFile = open(outputFileName + "_sim.txt", "w")
PC = 96
notBreak = True
cycleCount = 1
index = 0

while(notBreak):

    index = address.index(PC)
    if description[index] == 'BREAK':
        notBreak = False
        outputRegisters(outFile, r, cycleCount)
        outputData(data, outFile)
    elif valid[index] == '0':
				cycleCount -=1
    elif valid[index] == '1':
        if description[index] == 'AND':
            rs = int(arg1[index], 2)
            rt = int(arg2[index], 2)
            rd = int(arg3[index], 2)
            r[rd] = r[rs] & r[rt]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'OR':
            rs = int(arg1[index], 2)
            rt = int(arg2[index], 2)
            rd = int(arg3[index], 2)
            r[rd] = r[rs] | r[rt]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'XOR': #XOR
            rs = int(arg1[index], 2)
            rt = int(arg2[index], 2)
            rd = int(arg3[index], 2)
            r[rd] = r[rs] ^ r[rt]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'MOVZ': #MOVZ
            rs = int(arg1[index], 2)
            rt = int(arg2[index], 2)
            rd = int(arg3[index], 2)
            if r[rt] == 0:
                r[rd] = r[rs]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'SLL':
            sa = int(offSet[index],2)
            rd = int(arg3[index], 2)
            rt = int(arg2[index],2)
            r[rd] = r[rt] << sa
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'NOP':
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'SUB':
            rs = int(arg1[index], 2)
            rt = int(arg2[index],2)
            rd = int(arg3[index], 2)
            r[rd] = r[rs] - r[rt]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'ADD':
            rs = int(arg1[index], 2)
            rt = int(arg2[index], 2)
            rd = int(arg3[index], 2)
            r[rd] = r[rs] + r[rt]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'JR':
            rs = int(arg1[index],2)
            jr = int(offSet[index],2)
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'SRL':
            sa = int(offSet[index], 2)
            rd = int(arg3[index], 2)
            rt = int(arg2[index], 2)
            r[rd] = r[rt] >> sa
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'ADDI':
            immediate = twosCompliment(arg3[index] + offSet[index] + function[index],16)
            rs = int(arg1[index],2)
            rt = int(arg2[index],2)
            r[rt] = r[rs] + immediate
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'MUL':
            rs = int(arg1[index], 2)
            rt = int(arg2[index], 2)
            rd = int(arg3[index], 2)
            r[rd] = r[rs] * r[rt]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'SW':
            memLocation = int(arg3[index] + offSet[index] + function[index], 2)
            regLocation = int(arg1[index], 2)
            memIndex = findMemLocation(memLocation, pcCounter)
            base = r[regLocation]
            rt = int(arg2[index], 2)
            if memIndex is None:
                pcCounter.append(memLocation)
                data.append(r[rt])
                for i in range(0,7):
                    memLocation += 4
                    pcCounter.append(memLocation)
                    data.append(0)
                memIndex = findMemLocation(memLocation, pcCounter)
                outputRegisters(outFile, r, cycleCount)
                outputData(data, outFile)
                outFile.write('\n')
            else:
                data[memIndex + (base /4)] = r[rt]
                outputRegisters(outFile, r, cycleCount)
                outputData(data, outFile)
        elif description[index] == 'LW':
            memLocation = int(arg3[index] + offSet[index] + function[index], 2)
            regLocation = int(arg1[index],2)
            memIndex = findMemLocation(memLocation, pcCounter)
            base = r[regLocation]
            rt = int(arg2[index],2)
            print
            r[rt] = data[memIndex + (base / 4)]
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'BLEZ':
            compliment = arg3[index] + offSet[index] + function[index]
            rs = int(arg1[index], 2)
            value = int(compliment, 2) << 2
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
            if r[rs] <= 0:
								PC += value
        elif description[index] == 'BEQ':#BEQ
            compliment = arg3[index] + offSet[index] + function[index]
            regChange = int(arg2[index], 2)
            value = int(compliment, 2)
            r = changeRegister(value, regChange, r)
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'BNE':
            compliment = arg3[index] + offSet[index] + function[index]
            regChange = int(arg2[index], 2)
            value = int(compliment, 2)
            r = changeRegister(value, regChange, r)
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
        elif description[index] == 'J':
            jump = int(arg1[index] + arg2[index] + arg3[index] + offSet[index] + function[index],2) << 2
            outputRegisters(outFile, r, cycleCount)
            outputData(data, outFile)
            PC = jump
            PC -= 4
    cycleCount += 1
    index += 1
    PC += 4
