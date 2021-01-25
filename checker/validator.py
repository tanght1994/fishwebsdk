class max_len_validator:
    def __init__(self, max_len):
        self.max_len = int(max_len)
    
    def __call__(self, data):
        if len(data) > self.max_len:
            raise Exception(f'max length limit, your length is {len(data)}, max length is {self.max_len}')


class min_len_validator:
    def __init__(self, min_len):
        self.min_len = int(min_len)
    
    def __call__(self, data):
        if len(data) < self.min_len:
            raise Exception(f'min length limit, your length is {len(data)}, min length is {self.min_len}')


class max_val_validator:
    def __init__(self, max_val):
        self.max_val = int(max_val)
    
    def __call__(self, data):
        if data > self.max_val:
            raise Exception(f'max value limit, your value is {data}, max value is {self.max_val}')


class min_val_validator:
    def __init__(self, min_val):
        self.min_val = int(min_val)
    
    def __call__(self, data):
        if data < self.min_val:
            raise Exception(f'min value limit, your value is {data}, min value is {self.min_val}')


class choice_validator:
    """
    选择"验证器"，验证value是否是允许的值
    """
    def __init__(self, choice_list):
        self.choice_list = set(choice_list)
    
    def __call__(self, data):
        if data not in self.choice_list:
            raise Exception(f'your data is {data}, not in choice list {list(self.choice_list)}')
