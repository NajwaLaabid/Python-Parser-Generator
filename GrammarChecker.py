import sys

    # need to add the pairwise thing for different RHSrules 
    # Grammar Description to respect for our checker:
        # - Doesn't support EBNF notation : make sure to express your grammar as BNF
        # - Each production is represented in a line : a new line means you moved to a different LHSrule
        # - RHS rules are separated by space and '|' symbol. 
        # - There's exactly one space between each tokens (terminals/non-terminals) in the production
        # - The "=" symbol is used to refer to link each LHS rule with its RHSrules (or production) 
        # - Enclose terminals between double quotes (eg. "program")
    # indirect recursion:
    # keep all lhs 'pre-processed'
    # for each first token in left recursion, check if it an LHS rule.
    # If yes, check all RHS rules of new LHS if they match old LHS

#read from file
 
class GrammarChecker:

 #alt 1: take each rule as line: reading by line stops at new line
 def __init__(self, grammar): 
        #read from the file in constructor
        with open(grammar, 'r') as f:
            self.lines = f.readlines()
 
 def isLHSrule(self, LHSrules, subRule, ind):
        i = ind + 1
        while(i < len(LHSrules)):
            str, n = LHSrules[i]
            if(subRule.strip() == str.strip()): #if subRule is a LHSrule other than its original LHSrule (because in this case, it will be a left recursion, checked by another function)
                return i
            i += 1
                
        return -1
        
 def reportLeftRecursion(self, rule1, str2):
        str1, n1 = rule1
        print("LEFT RECURSION ISSUE\n" + "Rule #{}".format(n1) + ": "+ str1.strip() +"\n" + 'Left Recursion in subrule : "' + str2.strip() + '"' + '\n\n')
        
 def leftRecursion(self, LHSrule, subRules):
        rule, n    = LHSrule
        for ind in range(len(subRules)):
            RHSrule = subRules[ind].strip()
            firstToken = RHSrule.split(" ")[0].strip()
            if(firstToken == rule):
                return ind
            
        return -1
        
 def getInitialTokens(self, subRules):
        tokens = []
        for i in range(len(subRules)):
            firstToken = subRules[i].strip().split(" ")[0].strip()
            tokens.append(firstToken)
        
        return tokens
        
#report only once
 def indirectPairwise(self, initTokens1, initTokens2):
        for i in range(len(initTokens1)):
            for j in range(len(initTokens2)):
                if(initTokens1[i] == initTokens2[j]):
                    return 1
        
        return 0
            
 def reportPairWise(self, LHSrule, subrule1, subrule2):
        str, n = LHSrule
        print("PAIRWISE DISJOINTNESS ISSUE\nRule  #{}".format(n))
        print('Rule''s parameter "'+ str + '"\nNeed to factor the two subRules : "' + subrule1.strip() + '" and "' + subrule2.strip() + '"\n\n\n')
        
 def pairWise(self, Productions, LHSrules, ind):
        i = 0
        LHSrule, subRules = Productions[ind]
        while(i < len(subRules)):
            firstToken = subRules[i].strip().split(" ")[0].strip()
            x = self.isLHSrule(LHSrules, firstToken, ind)
            initTokens1 = []
            if(x != -1):
                LHSrule1 , subRules1 = Productions[x]
                initTokens1 = self.getInitialTokens(subRules1)
            j = i + 1
            while(j < len(subRules)):
                token = subRules[j].strip().split(" ")[0].strip()
                if(firstToken == token):
                    self.reportPairWise(LHSrule, subRules[i], subRules[j])
                else:
                    y = self.isLHSrule(LHSrules, token, ind)
                    initTokens2 = []
                    if(y != -1):
                        LHSrule2 , subRules2 = Productions[y]
                        initTokens2 = self.getInitialTokens(subRules2)
                        flag = self.indirectPairwise(initTokens1, initTokens2)
                        if(flag):
                            str1, n1 = LHSrule1
                            str2, n2 = LHSrule2
                            self.reportPairWise(LHSrule, str1, str2)
                
                j = j + 1
            i = i + 1

 def reportIndirectRecursion(self, rule1, rule2):
        str1, n1  = rule1
        str2, n2 = rule2
        print("INDIRECT RECURSION ISSUE\n\n" + "Rule #{}".format(n1) + ": " + str1 + "\nRule #{}".format(n2) + ": " + str2 + "\n\n\n")

        
 def indirectRecursion(self, Productions, LHSrules):
       for i in range(len(Productions)):
            rule1, subRules1 = Productions[i]
            for j in range(len(subRules1)):
                ind = self.isLHSrule(LHSrules, subRules1[j], i)
                if(ind != -1):
                    x = 0
                    rule2, subRules2 = Productions[ind]
                    x = self.leftRecursion(rule1, subRules2) #is there a left recursion between rule1 and subrules of rule2?
                    if(x != -1):
                        self.reportIndirectRecursion(rule1, rule2) 
            

 #break down the rule into tokens to check for validity of grammar
 def getProductions(self):
        Productions = []
        LHSrules = []
        for pos in range(len(self.lines)):
            curLine = self.lines[pos]
            str = curLine.partition(" ")[0].strip()
            curLHS = (str, pos+1) 
            LHSrules.append(curLHS)
            
            i = len(str) + 3
            self.lines[pos] = self.lines[pos][i:]
            
            subRules = self.lines[pos].split("|")
            prod = (curLHS, subRules)
            Productions.append(prod)
        
        return Productions, LHSrules

 def checker(self):
        Productions, LHSrules = self.getProductions()
        
        self.indirectRecursion(Productions, LHSrules);
        
        for ind in range(len(Productions)):
            LHSrule, subRules = Productions[ind]
            self.pairWise(Productions, LHSrules, ind)
            x = self.leftRecursion(LHSrule, subRules)
            if(x != -1):
                self.reportLeftRecursion(LHSrule, subRules[x])

def main():
    gc = GrammarChecker("Grammar.txt")
    gc.checker()
        
if __name__ == "__main__":
    main()
