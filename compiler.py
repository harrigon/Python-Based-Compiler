import re
import sys


class Scanner:
    '''The interface comprises the methods lookahead and consume.
       Other methods should not be called from outside of this class.'''

    def __init__(self, input_file):
        '''Reads the whole input_file to input_string, which remains constant.
           current_char_index counts how many characters of input_string have
           been consumed.
           current_token holds the most recently found token and the
           corresponding part of input_string.'''
        self.input_string = input_file.read()
        self.current_char_index = 0
        self.current_token = self.get_token()

    def skip_white_space(self):
        '''Consumes all characters in input_string up to the next
           non-white-space character.'''

        while self.current_char_index < len(self.input_string):
            if (self.input_string[self.current_char_index] in [' ', '\n', '\t']) == False:
                break
            else:
                self.current_char_index += 1        

    def no_token(self):
        '''Stop execution if the input cannot be matched to a token.'''
        print('lexical error: no token found at the start of ' +
              self.input_string[self.current_char_index:])
        exit()

    def get_token(self):
        '''Returns the next token and the part of input_string it matched.
           The returned token is None if there is no next token.
           The characters up to the end of the token are consumed.
           TODO:
           Raise an exception by calling no_token() if the input contains
           extra non-white-space characters that do not match any token.'''
        self.skip_white_space()
        token, longest = None, ''
        for (t, r) in Token.token_regexp:
            match = re.match(r, self.input_string[self.current_char_index:])

            if match and match.end() > len(longest):
                token, longest = t, match.group()
            
        if token == None and self.current_char_index < len(self.input_string):
            #me trying not to fuck it up
            self.no_token()
        else:
            self.current_char_index += len(longest)
            return (token, longest)

    def lookahead(self):
        '''Returns the next token without consuming it.
           Returns None if there is no next token.'''
        return self.current_token[0]

    def unexpected_token(self, found_token, expected_tokens):
        '''Stop execution if an unexpected token is found.'''
        print('syntax error: token in ' + repr(expected_tokens) +
              ' expected but ' + repr(found_token) + ' found')
        exit()

    def consume(self, *expected_tokens):
        '''Returns the next token and consumes it, if it is in
           expected_tokens. Calls unexpected_token(...) otherwise.
           If the token is a number or an identifier, not just the
           token but a pair of the token and its value is returned.'''
        
        
        current_token = self.current_token
        if current_token[0] in expected_tokens:
            self.current_token = self.get_token()
            if current_token[0] == 'NUM' or current_token[0] == 'ID': 
                return current_token[0], current_token[1]
            else:
                return current_token[0]
        
        else:
            self.unexpected_token(self.current_token[0], expected_tokens)


class Token:
    # The following enumerates all tokens.
    DO    = 'DO'
    ELSE  = 'ELSE'
    END   = 'END'
    IF    = 'IF'
    THEN  = 'THEN'
    WHILE = 'WHILE'
    READ  = 'READ'#I did this   
    WRITE = 'WRITE' #I did this     
    SEM   = 'SEM'
    BEC   = 'BEC'
    LESS  = 'LESS'
    EQ    = 'EQ'
    GRTR  = 'GRTR'
    LEQ   = 'LEQ'
    NEQ   = 'NEQ'
    GEQ   = 'GEQ'
    ADD   = 'ADD'
    SUB   = 'SUB'
    MUL   = 'MUL'
    DIV   = 'DIV'
    LPAR  = 'LPAR'
    RPAR  = 'RPAR'    
    NUM   = 'NUM'
    ID    = 'ID'
    AND   = 'AND'##BOOLEAN
    NOT   = 'NOT'##BOOLEAN
    OR    = 'OR'  ##BOOLEAN  


    # The following list gives the regular expression to match a token.
    # The order in the list matters for mimicking Flex behaviour.
    # Longer matches are preferred over shorter ones.
    # For same-length matches, the first in the list is preferred.
    token_regexp = [
        (DO,    'do'),
        (READ,  'read'),
        (WRITE, 'write'),
        (ELSE,  'else'),
        (END,   'end'),
        (IF,    'if'),
        (THEN,  'then'),
        (WHILE, 'while'),
        (AND,   'and'), ##BOOLEAN
        (NOT,   'not'),##BOOLEAN
        (OR,    'or'), ##BOOLEAN
        (SEM,   ';'),
        (BEC,   ':='),
        (LESS,  '<'),
        (EQ,    '='),
        (GRTR,  '>'),
        (LEQ,   '<='),  
        (NEQ,   '!='),##I DID THIS
        (GEQ,   '>='),
        (ADD,   '\\+'), # + is special in regular expressions
        (SUB,   '-'),
        (MUL,   '\\*'),##I DID THIS AND PUT IN \\ AS SPECIAL CHARACTERS
        (DIV,   '/'),##I DID THIS
        (LPAR,  '\\('), # ( is special in regular expressions
        (RPAR,  '\\)'), # ) is special in regular expressions
        (NUM,   '[0-9]+'),##I DID THIS
        (ID,    '[a-z]+'),
    ]

