import reader
import printer

PROMPT = "user> "

def READ(param: str):
    return reader.read_str(param)

def EVAL(param):
    #print("entering eval: " + str(param))
    return param

def PRINT(param):
    #print("entering print: " + str(param))
    print(printer.pr_str(param))

def rep(param: str):
    return PRINT(EVAL(READ(param)))

while True:
    try:
        rep(input(PROMPT))

    except EOFError as e:
        exit(0)
