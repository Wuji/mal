import reader
import printer
import core
from mal_types import MAL_TYPES
import env

PROMPT = "user> "
MAL_NOT = "(def! not (fn* (a) (if a false true)))"

def create_env():

    repl_env = env.Env(None)

    for funct in core.ns:
        repl_env.set(funct, core.ns[funct])

    return repl_env

def eval_ast(ast, repl_env):
    # print("evaluating "+ str(ast))
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
            # symbol = mal_data
            symbol_env = repl_env.find(ast)

            if symbol_env:
                symbol_def = symbol_env.get(ast)
                return symbol_def
            else:
                raise Exception(str(ast)+" not found.")
            # else:
                # raise Exception("unimplemented symbol " + str(symbol))
        case MAL_TYPES.MAL_FUNCTION:
            print("function_eval ")
            print(mal_type)
            print(mal_data)
        case _:
            return ast

def READ(param: str):
    return reader.read_str(param)

def EVAL(ast, repl_env):
    mal_type = ast[0]
    mal_expr = ast[1]

    if mal_type == MAL_TYPES.MAL_LIST:
        if not mal_expr:
            return ast

        first_element = mal_expr[0]
        if first_element[0] == MAL_TYPES.MAL_SYMBOL:
            match first_element[1]:
                case "def!":
                    new_symbol = mal_expr[1]
                    symbol_def = mal_expr[2]
                    evaluated_symbol_def = EVAL(symbol_def, repl_env)

                    repl_env.set(new_symbol, evaluated_symbol_def)
                    return evaluated_symbol_def
                case "let*":
                    # print('new stuff')
                    new_env = env.Env(repl_env)

                    binding_list = mal_expr[1]

                    to_eval = mal_expr[2]
                    if len(binding_list[1]) % 2 == 1:
                        raise Exception("unbalanced binding list")

                    list_iter = iter(binding_list[1])
                    for b_symbol, b_def in zip(list_iter, list_iter):

                        new_env.set(b_symbol, EVAL(b_def, new_env))
                    # print('new env '+str(new_env.data))
                    return EVAL(to_eval, new_env)
                case "do":
                    # Evaluate all the elements of the list using eval_ast and return the final evaluated element.
                    evaluated = []
                    for element in mal_expr[1:]:
                        evaluated.append(EVAL(element, repl_env))
                    # evaluated = [eval_ast(x, repl_env) for x in mal_expr[1:]]
                    return evaluated[-1]
                case "if":
                    condition_result = EVAL(mal_expr[1], repl_env)
                    is_nil = condition_result[0] == MAL_TYPES.MAL_NIL
                    is_false = condition_result[0] == MAL_TYPES.MAL_BOOLEAN and condition_result[1] == "false"
                    if not is_nil and not is_false:
                        return EVAL(mal_expr[2], repl_env)
                    if len(mal_expr) > 3:
                        return EVAL(mal_expr[3], repl_env)
                    else:
                        return (MAL_TYPES.MAL_NIL, "nil")
                case "fn*":
                    # print("binds: "+str(mal_expr[1]))
                    # print("exprs: "+str(mal_expr[2]))

                    def closure(*args):
                        new_env = env.Env(repl_env, mal_expr[1][1], args)

                        return EVAL(mal_expr[2], new_env)
        
                    return (MAL_TYPES.MAL_FUNCTION, closure)
                case _:
                    pass
                    # raise Exception("Error: unknown Symbol "+str(first_element[1]))
        
        evaluated = eval_ast(ast, repl_env)
        
        # print("evaluated list in EVAL: "+str(evaluated))

        if evaluated[0][0] == MAL_TYPES.MAL_FUNCTION:
            return evaluated[0][1](*evaluated[1:])
        else:
            return (MAL_TYPES.MAL_LIST, evaluated)

    return eval_ast(ast, repl_env)

def PRINT(param):
    #print("entering print: " + str(param))
    print(printer.pr_str(param, True))

def rep(param: str, repl_env: env.Env):

    return PRINT(EVAL(READ(param), repl_env))


repl_env = create_env()

rep(MAL_NOT, repl_env)

while True:
    try:
        rep(input(PROMPT), repl_env)

    except EOFError as e:
        exit(0)
    except Exception as e:
        print(e)
