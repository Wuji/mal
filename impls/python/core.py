from pickle import TRUE
from mal_types import MAL_TYPES
import printer

def mal_list(*args):
    return (MAL_TYPES.MAL_LIST, list(args))

def mal_is_list(a):
    if a[0] == MAL_TYPES.MAL_LIST:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")

def mal_is_empty(a):
    if not a[1]:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")

def mal_count(a):
    if a[0] == MAL_TYPES.MAL_NIL:
        return (MAL_TYPES.MAL_NUMBER, 0)
    else:
        return (MAL_TYPES.MAL_NUMBER, len(a[1]))

def mal_equal(a, b):
    if a[0] == b[0] and a[1] == b[1]:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")

def mal_less(a, b):
    if a[0] == b[0] and a[1] < b[1]:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")

def mal_less_equal(a, b):
    if a[0] == b[0] and a[1] <= b[1]:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")

def mal_greater(a, b):
    if a[0] == b[0] and a[1] > b[1]:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")

def mal_greater_equal(a, b):
    if a[0] == b[0] and a[1] >= b[1]:
        return (MAL_TYPES.MAL_BOOLEAN, "true")
    else:
        return (MAL_TYPES.MAL_BOOLEAN, "false")
    
def mal_prn(*args):
    outstr = ""
    for arg in args:
        if outstr == "":
            outstr = printer.pr_str(arg, True)
        else: 
            outstr = outstr + " " + printer.pr_str(arg, True)
    print(outstr)
    return (MAL_TYPES.MAL_NIL, "nil")

def mal_str(*args):
    outstr = ""
    for arg in args:
        outstr += printer.pr_str(arg, False)
    return (MAL_TYPES.MAL_STRING, outstr)

def mal_pr_str(*args):
    outstr = ""
    for arg in args:
        if outstr == "":
            outstr = printer.pr_str(arg, True)
        else:
            outstr = outstr + " " + printer.pr_str(arg, True)
    return (MAL_TYPES.MAL_STRING, outstr)

def mal_println(*args):
    outstr = ""
    for arg in args:
        if outstr == "":
            outstr = printer.pr_str(arg, False)
        else:
            outstr = outstr + " " + printer.pr_str(arg, False)
    print(outstr)
    return (MAL_TYPES.MAL_NIL, "nil")

ns = {
    (MAL_TYPES.MAL_SYMBOL, "+"): (MAL_TYPES.MAL_FUNCTION, lambda a,b: (MAL_TYPES.MAL_NUMBER, a[1]+b[1])),
    (MAL_TYPES.MAL_SYMBOL, "-"): (MAL_TYPES.MAL_FUNCTION, lambda a,b: (MAL_TYPES.MAL_NUMBER, a[1]-b[1])),
    (MAL_TYPES.MAL_SYMBOL, "*"): (MAL_TYPES.MAL_FUNCTION, lambda a,b: (MAL_TYPES.MAL_NUMBER, a[1]*b[1])),
    (MAL_TYPES.MAL_SYMBOL, "/"): (MAL_TYPES.MAL_FUNCTION, lambda a,b: (MAL_TYPES.MAL_NUMBER, int(a[1]/b[1]))),
    (MAL_TYPES.MAL_SYMBOL, "="): (MAL_TYPES.MAL_FUNCTION, mal_equal),
    (MAL_TYPES.MAL_SYMBOL, "<"): (MAL_TYPES.MAL_FUNCTION, mal_less),
    (MAL_TYPES.MAL_SYMBOL, "<="): (MAL_TYPES.MAL_FUNCTION, mal_less_equal),
    (MAL_TYPES.MAL_SYMBOL, ">"): (MAL_TYPES.MAL_FUNCTION, mal_greater),
    (MAL_TYPES.MAL_SYMBOL, ">="): (MAL_TYPES.MAL_FUNCTION, mal_greater_equal),
    (MAL_TYPES.MAL_SYMBOL, "count"): (MAL_TYPES.MAL_FUNCTION, mal_count),
    (MAL_TYPES.MAL_SYMBOL, "list"): (MAL_TYPES.MAL_FUNCTION, mal_list),
    (MAL_TYPES.MAL_SYMBOL, "list?"): (MAL_TYPES.MAL_FUNCTION, mal_is_list),
    (MAL_TYPES.MAL_SYMBOL, "empty?"): (MAL_TYPES.MAL_FUNCTION, mal_is_empty),
    (MAL_TYPES.MAL_SYMBOL, "str"): (MAL_TYPES.MAL_FUNCTION, mal_str),
    (MAL_TYPES.MAL_SYMBOL, "pr-str"): (MAL_TYPES.MAL_FUNCTION, mal_pr_str),
    (MAL_TYPES.MAL_SYMBOL, "prn"): (MAL_TYPES.MAL_FUNCTION, mal_prn),
    (MAL_TYPES.MAL_SYMBOL, "println"): (MAL_TYPES.MAL_FUNCTION, mal_println),
}