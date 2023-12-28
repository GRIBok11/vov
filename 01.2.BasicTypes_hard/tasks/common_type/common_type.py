def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    if type1 == bool:
        if type2 == bool:
            return bool
        elif type2 == int:
            return int
        elif type2 == float:
            return float
        elif type2 == complex:
            return complex
        elif type2 == list:
            return str
        elif type2 == range:
            return str
        elif type2 == tuple:
            return str
        elif type2 == str:
            return str
    elif type1 == int:
        if type2 == bool:
            return int
        elif type2 == int:
            return int
        elif type2 == float:
            return float
        elif type2 == complex:
            return complex
        elif type2 == list:
            return str
        elif type2 == range:
            return str
        elif type2 == tuple:
            return str
        elif type2 == str:
            return str
    elif type1 == float:
        if type2 == bool:
            return float
        elif type2 == int:
            return float
        elif type2 == float:
            return float
        elif type2 == complex:
            return complex
        elif type2 == list:
            return str
        elif type2 == range:
            return str
        elif type2 == tuple:
            return str
        elif type2 == str:
            return str
    elif type1 == complex:
        if type2 == bool:
            return complex
        elif type2 == int:
            return complex
        elif type2 == float:
            return complex
        elif type2 == complex:
            return complex
        elif type2 == list:
            return str
        elif type2 == range:
            return str
        elif type2 == tuple:
            return str
        elif type2 == str:
            return str
    elif type1 == list:
        if type2 == bool:
            return str
        elif type2 == int:
            return str
        elif type2 == float:
            return str
        elif type2 == complex:
            return str
        elif type2 == list:
            return list
        elif type2 == range:
            return list
        elif type2 == tuple:
            return list
        elif type2 == str:
            return str
    elif type1 == range:
        if type2 == bool:
            return str
        elif type2 == int:
            return str
        elif type2 == float:
            return str
        elif type2 == complex:
            return str
        elif type2 == list:
            return list
        elif type2 == range:
            return tuple
        elif type2 == tuple:
            return tuple
        elif type2 == str:
            return str
    elif type1 == tuple:
        if type2 == bool:
            return str
        elif type2 == int:
            return str
        elif type2 == float:
            return str
        elif type2 == complex:
            return str
        elif type2 == list:
            return list
        elif type2 == range:
            return tuple
        elif type2 == tuple:
            return tuple
        elif type2 == str:
            return str
    elif type1 == str:
        if type2 == bool:
            return str
        elif type2 == int:
            return str
        elif type2 == float:
            return str
        elif type2 == complex:
            return str
        elif type2 == list:
            return str
        elif type2 == range:
            return str
        elif type2 == tuple:
            return str
        elif type2 == str:
            return str
