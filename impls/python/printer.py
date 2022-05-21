from mal_types import MAL_TYPES
import mal_types
import itertools

def pr_str(maltype, print_readably):
    # print("entering pr_str with "+str(maltype))
    typeof_maltype = maltype[0]
    valueof_maltype = maltype[1]
    # print(type(valueof_maltype))
    match typeof_maltype:
        case MAL_TYPES.MAL_BOOLEAN | MAL_TYPES.MAL_NIL:
            return str(valueof_maltype)
        case MAL_TYPES.MAL_STRING:
            if not valueof_maltype:
                return ""
            
            if print_readably:
                return valueof_maltype
            else:
                value_string = valueof_maltype.strip('"')
                return value_string

        case MAL_TYPES.MAL_NUMBER:
            return str(valueof_maltype)
        case MAL_TYPES.MAL_LIST:
            joined = ""
            if valueof_maltype:
                joined = " ".join(map(pr_str, valueof_maltype, itertools.repeat(print_readably)))
            return "(" + joined + ")"
        case MAL_TYPES.MAL_VECTOR:
            joined = ""
            if valueof_maltype:
                joined = " ".join(map(pr_str, valueof_maltype, itertools.repeat(print_readably)))
            return "[" + joined + "]"
        case MAL_TYPES.MAL_HASH_MAP:
            joined = ""
            if valueof_maltype:
                joined = " ".join(map(pr_str, valueof_maltype, itertools.repeat(print_readably)))
            return "{" + joined + "}"
        case MAL_TYPES.MAL_SYMBOL:
            symbol = valueof_maltype
            if symbol in mal_types.get_mal_special_symbols():
                symbol_str = mal_types.get_mal_special_symbol(symbol)
            else:
                symbol_str = symbol

            return symbol_str
        case MAL_TYPES.MAL_FUNCTION:
            return MAL_TYPES.MAL_FUNCTION.value
        case _:
            raise Exception("Error: Unsupported type: " + str(typeof_maltype))
