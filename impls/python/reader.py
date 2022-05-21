import mal_types

class Reader:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0

    def next(self):
        if not self.position < len(self.tokens):
            return None

        old_index = self.position
        self.position = old_index + 1

        return self.tokens[old_index]

    def peek(self):
        if not self.position < len(self.tokens):
            return None

        return self.tokens[self.position]

def read_str(string: str):
    """ This function will call 'tokenize' and then create a new Reader object instance with the tokens
        then it will call 'read_form´ with the Reader instance
    """
    return read_form(Reader(tokenize(string)))

def tokenize(to_tokenize: str):
    """ This function will take a single string and return an array/list of all the tokens (strings) in it.
        For each match captured within the parenthesis starting at char 6 of the regular expression a new token will be created.

        * [\s,]*:              Matches any number of whitespaces or commas. This is not captured so it will be ignored and not tokenized.

        * ~@:                  Captures the special two-characters ~@ (tokenized).

        * [\[\]{}()'`~^@]:     Captures any special single character, one of []{}()'`~^@ (tokenized).

        * "(?:\\.|[^\\"])*"?:  Starts capturing at a double-quote and stops at the next double-quote unless it was preceded by a
                               backslash in which case it includes it until the next double-quote (tokenized). It will also match
                               unbalanced strings (no ending double-quote) which should be reported as an error.

        * ;.*:                 Captures any sequence of characters starting with ; (tokenized).

        * [^\s\[\]{}('"`,;)]*: Captures a sequence of zero or more non special characters (e.g. symbols, numbers, "true", "false",
                               and "nil") and is sort of the inverse of the one above that captures special characters (tokenized).
    """
    tokens = list()

    length = len(to_tokenize)
    index = 0
    token = ""
    while index < length:
        #print("tokenizing index at " + str(index))
        #print("tokenizing char " + str(to_tokenize[index]))
        character = to_tokenize[index]
        match character:
            # ignore whitespace stuff
            case "," | " " | "\n" | "\t":
                if not token == "":
                    new_token = token
                    tokens.append(new_token)
                    token = ""
                index = index+1
                continue

            # capture "~@"
            case "~":
                if not token == "":
                    new_token = token
                    tokens.append(new_token)
                    token = ""
                if index+1 < length and to_tokenize[index+1] == "@":
                    tokens.append("~@")
                    index = index+2
                else:
                    tokens.append(character)
                    index = index+1
                continue

            # capture "special characters"
            case "[" | "]" | "{" | "}" | "(" | ")" | "^" | "'" | "`" | "@":
                #print("current token "+token)
                #print("current char "+character)
                if not token == "":
                    new_token = token
                    tokens.append(new_token)
                    token = ""
                # if character in mal_types.get_mal_symbols():
                #     tokens.append(mal_types.get_mal_symbol(character))
                # else:
                #     tokens.append(character)
                tokens.append(character)
                index = index+1
                continue

            # capture strings
            case '"':
                if not token == "":
                    new_token = token
                    tokens.append(new_token)
                    token = ""

                not_matched = True
                next_index = index + 1
                while(not_matched):
                    matched_index = to_tokenize.find('"', next_index, length)

                    # print("matched_i "+str(matched_index))
                    if matched_index == -1:

                        raise Exception('Error unbalanced "')
                    else:
                        slash_count = to_tokenize.count("\\", next_index, matched_index)
                        if to_tokenize[matched_index - 1] == "\\" and not slash_count % 2 == 0:
                            next_index = matched_index + 1
                        else:
                            tokens.append(to_tokenize[index:matched_index+1])
                            index = matched_index+1
                            not_matched = False
                continue

            # capture comments
            case ";":
                if not token == "":
                    new_token = token
                    tokens.append(new_token)
                    token = ""
                    tokens.append(to_tokenize[index:length])
                break

            # capture until next special character
            case _:
                #print("catching rest")
                token = token + character
                index = index+1
                #print("catching rest token:" + str(token))
                #print("catching rest index: " + str(index) )
                if index < length:
                    continue
                else:
                    tokens.append(token)
                    token = ""
    if not token == "":
        tokens.append(token)

    # print(str(tokens))
    return tokens

def read_form(reader: Reader):
    """ This function will peek at the first token in the Reader object and switch on the first character of that token.
        If the character is a left paren then 'read_list' is called with the Reader object. Otherwise, 'read_atom' is called
        with the Reader Object.

        The return value from read_form is a mal data type.
    """

    match reader.peek():
        case "(":
            the_list = read_list(reader)
            return the_list

        case "{":
            the_map = read_map(reader)
            return the_map

        case "[":
            the_vector = read_vector(reader)
            return the_vector

        case "'" | "`" | "~" | "^" | "@" | "~@":
            the_symbol = read_symbol(reader)
            return the_symbol

        case _:
            atom = read_atom(reader)
            #print ("read_form: atom: "+str(atom))
            return atom

def read_complex_type(reader: Reader, paren_type, mal_type):
    """ This function will repeatedly call read_form with the Reader object until it encounters a ')' token (if it reach
        EOF before reading a ')' then that is an error).

        It accumulates the results into a List type.
    """
    # print("Entering read_list")
    reader.next()
    unmatched = True
    result = list()
    while reader.peek():
        if reader.peek() == paren_type:
            unmatched = False
            reader.next()
            return (mal_type, result)
        else:
            result.append(read_form(reader))

    if unmatched:
        raise Exception("Error unbalanced opening " + paren_type)

def read_list(reader: Reader):
    return read_complex_type(reader, ")", mal_types.MAL_TYPES.MAL_LIST)

def read_map(reader: Reader):
    return read_complex_type(reader, "}", mal_types.MAL_TYPES.MAL_HASH_MAP)

def read_vector(reader: Reader):
    return read_complex_type(reader, "]", mal_types.MAL_TYPES.MAL_VECTOR)

def read_symbol(reader: Reader):
    if reader.peek():
        symbol_token = reader.next()
        symbol_type = mal_types.MAL_TYPES.MAL_SYMBOL

        if symbol_token in mal_types.get_mal_special_symbols():
            return (symbol_type, (symbol_token, read_form(reader)))
        else:
            return (symbol_type, symbol_token)

    raise Exception("unexpected EOF with quote")

def read_atom(reader: Reader):
    """ This function will look at the contents of the token and return the appropriate scalar (simple/single) data type
        value. Initially, you can just implement numbers (integers) and symbols. This will allow you to proceed through
        the next couple of steps before you will need to implement the other fundamental mal types: nil, true, false,
        and string. The remaining scalar mal type, keyword does not need to be implemented until step A (but can be
        implemented at any point between this step and that). BTW, symbols types are just an object that contains a
        single string name value (some languages have symbol types already).
    """
    next_token = reader.next()

    if next_token and next_token[0] == '"':
        return (mal_types.MAL_TYPES.MAL_STRING, str(next_token))
    if next_token == "nil":
        return (mal_types.MAL_TYPES.MAL_NIL, next_token)
    if next_token == "true" or next_token == "false":
        return (mal_types.MAL_TYPES.MAL_BOOLEAN, next_token)

    # FIXME: add other number types
    try:
        int_value = int(next_token)
        return (mal_types.MAL_TYPES.MAL_NUMBER, int_value)
    except:
        pass

    return (mal_types.MAL_TYPES.MAL_SYMBOL, str(next_token))
