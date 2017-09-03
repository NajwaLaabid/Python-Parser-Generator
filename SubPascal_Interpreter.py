import sys, re

keywords = set(['PROGRAM', 'IDENTIFIER', 'ARRAY', 'NUM', 'OF', 'INTEGER', 'REAL', 'FUNCTION', 'REAL', 'FUNCTION', 'PROCEDURE', 'BEGIN', 'END', 'AND', 'OR', 'DIV', 'MOD', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'RELOP', 'OP', 'NOT'])

symbols = set(['(', ')', '[', ']', ';', ',' ,'.', ':' , '.', '=', '<', '>', '-', '+', '\\', '*'])

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def printToken(self):
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = self.value
        )

class LexAnalyzer:

    #regex used :
    identifier = re.compile(r"[a-zA-Z][a-zA-Z0-9]*")
    unsigned_integer = re.compile(r"[0-9]+")
    identifier_keyword = re.compile(r"[a-zA-Z]") 
    real_number = re.compile(r"[0-9]+[\.][0-9]+E(\+|-)?[0-9]+")
    white_space = re.compile(r"\s*")
    
    #variable to check if we are inside a comment
    comment = 0
    
    def __init__(self, pascalProgram): 
        #read from the file in LexAnalyzer's constructor
        with open(pascalProgram, 'r') as f:
            self.buf = []
            lines = f.readlines()
            for pos in range(len(lines)): 
                self.buf += [(lines[pos].strip(), pos + 1)]
                
    #Skip white spaces
    def skipWhiteSpace(self, line):
        m = LexAnalyzer.white_space.match(line)
        if m: return(m.end())
        else : return(0)
    
    #Is token Identifier/Keyword?
    def identifierOrKeyword(self, line):
    
        if LexAnalyzer.identifier_keyword.match(line):
            m = LexAnalyzer.identifier.match(line)
            string = line[m.start():m.end()].upper()
            type = "IDENTIFIER"
    
            if string in keywords:
                type = "KEYWORD"
                
            return Token(string, type), m.end()
            
        return None, 0
    
    #Is token Integer? 
    def integer(self, line):
    
        m = LexAnalyzer.unsigned_integer.match(line)
        if m:
            value = line[m.start():m.end()]
            type = "INTEGER"
            return Token(value, type), m.end()
            
        return None, 0
    
    #Is token a Real?
    def real(self, line):
        m = LexAnalyzer.real_number.match(line)
        
        if m:
            value = line[m.start():m.end()]
            type = "REAL"
            return Token(value, type), m.end()
            
        return None, 0
        
    #Function to read comments. Keeps consuming characters as long as it didn't find a closing brace
    def readComment(self, line):
        i = 0
        while(i < len(line) and line[i] != '}'):
            i += 1
            
        return i
    
    #Takes a line, gets tokens from it if it's not a comment (i.e, if a comment was not open in the line before). Else, it skips line
    def tokenize(self, line, lineNumber):
        position = 1 #gives the token's position in the line
        
        while(True):
            #are we still in a comment?
            if self.comment:
                i = self.readComment(line)
                #is the whole line still a comment? if so, move on to next line
                if i >= len(line):
                    return
                else: 
                    #take the part of the line that's not a comment
                    self.comment = 0
                    line = line[i+1:]
                
            flag = 0 #flag for errors
    
            #skips white spaces
            m = self.skipWhiteSpace(line)
            if m >= len(line): 
                break
                
            #Identifier/Keyword
            line = line[m:]
            token, pos =  self.identifierOrKeyword(line)
            if token:
            
                yield(token, position, lineNumber)
                position += 1
                if pos > len(line):
                    break 
                flag = 1
            line = line[pos:]
            
            #Real
            token, pos = self.real(line)
            if token:
                yield(token, position, lineNumber)
                position += 1
                if pos > len(line):
                    break
                flag = 1
            line = line[pos:]
            
            #Integer
            token, pos = self.integer(line)
            if token:
                yield(token, position, lineNumber)
                position += 1
                if pos > len(line): 
                    break
                flag = 1
                
            line = line[pos:]
                
            #Symbols 
            if flag == 0:
                ok = 0
                #checks for comments in the middle of the line
                if line[0] == '{':
                    flag = 1
                    i = self.readComment(line)
                    #if comment does not end at line (multi line comment)
                    if i == len(line):
                        self.comment = 1
                        break
                    else:
                        #if comment ends at line. Split line (take what's left after comment)
                        self.comment = 0
                        if i == len(line)-1: #len - 1 to include the '}' character
                            break
                        line = line[i+1:]
                #if it's not a '{', check if valid symbol
                else:                  
                    if line[0] in symbols:
                        flag = 1
                        yield(Token(str('\''+ line[0] + '\'' + ' '), "SYMBOL"), position, lineNumber) #make the symbol between single quotes
                    else:
                        error = line[0] #take the symbol as an error
                    position += 1
                    line = line[1:]
            
            #Error
            if flag == 0: 
                print("ERROR : Invalid Token : ", error, "in line : ", lineNumber, " position : ", position)
                
    #turns all the tokens found into a list, to allow iteration and printing in main    
    def getTokens(self):
        token_list = []
        for (s, p) in self.buf:
            token_list += list(self.tokenize(s, p))
            
        return filter(lambda x: x, token_list)

        
def main():
    sc = LexAnalyzer("Sample.txt")
    tokens = sc.getTokens()
    print("Token({Type}, {Value})  Line  Position in Line\n")
    for t in tokens:
        token, position, line = t
        print(token.printToken()," Line ", line, "  Position ", position, "\n")
        
if __name__ == "__main__":
    main()
