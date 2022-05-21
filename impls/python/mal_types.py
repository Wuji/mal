#!/usr/bin/env python3
from enum import Enum

MAL_SPECIAL_SYMBOLS = {
    "'": "quote",
    "`": "quasiquote",
    "~": "unquote",
    "@": "deref",
    "^": "with-meta",
    "~@": "splice-unquote"

}

class MAL_TYPES(Enum):
    MAL_STRING = "mal_string"
    MAL_BOOLEAN = "mal_boolean"
    MAL_NIL = "mal_nil"
    MAL_LIST = "mal_list"
    MAL_NUMBER = "mal_number"
    MAL_HASH_MAP = "mal_hash_map"
    MAL_VECTOR = "mal_vector"
    MAL_SYMBOL = "mal_symbol"
    MAL_FUNCTION = "#<function>"

def get_mal_special_symbols():
    return MAL_SPECIAL_SYMBOLS

def get_mal_special_symbol(symbol_str: str):
    if symbol_str in MAL_SPECIAL_SYMBOLS:
        return MAL_SPECIAL_SYMBOLS[symbol_str]
    return None
