import math

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INT, FLOAT, PLUS, MINUS, MUL, DIV, PARENTHESIS, RPARENTHESIS, ASSIGNMENT, VAR, LESS, GREATER, EQUAL, LESSEQUAL, GREATEREQUAL, SIN, COS, TAN, CTG, SQRT, POW, LOG, EOF = (
'INT', 'FLOAT', 'PLUS', 'MINUS', 'MUL', 'DIV', 'PARENTHESIS', 'RPARENTHESIS', 'ASSIGNMENT', 'VAR', 'LESS', 'GREATER', 'EQUAL', 'LESSEQUAL', 'GREATEREQUAL', 'SIN', 'COS', 'TAN', 'CTG', 'SQRT', 'POW', 'LOG', 'EOF'
)

FUNCTIONS = [SIN, COS, TAN, CTG, SQRT, POW, LOG]
FUNC_DICT = {
    SIN : math.sin,
    COS : math.cos,
    TAN : math.tan,
    CTG : lambda x: 1/math.tan(x),
    SQRT: math.sqrt,
    POW : lambda x: math.pow(2, x),
    LOG : math.log
}
variables = dict()



class Token(object):
    def __init__(self, type, value):
        # token type: INT, PLUS, MINUS, MUL, DIV ...
        self.type = type
        # token value: non-negative integer value, '+', '-', '*', '/', ...
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INT, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, msg):
        raise Exception('Lexer exception:', msg)

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # def integer(self):
    #     """Return a (multidigit) integer consumed from the input."""
    #     result = ''
    #     while self.current_char is not None and self.current_char.isdigit():
    #         result += self.current_char
    #         self.advance()
    #     return int(result)

    def reset_pos(self):
        self.pos = 0
        self.current_char = self.text[self.pos]

    def handle_digit(self):
        """Return a (multidigit) integer or float."""
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        if result.count('.') == 0:
            return Token(INT, int(result))
        elif result.count('.') == 1:
            return Token(FLOAT, float(result))
        else:
            self.error('More then one . in number...')
    
    def handle_letter(self):
        """Return a variable or function"""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if self.current_char == '(':
            if result in FUNCTIONS:
                return Token(result, result)
            else:
                self.error('Invalid function name...')
        else:
            return Token(VAR, result)
        
    def handle_equal(self):
        """Return = or =="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(EQUAL, '==')
        else:
            return Token(ASSIGNMENT, '=')
            
    def handle_less(self):
        """Return < or <="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(LESSEQUAL, '<=')
        else:
            return Token(LESS, '<')
            
    def handle_greater(self):
        """Return > or >="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(GREATEREQUAL, '>=')
        else:
            return Token(GREATER, '=')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.handle_digit()

            if self.current_char.isalpha():
                return self.handle_letter()

            if self.current_char == '=':
                return self.handle_equal()
            if self.current_char == '<':
                return self.handle_less()
            if self.current_char == '>':
                return self.handle_greater()

            token = None

            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
            elif self.current_char == '-':
                token = Token(MINUS, self.current_char)
            elif self.current_char == '*':
                token = Token(MUL, self.current_char)
            elif self.current_char == '/':
                token = Token(DIV, self.current_char)
            elif self.current_char == '(':
                token = Token(PARENTHESIS, self.current_char)
            elif self.current_char == ')':
                token = Token(RPARENTHESIS, self.current_char)
            else:
                self.error('Invalid character...')

            self.advance()
            return token

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, msg):
        raise Exception('Interpreter error:', msg)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error('Tokens dont match...')

    def paran_expr(self):
        result = self.expr()
        self.eat(RPARENTHESIS)
        return result
        # if self.current_token.type == PARENTHESIS:
        #     self.eat(PARENTHESIS)
        #     result = self.paran_expr()
        #     # maybe
        #     # self.eat(RPARENTHESIS)
        # else:
        #     result = self.factor()

        # while self.current_token.type != RPARENTHESIS: # a sta ako dodje do kraja
        #     if self.current_token.type in FUNCTIONS:
        #         func = self.current_token.type;
        #         self.eat(func)
        #         result = self.apply_token(last_token, result, FUNC_DICT[func](self.paran_expr()))
        #     elif self.current_token.type in (PLUS, MINUS, MUL, DIV):
        #         last_token = self.current_token
                
        #     last_token = self.current_token

        return result

    def factor(self):
        token = self.current_token
        if token.type == INT:
            self.eat(INT)
            return token.value
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return token.value
        elif token.type == VAR:
            self.eat(VAR)
            if token.value not in variables:
                self.error('Varible ' + token.value + ' used before asignment...')
            return variables[token.value]
        elif token.type == PARENTHESIS:
            self.eat(PARENTHESIS)
            return self.paran_expr()
        else:
            self.error(str(token) + ' is not a primitive type...')

    def func_factor(self):
        token = self.current_token

        if token.type in FUNCTIONS:
            self.eat(token.type)
            return FUNC_DICT[token.type](self.factor())
        return self.factor()

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.func_factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.func_factor()
            elif token.type == DIV:
                self.eat(DIV)
                next_factor = self.func_factor()
                if isinstance(result, int) and isinstance(next_factor, int):
                    result = int(result / next_factor)
                else:
                    result = result / next_factor

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

    def logical_expr(self):
        result = left_side = self.expr()
        token = self.current_token

        if token.type in (LESS, LESSEQUAL, GREATER, GREATEREQUAL, EQUAL):
            self.eat(token.type)
            right_side = self.expr()
            if token.type == LESS:
                result = left_side < right_side
            if token.type == LESSEQUAL:
                result = left_side <= right_side
            if token.type == GREATER:
                result = left_side > right_side
            if token.type == GREATEREQUAL:
                result = left_side >= right_side
            if token.type == EQUAL:
                result = left_side == right_side

        if self.current_token.type != EOF:
            self.error('Invalid statement at end...')

        return result

    def statement(self):
        """Arithmetic expression parser / interpreter.

        statemet    : (VAR ASSIGNMENT)? logical_expr
        logical_expr: expr ((LESS | LESSEQUAL | GREATER | GREATEREQUAL | EQUAL) expr)?
        expr        : term ((PLUS | MINUS) term)*
        term        : factor ((MUL | DIV) factor)*
        func_factor : (FUNCTION)? factor
        factor      : (INT | FLOAT | VAR | paran_expr)
        paran_expr  : (PARENTHESIS) expr (RPARENTHESIS)

        """

        first_token = self.current_token
        if first_token.type == VAR:
            self.eat(VAR)
            second_token = self.current_token

            if second_token.type == ASSIGNMENT:
                self.eat(ASSIGNMENT)
                new_var_val = self.logical_expr()
                variables[first_token.value] = new_var_val
                return None
            else:
                self.lexer.reset_pos()
                self.current_token = self.lexer.get_next_token()
        
        return self.logical_expr()

def main():
    while True:
        try:
            text = input('rafmat: ')
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue
        if text == 'EXIT' or text == 'q':
            break
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.statement()
        if result != None:
            print(result)


if __name__ == '__main__':
    main()