class Symbol_Table:
    '''A symbol table maps identifiers to locations.'''
    def __init__(self):
        self.symbol_table = {}
    def size(self):
        '''Returns the number of entries in the symbol table.'''
        return len(self.symbol_table)
    def location(self, identifier):
        '''Returns the location of an identifier. If the identifier is not in
           the symbol table, it is entered with a new location. Locations are
           numbered sequentially starting with 0.'''
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        index = len(self.symbol_table)
        self.symbol_table[identifier] = index
        return index

class Label:
    def __init__(self):
        self.current_label = 0
    def next(self):
        '''Returns a new, unique label.'''
        self.current_label += 1
        return 'l' + str(self.current_label)

def indent(s, level):
    return '    '*level + s + '\n'

class Program_AST:
    def __init__(self, program):
        self.program = program
    def __repr__(self):
        return repr(self.program)
    def indented(self, level):
        return self.program.indented(level)
    def code(self):
        program = self.program.code()
        local = symbol_table.size()
        java_scanner = symbol_table.location('Java Scanner')
        
        ##Dont even bother
        return '.class public Program\n' + \
               '.super java/lang/Object\n' + \
               '.method public <init>()V\n' + \
               'aload_0\n' + \
               'invokenonvirtual java/lang/Object/<init>()V\n' + \
               'return\n' + \
               '.end method\n' + \
               '.method public static main([Ljava/lang/String;)V\n' + \
               '.limit locals ' + str(local) + '\n' + \
               '.limit stack 1024\n' + \
               'new java/util/Scanner\n' + \
               'dup\n' + \
               'getstatic java/lang/System.in Ljava/io/InputStream;\n' + \
               'invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V\n' + \
               'astore ' + str(java_scanner) + '\n' + \
               program + \
               'return\n' + \
               '.end method\n'
    #----------------------------------------Not to worry^^^^Not my problem

class Statements_AST:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result
    def indented(self, level):
        result = indent('Statements', level)
        for st in self.statements:
            result += st.indented(level+1)
        return result
    def code(self):
        result = ''
        for st in self.statements:
            result += st.code()
        return result

