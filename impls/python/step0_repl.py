PROMPT = "user> "

def READ(param: str):
    return param

def EVAL(param: str):
    return param

def PRINT(param: str):
    return param

def rep(param: str):
    return PRINT(EVAL(READ(param)))

while True:
    try:
        print(rep(input(PROMPT)))

    except EOFError as e:
        exit(0)
