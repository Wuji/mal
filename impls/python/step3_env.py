import reader
import printer
import mal_types
from mal_types import MAL_TYPES
import env

PROMPT = "user> "

def create_env():
    # FIXME: NIL Type
    repl_env = env.Env(None)

    repl_env.set('+', lambda a,b: (mal_types.MAL_TYPES.MAL_NUMBER, a[1]+b[1]))
    repl_env.set('-', lambda a,b: (mal_types.MAL_TYPES.MAL_NUMBER, a[1]-b[1]))
    repl_env.set('*', lambda a,b: (mal_types.MAL_TYPES.MAL_NUMBER, a[1]*b[1]))
    repl_env.set('/', lambda a,b: (mal_types.MAL_TYPES.MAL_NUMBER, int(a[1]/b[1])))
    return repl_env

def eval_ast(ast, repl_env):
    print("evaluating "+ str(ast))
    mal_type = ast[0]
    mal_data = ast[1]

    match mal_type:
        case MAL_TYPES.MAL_LIST:
            return [EVAL(x, repl_env) for x in mal_data]

        case MAL_TYPES.MAL_VECTOR:
            if len(ast[1]):
                return (MAL_TYPES.MAL_VECTOR, [EVAL(x, repl_env) for x in ast[1]])
            else:
                return ast

        case MAL_TYPES.MAL_HASH_MAP:
            if len(ast[1]):
                return (MAL_TYPES.MAL_HASH_MAP, [EVAL(ast[1][x], repl_env) if x % 2 == 1 else ast[1][x] for x in range(len(ast[1]))])
            else:
                return ast

        case MAL_TYPES.MAL_SYMBOL:
            symbol = mal_data
            symbol_env = repl_env.find(symbol)

            if symbol_env:
                symbol_def = symbol_env.get(symbol)
                return symbol_def
            else:
                raise Exception(symbol+" not found.")
            # else:
                # raise Exception("unimplemented symbol " + str(symbol))
        case _:
            return ast

def READ(param: str):
    return reader.read_str(param)

def EVAL(ast, repl_env):
    mal_type = ast[0]
    mal_expr = ast[1]

    if mal_type == MAL_TYPES.MAL_LIST:
        if not ast[1]:
            return ast

        first_element = mal_expr[0]
        if first_element[0] == MAL_TYPES.MAL_SYMBOL:
            match first_element[1]:
                case "def!":
                    new_symbol = mal_expr[1][1]
                    symbol_def = mal_expr[2]
                    evaluated_symbol_def = EVAL(symbol_def, repl_env)

                    repl_env.set(new_symbol, evaluated_symbol_def)
                    return evaluated_symbol_def
                case "let*":
                    print('new stuff')
                    new_env = env.Env(repl_env)

                    binding_list = mal_expr[1]

                    to_eval = mal_expr[2]
                    if len(binding_list[1]) % 2 == 1:
                        raise Exception("unbalanced binding list")

#                    [EVAL(binding_list[1][x], repl_env) if x % 2 == 1 else binding_list[1][x] for x in range(len(binding_list[1]))]
                    list_iter = iter(binding_list[1])
                    for b_symbol, b_def in zip(list_iter, list_iter):

                        new_env.set(b_symbol[1], EVAL(b_def, new_env))
                    print('new env '+str(new_env.data))
                    return EVAL(to_eval, new_env)
                case _:
                    evaluated = eval_ast(ast, repl_env)

                    if hasattr(evaluated[0], '__call__'):
                        return evaluated[0](*evaluated[1:])
                    else:
                        return (MAL_TYPES.MAL_LIST, evaluated)

    return eval_ast(ast, repl_env)

def PRINT(param):
    #print("entering print: " + str(param))
    print(printer.pr_str(param))

def rep(param: str, repl_env: env.Env):

    return PRINT(EVAL(READ(param), repl_env))


repl_env = create_env()

while True:
    try:
        rep(input(PROMPT), repl_env)

    except EOFError as e:
        exit(0)
    except Exception as e:
        print(e)
