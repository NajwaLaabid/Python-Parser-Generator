# Algorithm used :
# Use DFS on RHS rules (stack implementation).
# For each popped rule, check if it appears among LHS rules. 
# If yes mark as found. If not, push into stack of missing.
# At the end, check list of lHS : all elements where found = 0 are unreachable.

# Grammar Format :
# first token of each new line is an LHS
# LHS = RHS1 | RHS2 |... |RHSn
# LHS2 = RHSx...

# Other specifications :
# Terminals are written between quotes


import sys

class ReachableMissing:
    
    def __init__(self, grammar):
        with open(grammar, 'r') as f:
            self.lines = f.readlines()
            
    def report(self, missing, unreachable):
        if(missing == []):
            print("No missing productions.\n")
        else:
            print("The following are missing productions:\n")
            for i in range(len(missing)):
                print("Non-terminal: " + missing[i] + "\n")
                
        if(unreachable == []):
            print("No unreachable productions")
        else :
            print("The following are unreachable productions:\n")
            for i in range(len(unreachable)):
                l = list(unreachable[i])
                print("Rule #{}".format(l[2]) + "\nNon-terminal: " + l[0] + "\n")
        
    def isLHSrule(self,subRule):
        for i in range(len(self.LHSrules)):
            str, n, ind = self.LHSrules[i]
            if(subRule == str):
                return i
                
        return -1
        
    def getRules(self):
        self.LHSrules = []
        self.subRules = []
        
        for i in range(len(self.lines)):
            line = self.lines[i].strip()
            LHSrule = line.split(" ")[0].strip()
            if(i == 0):
                self.LHSrules.append((LHSrule, 1, i+1))
            else:
                self.LHSrules.append((LHSrule, 0, i+1))
            
            #after spliting the production, we only have the RHSrule left in line
            ind = len(LHSrule)+3
            RHSrule = self.lines[i][ind:].strip()
            
            #get non-terminals from the RHSrule
            nonTerminal = []
            while(len(RHSrule) > 0):
                subRule = RHSrule.split("|")[0].strip()
                ind = len(subRule)+3
                RHSrule = RHSrule[ind:].strip()
              
                while(len(subRule) > 0):
                     token = subRule.split()[0]
                     ind = len(token) + 1
                     subRule = subRule[ind:]
                     if(token[0] != '"'):
                        nonTerminal.append(token)
            
            #gets list of all non terminals in all RHSrules of a given LHSrule
            self.subRules.append(nonTerminal)
        
    
    def missing(self):
        missing = []
        stack = self.subRules[0]
       
        while(len(stack) > 0):
            subRule = stack.pop()
            x = self.isLHSrule(subRule)
            if(x != -1):
                l = list(self.LHSrules[x])
                l[1] = 1
                self.LHSrules[x] = tuple(l)
                RHSrules = self.subRules[x]
                
                for i in range(len(RHSrules)):
                    stack.append(RHSrules[i])
            else:
                missing.append(subRule)
                
        return missing
        
    def unreachable(self):
        unreachableRules = []
        for i in range(len(self.LHSrules)):
            if(self.LHSrules[i][1] == 0):
                unreachableRules.append(self.LHSrules[i])
                
        return unreachableRules
            
    def check(self):
        self.getRules()
        self.report(self.missing(), self.unreachable())


def main():
    rm = ReachableMissing("test.txt")
    rm.check()
        
if __name__ == "__main__":
    main()