class If_AST:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
                       repr(self.then) + ' end'
    def indented(self, level):
        return indent('If', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        return self.condition.false_code(l1) + \
               self.then.code() + \
               l1 + ':\n'
#here --------------------------------------------------------------------#
class If_Else_AST:
    def __init__(self, condition, then, else_then):
        self.condition = condition
        self.then = then
        self.else_then = else_then
        
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
               repr(self.then) + ' else ' + repr(self.else_then)
    
    def indented(self, level):
        #return indent('If', level) + \
               #self.condition.indented(level+1) + \
               #self.then.indented(level+1)        
        return indent('If-Else', level) + self.condition.indented(level+1) + \
        self.then.indented(level+1) + self.else_then.indented(level+1)
    
    def code(self):
        myl1 = label_generator.next()##HERE FOR ERRORS
        myl2 = label_generator.next()
        return self.condition.false_code(myl1) + self.then.code() + 'goto ' + myl2 + '\n' + myl1 + ':\n' +\
               self.else_then.code() + myl2 + ':\n'
#here --------------------------------------------------------------------#

class While_AST:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        
    def __repr__(self):
        return 'while ' + repr(self.condition) + ' do ' + \
                          repr(self.body) + ' end'
    def indented(self, level):
        return indent('While', level) + \
               self.condition.indented(level+1) + \
               self.body.indented(level+1)
    
    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        return l1 + ':\n' + \
               self.condition.false_code(l2) + \
               self.body.code() + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'

class Assign_AST:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        
    def __repr__(self):
        return repr(self.identifier) + ':=' + repr(self.expression)
    
    def indented(self, level):
        return indent('Assign', level) + \
               self.identifier.indented(level+1) + \
               self.expression.indented(level+1)
    
    def code(self):
        loc = symbol_table.location(self.identifier.identifier)
        return self.expression.code() + \
               'istore ' + str(loc) + '\n'

class Write_AST:
    def __init__(self, expression):
        self.expression = expression      
    def __repr__(self):
        return 'write ' + repr(self.expression)   
    def indented(self, level):
        return indent('Write', level) + self.expression.indented(level+1)
    def code(self):
        #-----------------------------------What the actual fuck
        #dont bother,move on
        return 'getstatic java/lang/System/out Ljava/io/PrintStream;\n' + \
               self.expression.code() + \
               'invokestatic java/lang/String/valueOf(I)Ljava/lang/String;\n' + \
               'invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n'

class Read_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return 'read ' + repr(self.identifier)
    def indented(self, level):
        return indent('Read', level) + self.identifier.indented(level+1)
    def code(self):
        java_scanner = symbol_table.location('Java Scanner')
        loc = symbol_table.location(self.identifier.identifier)
        return 'aload ' + str(java_scanner) + '\n' + \
               'invokevirtual java/util/Scanner.nextInt()I\n' + \
               'istore ' + str(loc) + '\n'

class Comparison_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        op = { Token.LESS:'<', Token.EQ:'=', Token.GRTR:'>',
               Token.LEQ:'<=', Token.NEQ:'!=', Token.GEQ:'>=' }
        return repr(self.left) + op[self.op] + repr(self.right)
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def true_code(self, label):
        op = { Token.LESS:'if_icmplt', Token.EQ:'if_icmpeq',
               Token.GRTR:'if_icmpgt', Token.LEQ:'if_icmple',
               Token.NEQ:'if_icmpne', Token.GEQ:'if_icmpge' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    def false_code(self, label):
        # Negate each comparison because of jump to "false" label.
        op = { Token.LESS:'if_icmpge', Token.EQ:'if_icmpne',
               Token.GRTR:'if_icmple', Token.LEQ:'if_icmpgt',
               Token.NEQ:'if_icmpeq', Token.GEQ:'if_icmplt' }
        ##print(op)
        #print(self.left.code() + \
                       #self.right.code() + \
                       #op[self.op] + ' ' + label + '\n')        
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    
class Boolean_Expression_AST:
    # the or boolean, then goes to next
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __repr__(self):
        return repr(self.left) + 'or' + repr(self.right)
    
    def __indented__(self, level):
        return indent(Token.OR, level) + self.left.indented(level+1) + self.right.indented(level+1)
    
    def true_code(self, label):
        #base
        return self.left.true_code(label) + self.right.true_code(label)
            
    def false_code(self, label):
        l1 = label
        #The same can jump again
        l2 = label_generator.next()
        return self.left.true_code(l2) + self.right.false_code(l1) + l2 + ':\n'

        
class Boolean_Term_AST:
    ## the and boolean, then goes to next
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __repr__(self):
        return repr(self.left) + 'and' + repr(self.right)
    
    def __indented__(self, level):
        return indent(Token.AND, level) + self.left.indented(level+1) + self.right.indented(level+1)
    
    def true_code(self, label):
        ##print("lable", label)
        l1 = label #l1 if valid
        #same dont matter can jump
        l2 = label_generator.next() #l2 if invalid
        return self.left.false_code(l2) + self.right.true_code(l1) + l2 + ':\n'
    
    def false_code(self, label):
        return self.left.false_code(label) + self.right.false_code(label)
    
            
class Boolean_Factor_AST:
    # the not boolean
    def __init__(self, expression):
        self.expression = expression
        
    def __repr__(self):
        return 'not' + repr(self.expression)
    
    def true_code(self, l1):
        return self.expression.false_code(l1)
    
    def false_code(self, l1):
        return self.expression.true_code(l1)

class Expression_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        op = { Token.ADD:'+', Token.SUB:'-', Token.MUL:'*', Token.DIV:'/' }
        return '(' + repr(self.left) + op[self.op] + repr(self.right) + ')'
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + self.right.indented(level+1)
    def code(self):
        op = { Token.ADD:'iadd', Token.SUB:'isub',
               Token.MUL:'imul', Token.DIV:'idiv' }
        return self.left.code() + self.right.code() + op[self.op] + '\n'

class Number_AST:
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return self.number
    def indented(self, level):
        return indent(self.number, level)
    def code(self): # works only for short numbers
        return 'sipush ' + self.number + '\n'

class Identifier_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return self.identifier
    def indented(self, level):
        return indent(self.identifier, level)
    def code(self):
        loc = symbol_table.location(self.identifier)
        return 'iload ' + str(loc) + '\n'


def program():
    sts = statements()
    return Program_AST(sts)

def statements():
    result = [statement()]
    while scanner.lookahead() == Token.SEM:
        scanner.consume(Token.SEM)
        st = statement()
        result.append(st)
    return Statements_AST(result)

def statement():
    if scanner.lookahead() == Token.IF:
        return if_statement()
    elif scanner.lookahead() == Token.WHILE:
        return while_statement()
    elif scanner.lookahead() == Token.ID:
        return assignment()
    elif scanner.lookahead() == Token.WRITE:
        return write()
    elif scanner.lookahead() == Token.READ:
        return read()
    else: # error
        return scanner.consume(Token.IF, Token.WHILE, Token.ID, Token.READ, Token.WRITE)

def if_statement():
    #print(scanner.get_token())
    scanner.consume(Token.IF)
    boolean_condition = boolean_expression() #replaced comparison for If/If_Else
    scanner.consume(Token.THEN)
    then = statements()
    
    if scanner.lookahead() == Token.ELSE:
        scanner.consume(Token.ELSE)
        else_ = statements()
        scanner.consume(Token.END)
        return If_Else_AST(boolean_condition, then, else_)
    
    else:
        scanner.consume(Token.END)
        return If_AST(boolean_condition, then)

def while_statement():
    scanner.consume(Token.WHILE)
    boolean_condition = boolean_expression() #replace comparison for while_do
    scanner.consume(Token.DO)
    body = statements()
    scanner.consume(Token.END)
    
    return While_AST(boolean_condition, body)

def assignment():
    ident = identifier()
    scanner.consume(Token.BEC)
    expr = expression()
    return Assign_AST(ident, expr)

def write():
    scanner.consume(Token.WRITE)
    expr = expression()
    return Write_AST(expr)

def read():
    scanner.consume(Token.READ)
    ident = identifier()
    return Read_AST(ident)

def comparison():
    left = expression()
    op = scanner.consume(Token.LESS, Token.EQ, Token.GRTR,
                         Token.LEQ, Token.NEQ, Token.GEQ)
    right = expression()
    return Comparison_AST(left, op, right)

def expression():
    result = term()
    while scanner.lookahead() in [Token.ADD, Token.SUB]:
        op = scanner.consume(Token.ADD, Token.SUB)
        tree = term()
        result = Expression_AST(result, op, tree)
    return result

def term():
    result = factor()
    while scanner.lookahead() in [Token.MUL, Token.DIV]:
        op = scanner.consume(Token.MUL, Token.DIV)
        tree = factor()
        result = Expression_AST(result, op, tree)
    return result

def factor():
    if scanner.lookahead() == Token.LPAR:
        scanner.consume(Token.LPAR)
        result = expression()
        scanner.consume(Token.RPAR)
        return result
    elif scanner.lookahead() == Token.NUM:
        value = scanner.consume(Token.NUM)[1]
        return Number_AST(value)
    elif scanner.lookahead() == Token.ID:
        return identifier()
    else: # error
        return scanner.consume(Token.LPAR, Token.NUM, Token.ID)

def identifier():
    value = scanner.consume(Token.ID)[1]
    return Identifier_AST(value)

#Following classes for extending the syntax:
#BooleanExpression = BooleanTerm (or BooleanTerm)*
#BooleanTerm = BooleanFactor (and BooleanFactor)*
#BooleanFactor = not BooleanFactor | Comparison

def boolean_expression():
    output = boolean_term()
    
    while scanner.lookahead() == Token.OR: #BooleanExpression = BooleanTerm (or BooleanTerm)*
        scanner.consume(Token.OR)
        output = Boolean_Expression_AST(output, boolean_term())
    return output

def boolean_term():
    output = boolean_factor()
    
    while scanner.lookahead() == Token.AND: #BooleanTerm = BooleanFactor (and BooleanFactor)*
        scanner.consume(Token.AND)
        output = Boolean_Term_AST(output, boolean_factor())
    return output

def boolean_factor():
    
    if scanner.lookahead() == Token.NOT: #BooleanFactor = not BooleanFactor | Comparison
        scanner.consume(Token.NOT)
        return Boolean_Factor_AST(boolean_factor()) #| Compariison part
    
    else:
        return comparison()
    

# Initialise scanner, symbol table and label generator.

scanner = Scanner(sys.stdin)
symbol_table = Symbol_Table()
symbol_table.location('Java Scanner') # fix a location for the Java Scanner
label_generator = Label()

# Uncomment the following to test the scanner without the parser.
# Show all tokens in the input.
#
##token = scanner.lookahead()
##while token != None:
    ##if token in [Token.NUM, Token.ID]:
        ##token, value = scanner.consume(token)
        ##print(token, value)
    ##else:
        ##print(scanner.consume(token))
    ##token = scanner.lookahead()
##exit()

# -------------------------------------------------------Call the parser.

ast = program()
if scanner.lookahead() != None:
    print('syntax error: end of input expected but token ' +
          repr(scanner.lookahead()) + ' found')
    exit()


#print(ast.indented(0), end='')
#exit()


print(ast.code(), end='')


