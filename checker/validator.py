def max_len_validator(value, max_len):
    if len(value) > max_len:
        raise Exception(f'max length limit, your length is {len(value)}, max length is {max_len}')

def min_len_validator(value, min_len):
    if len(value) < min_len:
        raise Exception(f'min length limit, your length is {len(value)}, min length is {min_len}')

def max_val_validator(value, max_val):
    if int(value) > int(max_val):
        raise Exception(f'max value limit, your value is {value}, max value is {max_val}')

def min_val_validator(value, min_val):
    if int(value) < int(min_val):
        raise Exception(f'min value limit, your value is {value}, min value is {min_val}')