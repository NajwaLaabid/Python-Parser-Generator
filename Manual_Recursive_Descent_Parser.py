# LL(1) Parser :
# - Input : file of tokens from lexical analyzer
# - Output : accept or rejet
# - Code : direct implementation of modified grammar


import sys

class Parser:
    def __init__(self, tokenStream):
        with open(tokenStream, 'r') as f:
            self.lines = f.readlines()
            
    def accept(self):
        print("PROGRAM ACCEPTED\n")
        
    def reject(self):
        print("PROGRAM REJECTED\n")  #add why?
            
    def Lex(self):
        self.lines = self.lines[1:]
        print self.lines[0]
        
    def nextToken(self):
        type = self.lines[0].split()[0].strip()
        value = self.lines[0].split()[1].strip()
        if(type == "KEYWORD"):
            return value
        else :
            return type
         #if it's a keyword, return value. else return type

    def sign(self):
        if(self.nextToken() != '+' and self.nextToken() != '-'):
            self.reject()    

    def factor_next(self):
        if (self.nextToken() == 'OPEN_PARENT'):
            self.Lex()
            self.expression_list()
            if(self.nextToken() == 'CLOSE_PARENT'):
                return 1
            else:
                self.reject()
        elif(self.nextToken() == 'MULOP' or self.nextToken() == 'ADDOP' or self.nextToken() == 'CLOSE_BRACE' or self.nextToken() == 'SEMICOLON' or self.nextToken() == 'END'):
            return 1
        else:
            self.reject()                

    def factor(self):
        if(self.nextToken() == 'IDENTIFIER'):
            self.Lex()
            self.factor_next()
        elif(self.nextToken() == 'OPEN_PARENT'):
            self.Lex()
            self.expression()
            if(self.nextToken() == 'CLOSE_PARENT'):
                #self.Lex()
                return 1
            else:
                self.reject()    
        elif(self.nextToken() == 'NOT'):
            self.Lex()
            self.factor()
        elif(self.nextToken() == 'INTEGER'):
            self.Lex() #not sure about this
            return 1
        else:
        	print "torture"
        	self.reject()                

    def term_next(self):
        if(self.nextToken() == 'MULOP'):
            self.Lex()
            term()
        elif(self.nextToken() == 'ADDOP' or self.nextToken() == 'CLOSE_BRACE' or self.nextToken() == 'SEMICOLON' or self.nextToken() == 'END' or self.nextToken() == 'THEN'):
            return 1
        else:
        	print "enouuugh"
        	self.reject()        


    def term(self):
    	self.Lex()
        self.factor()
        self.term_next()

    def simple_expression(self):
        if(self.nextToken() == '+' or self.nextToken() == '-'):#check if we will need to c1ll lex() before
            self.Lex()
            self.sign()
            self.term()
        elif(self.nextToken() == 'IDENTIFIER' or self.nextToken() == 'NUM' or self.nextToken() == 'NOT' or self.nextToken() == 'OPEN_PARENT'):
            self.Lex()
            self.term()
            if(self.nextToken() == 'ADDOP'):
                simple_expression()
            else:
                return 1
        else:
        	print "y u do dis??"
        	self.reject()           

    def expresion_next(self):
        if(self.nextToken() == 'RELOP'):
            self.Lex()
            self.simple_expression()
        elif(self.nextToken() == 'SEMICOLON' or self.nextToken() == 'CLOSE_PARENT' or self.nextToken() == 'CLOSE_BRACE' or self.nextToken() == 'SEMICOLON' or self.nextToken() == 'END' or self.nextToken() == 'IDENTIFIER' or self.nextToken() == 'THEN'):#TO CHECK:
            return 1
        else:
        	print "prog rejceted"
        	self.reject()
        	return 0     

    def expression(self):
    	#self.Lex()
        self.simple_expression()
        print "first " + self.nextToken()
        #self.Lex()
        print "second " + self.nextToken()
        self.expresion_next()
        print "thirsd " + self.nextToken()

    def expression_list_next(self):
        if(self.nextToken() == ','):
            self.Lex()
            self.expression_list()
        elif(self.nextToken() == 'CLOSE_PARENT'):
            return 1
        else:
        	self.reject()     

    def expression_list(self):
        self.expression()
        self.expression_list_next()

    def assignop(self):
    	if (self.nextToken() == 'COLON'):
    		self.Lex()
    		if (self.nextToken() == 'EQUAL'):
    			self.Lex()
    			return
    	elif(self.nextToken() != 'EQUAL'):
    		self.reject() 

    def var_or_proc(self): ####TAKE CARE OF EPSILON
        if(self.nextToken() == 'OPEN_PARENT'):
            self.Lex()
            self.expression_list()
            if(self.nextToken() == 'CLOSE_PARENT'):
                self.Lex()
                return 1
            else:
                self.reject()
                return 0
        elif(self.nextToken() == 'OPEN_BRACE'):
            self.Lex()
            self.expression()
            if(self.nextToken() == 'CLOSE_PARENT'):
                self.Lex()
                self.assignop()
                self.expression()
                return 1
            else:
            	self.reject()
            	return 0
        elif (self.nextToken() == ':'):
        	self.assignop()    	
        else:
        	self.assignop()
        	self.expression()
        
    def statement(self):
        if(self.nextToken() == 'IDENTIFIER'):
            self.Lex()
            self.var_or_proc()
            return
        elif(self.nextToken() == 'IF'):
            self.Lex()
            self.expression()
            print self.nextToken()
            if(self.nextToken() == 'THEN'):
                self.Lex()
                self.statement()
                if(self.nextToken() == 'ELSE'):
                    self.Lex()
                    self.statement()
                    return 1
                else:
                	self.reject()
            else:
            	self.reject()
        elif(self.nextToken() == 'WHILE'):
            self.Lex()
            self.expression()
            if(self.nextToken() == 'DO'):
                self.statement()
            else:
            	self.reject()
        else:
            self.compound_statement()
            
    def statement_list_next(self):
        if(self.nextToken() == 'SEMICOLON'):
            self.Lex()
            self.statement_list()
        elif(self.nextToken() == 'END'):
            return 1
        else:
            self.reject()
            return 0
            
    def statement_list(self):
        self.statement()
        self.statement_list_next()
        
    def compound_statement_next(self):
        if(self.nextToken() == 'END'):
            self.Lex()
            return 1
        else:
        	self.statement_list()
        	if(self.nextToken() == 'END'):
        		self.Lex()
        		return 1
        	else:
        		self.reject()
        		return 0	
            
                
    def compound_statement(self):
        if(self.nextToken() == 'BEGIN'):
            self.Lex()
            self.compound_statement_next()
            return 1
        else:
        	self.reject()
        	return 0
            
    def parameter_list_next(self):
        if(self.nextToken() == 'SEMICOLON'):
            self.Lex()
            self.parameter_list()
            self.Lex()
        elif(self.nextToken() == 'CLOSE_PARENT'):
            return 1
        else:
        	self.reject
        	return 0

    def parameter_list(self):
        self.identifier_list()
        if(self.nextToken() == 'COLON'):
            self.Lex()
            self.type()
            self.Lex()
            self.parameter_list_next()
            return 1
        else:
        	self.reject()
        	return 0
        
    def arguments(self):
        if(self.nextToken() == 'OPEN_PARENT'):
            self.Lex()
            self.parameter_list()
            if(self.nextToken() == 'CLOSE_PARENT'):
                self.Lex()
                return 1
            else:
            	print "ici"
                self.reject()
                return 0
        elif(self.nextToken() == 'SEMICOLON'):
            return 1
        elif(self.nextToken() == 'COLON'): ####to checkkk
            return 1    
        else:
            self.reject()
            return 0
            
    def subprogram_head(self):
        if(self.nextToken() == 'FUNCTION'):
            self.Lex()
            if(self.nextToken() == 'IDENTIFIER'):
                self.Lex()
                self.arguments()
                if(self.nextToken() == 'COLON'):
                    self.Lex()
                    self.standard_type()
                    self.Lex()
                    if(self.nextToken() == 'SEMICOLON'):
                        self.Lex()
                        return 1
                    else:
                        self.reject()
                        return 0
                else:
                    self.reject()
                    return 0
            else:
                self.reject()
                return 0
        elif(self.nextToken() == 'PROCEDURE'):
            self.Lex()
            if(self.nextToken() == 'IDENTIFIER'):
                self.Lex()
                self.arguments()
                if(self.nextToken == 'SEMICOLON'):
                    self.Lex()
                    return 1
                else:
                    self.reject()
                    return 0
            else:
                self.reject()
                return 0        
        else:
        	self.reject()
        	return 0
                
    def subprogram_declaration(self):
        self.subprogram_head()
        self.declarations()
        self.compound_statement()
    
    def subprogram_declaration_next(self):
        if(self.nextToken() == 'BEGIN'):
            return 1
        if(self.nextToken() == 'SEMICOLON'):
            self.subprogram_declarations()
        else:
        	self.reject()
        	return 0
        
    def subprogram_declarations(self):
        self.subprogram_declaration()
        self.subprogram_declaration_next()
         
    def standard_type(self):
        if(self.nextToken() != 'INTEGER' and self.nextToken() != 'REAL'):
            self.reject()  
               
    def type(self):
        if(self.nextToken() == 'ARRAY'):
            self.Lex()
            if(self.nextToken() == 'OPEN_BRACE'):
                self.Lex()
                if(self.nextToken() == 'NUM'):
                    if(self.nextToken() == 'DOT'):
                        self.Lex()
                    else:
                        self.reject()
                    if(self.nextToken() == 'DOT'):
                        self.Lex()
                    else:
                        self.reject()
                    if(self.nextToken() == 'NUM'):
                        self.Lex()
                        if(self.nextToken() == 'CLOSE_BRACE'):
                            self.Lex()
                            if(self.nextToken() == 'of'):
                                self.Lex()
                                self.standard_type()
                            else:
                                self.reject()
                        else:
                            self.reject()
                    else:
                        self.reject()
                else:
                    self.reject()
            else:
                self.reject()
        else:
            self.standard_type()
            
    def declarations(self):
        if(self.nextToken() == 'FUNCTION' or self.nextToken == 'PROCEDURE'):
            return 1
        elif(self.nextToken() == 'VAR'):
            self.Lex()
            self.identifier_list()
            if(self.nextToken() == 'COLON'):
                self.Lex()
                self.type()
                self.Lex()
                if(self.nextToken() == 'SEMICOLON'):
                    self.Lex()
                    self.declarations()
                else:
                    self.reject()
                    return 0
            else:
                self.reject()
                return 0
        elif(self.nextToken() == 'BEGIN'):
        	return 1         
        else:
            self.reject()
    
    def identifier_list_next(self):
        if(self.nextToken() == 'COMA'):
            self.Lex()
            self.identifier_list()
        elif(self.nextToken() == 'CLOSE_PARENT' or self.nextToken() == 'COLON'): #to check by cAses set flAg or smtg
            return  #can work empty? try break?
            
    def identifier_list(self):
        if(self.nextToken() == 'IDENTIFIER'):
            self.Lex()
            self.identifier_list_next()
            return
        else:
            self.reject()
         
    def program(self):
        if(self.nextToken() == 'PROGRAM'):
            self.Lex()
            if(self.nextToken() == 'IDENTIFIER'):
                self.Lex()
                if(self.nextToken() == 'OPEN_PARENT'):
                    self.Lex()
                    self.identifier_list() #self.Lex() inside

                    if(self.nextToken() == 'CLOSE_PARENT'):
                        self.Lex()
                        if(self.nextToken() == 'SEMICOLON'):
                            self.Lex()
                            self.declarations()
                            self.subprogram_declarations()
                            self.compound_statement()
                            if(self.nextToken() == 'DOT'):
                            	self.accept()  
								return 1
                            else:
                            	self.reject()
								return 0
                        else:
                            self.reject()
							return 0
                    else:
                        self.reject()
						return 0
                else:
                    self.reject()
					return 0
            else:
                self.reject()
				return 0
        else:
            self.reject()
			return 0
    
    def parser(self):
        self.program()
    

def main():
    prs = Parser("tokenStream.txt")
    prs.parser()
        
if __name__ == "__main__":
    main()
        
