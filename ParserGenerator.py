import sys

# conditions on grammar:
# e is left at the end

# need to add:
# fetch terminal for e case

# think about having the LHS rule appear in many places in its parent LHS
# cases to consider:
# or with only calls -> get tokens up or down
#
class ParserGenerator:

    def __init__(self, grammar, parser):
        self.tokensLookAhead = []
        self.LHSrules = []
        self.RHSrules = []
        self.productionTokens = []
        with open(grammar, 'r') as f:
            self.lines = f.readlines()
        self.fparser = open(parser, 'w')
    
    def tokenize(self):
        for i in range(len(self.lines)):
            line = self.lines[i]
            LHSrule = line.split('=')[0].strip()
            ind = len(LHSrule) + 3
            line  = line[ind:]
            RHSrule = line.split('|')
            self.LHSrules.append(LHSrule)
            self.RHSrules.append(RHSrule)
            
    def getTokens(self):
        for i in range(len(self.RHSrules)):
            prodTokens = []
            for j in range(len(self.RHSrules[i])):
                prod = self.RHSrules[i][j]
                tokens = prod.split()
                prodTokens.append(tokens)
              
            self.productionTokens.append(prodTokens)
          
    def inLHSrules(self, token):
        for i in range(len(self.LHSrules)):
            if(token == self.LHSrules[i]):
                return i
        return -1
            
    def getTerminalDown(self, firstToken):
        if(firstToken[0] == '#'):
            return firstToken
        else:
            ind = self.inLHSrules(firstToken)
            for i in range(len(self.RHSrules[ind])):
                firstToken = self.RHSrules[ind][i].split()[0].strip()
                return self.getTerminalDown(firstToken)
                
    def inSubRule(self, ind, curLHS):
        subRules = self.RHSrules[ind]
        for i in range(len(subRules)):
            tokensOfSubRule = subRules[i].split()
            for j in range(len(tokensOfSubRule)):
                if(curLHS == tokensOfSubRule[j]):
                    if(j+1 >= len(tokensOfSubRule)): #nothing after subrule
                        return 'LHS', self.LHSrules[ind]
                    else:
                        nextToken = tokensOfSubRule[j+1].strip()
                        if(nextToken[0] == '#'):
                            return 'TERMINAL', nextToken
                        else:
                            return 'RHS', nextToken
        return 'NONE', 'NONE'
                        
    def getTerminalUp(self, curLHS):
        i = self.inLHSrules(curLHS) - 1
        #print("i {}\n".format(i))
        while(i >= 0):
            LHS = self.LHSrules[i]
            type, afterCurLHS = self.inSubRule(i, curLHS)
            if(type == 'NONE' and afterCurLHS == 'NONE'):
                i = i - 1
            else:
                if(type == 'TERMINAL'):
                    return afterCurLHS
                elif(type == 'RHS'):
                    return self.getTerminalDown(afterCurLHS)
                else:
                    return self.getTerminalUp(afterCurLHS)
                
    def indent(self, ind):
        while(ind > 0):
            self.fparser.write("    ")
            ind = ind - 1
        
    def writeBasics(self):
        f = open('sampleParser.py', 'r')
        lines = f.readlines()
        for i in range(len(lines)):
            self.fparser.write(lines[i])
        
    def writeMain(self):
        f = open('main.py', 'r')
        lines = f.readlines()
        for i in range(len(lines)):
            self.fparser.write(lines[i])
            
    def writeCond(self, lookAhead):
        self.fparser.write('if(self.nextToken() == "{}"):\n'.format(lookAhead))
		self.fparser.write("self.Lex()\n")
		#return 1
    
    def writeProc(self, name):
        self.fparser.write("self.{}()\n".format(name))
    
    def writeElse(self, ind):
        self.indent(ind)
        self.fparser.write("else:\n")
        self.indent(ind + 1)
        self.fparser.write("self.reject()\n")
        
    def writeElif(self, ind, lookAhead):
        self.indent(ind)
        self.fparser.write('elif(self.nextToken() == "{}"):\n'.format(lookAhead))
        
    def writeElifCons(self, lookAhead, ind):
        self.indent(ind)
        self.fparser.write('elif(self.nextToken() == "{}"):\n'.format(lookAhead))
        self.indent(3)
        self.fparser.write('self.Lex()\n')
        
    def checkToken(self, token, ind):
        if(token[0] == '#'):
            token = token[1:]
            self.indent(ind)
            self.writeCond(token)
            return 1
        else:
            self.indent(ind)
            self.writeProc(token)
            return 0
    
    def writeSingle(self, i):   
        Ifs = 0
        IndexIf = []
        tokens = self.productionTokens[i][0]
        for y in range(len(tokens)):
            if(y == 0):
                ind = y + 2
            else:
                ind = y 
            if(self.checkToken(tokens[y], ind) == 1):
                Ifs = Ifs + 1
                IndexIf.append(ind)
                
        return Ifs, IndexIf
        
    #assumption : if have many subrules, shld have an elif. even if only two
    def writeMultiple(self, i):
        Ifs, IndexIf = self.writeSingle(i) #output first one
        while(Ifs > 1):
            self.writeElse(IndexIf[Ifs - 1])
            Ifs = Ifs - 1
            
        y = 1
        Ifs = 0
        IndexIf = []
        maxY = len(self.productionTokens[i])
        while(y < maxY):
            tokens = self.productionTokens[i][y]
            if(tokens[0][0] == '#'):
                #add indent
                token = tokens[0][1:]
                self.writeElifCons(token, 2)
            elif(tokens[0] == 'e'):
                print("niahahahha\n")
                token = self.getTerminalUp(self.LHSrules[i]) #nope change that
                token = token[1:]
                self.writeElif(2, token)
            else:
                token = self.getTerminalDown(tokens[0])
                token = token[1:]
                self.writeElif(2, token)
                
            tokens = tokens[1:]
            x = 1
            for x in range(len(tokens)):
                #add indent
                if(self.checkToken(tokens[x], x) == 1):    
                    Ifs = Ifs + 1
                    IndexIf.append(x)
            y = y + 1
        
        return Ifs, IndexIf
        
    def writeParser(self):
        self.getTokens()
        self.writeBasics()
        for i in range(len(self.LHSrules)):
            print("functions\n")
            self.fparser.write("\n\n")
            self.indent(1)
            self.fparser.write("def ")
            self.fparser.write(self.LHSrules[i])
            self.fparser.write("(self):\n")
        
            n = len(self.productionTokens[i])
            if(n == 1):
                Ifs, IndexIf = self.writeSingle(i)
                while(Ifs > 0):
                    self.writeElse(IndexIf[Ifs-1])
                    Ifs = Ifs - 1
            else:
                #self.fparser.write("not yet!!\n")
                Ifs, IndexIf = self.writeMultiple(i)
                while(Ifs > 0):
                    self.writeElse(IndexIf[Ifs-1])
                    Ifs = Ifs - 1
                
                self.writeElse(2)
        self.fparser.write("\n\n")
        self.writeMain()
              
    def printAll(self):
        self.getTokens()
        for i in range(len(self.LHSrules)):
            print(self.LHSrules[i])
            print(self.RHSrules[i])
            print("prod\n")
            print(self.productionTokens[i])
        # for i in range(len(self.LHSrules)):
            # print(self.LHSrules[i])
           # for j in range(len(self.tokensLookAhead[i])):                                                                                              
            
def main():
    prsg = ParserGenerator("Grammar.txt", "psskch.py")
    prsg.tokenize()
    prsg.writeParser()
   # prsg.printAll()
        
if __name__ == "__main__":
    main()
    
        
        
