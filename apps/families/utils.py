def str_to_snake_case(in_str: str):
    out_str = ''

    for c in in_str:
        if c.isspace():
            out_str += '_'
        elif c.isupper():
            out_str += c.lower()
        else:
            out_str += c
    
    return out_str