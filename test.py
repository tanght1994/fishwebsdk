class Field:

    not_allow_values = [None, '', {}, []]

    def __init__(self, sname=None, dname=None, not_allow_values=None, default=None):
        
        # 校验sname
        if sname == '':
            raise Exception('')
        self.sname = sname

        # 校验dname
        self.dname = dname or sname
        if self.dname in ['', None]:
            raise Exception('')
        
        # 校验not_allow_values
        if not_allow_values:
            if not isinstance(not_allow_values, (tuple, list, set)):
                raise Exception('')
            else:
                self.not_allow_values = not_allow_values
        
        # 校验default
        self.default = default
    
    def is_not_allow_value(self, value):
        return value in self.not_allow_values

    def to_python(self, value):
        raise NotImplementedError()
    
    def clean(self, data):
        python_value = self.to_python(data)
        if self.is_not_allow_value(python_value):
            python_value = self.default
        if self.is_not_allow_value(python_value):
            raise Exception('')
        
        # 验证器验证
        
        self.value = python_value


class Checker:
    fields = []

    def clean(self, data):
        for field in self.fields:
            field.clean()
        self.value = {field.name: field.value for field in self.fields}
