import reader
import printer
import mal_types

PROMPT = "user> "

repl_env = {'+': lambda a,b: (mal_types.get_mal_type("number"), a[1]+b[1]),
            '-': lambda a,b: (mal_types.get_mal_type("number"), a[1]-b[1]),
            '*': lambda a,b: (mal_types.get_mal_type("number"), a[1]*b[1]),
            '/': lambda a,b: (mal_types.get_mal_type("number"), int(a[1]/b[1]))}

def eval_ast(ast, repl_env):

    mal_type = ast[0]

    match mal_type:
        case "MAL_LIST":
            print("evaluating list")
            return [EVAL(x, repl_env) for x in ast[1]]

        case "MAL_VECTOR":
            print("evaluating vector")
            if len(ast[1]):
                return ("MAL_VECTOR", [EVAL(x, repl_env) for x in ast[1]])
            else:
                return ast

        case "MAL_HASH_MAP":
            print("evaluating hash-map")
            if len(ast[1]):
                return ("MAL_HASH_MAP", [EVAL(ast[1][x], repl_env) if x % 2 == 1 else ast[1][x] for x in range(len(ast[1]))])
            else:
                return ast
        case "MAL_SYMBOL":
            symbol = ast[1][0]
            if symbol in repl_env:
                return repl_env[symbol]
            else:
                return "unimplemented"
        case _:
            return ast

def READ(param: str):
    return reader.read_str(param)

def EVAL(ast, repl_env):
    print("entering eval: " + str(ast))
    mal_type = ast[0]

    match mal_type:
        case "MAL_LIST":
            if ast[1]:
                evaluated = eval_ast(ast, repl_env)
                print("evaluated: "+str(evaluated))
                if ast[1][0][1] in mal_types.get_mal_symbols():
                    return evaluated[0](*evaluated[1:])
                else:
                    return evaluated
            else:
                return ast
        case _:
            return eval_ast(ast, repl_env)

def PRINT(param):
    #print("entering print: " + str(param))
    print(printer.pr_str(param))

def rep(param: str):
    return PRINT(EVAL(READ(param), repl_env))

while True:
    try:
        rep(input(PROMPT))

    except EOFError as e:
        exit(0)
