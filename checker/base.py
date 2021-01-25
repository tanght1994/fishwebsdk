import copy
class Base:

    def __init__(self, sname=None, dname=None, not_allow_values=None, default=None):
        
        self.not_allow_values = [None, '', {}, []]
        self.validators = []

        # 校验sname
        if sname is None:
            raise Exception('sname must be set')
        self.sname = sname

        # 校验dname
        self.dname = dname or sname
        if self.dname is None:
            raise Exception('dname is None')
        
        # 校验not_allow_values
        if not_allow_values:
            if not isinstance(not_allow_values, (tuple, list, set)):
                raise Exception('not_allow_values type error, it must be tuple/list/set')
            else:
                self.not_allow_values = not_allow_values
        
        # 校验default
        self.default = default

        self.clean_data = None
        self.error = None
        self.already_clean = False
    
    @property
    def value(self):
        if not self.already_clean:
            raise Exception('not run clean')
        if self.error is not None:
            raise Exception('have error')
        return self.clean_data
    
    @property
    def name(self):
        return self.dname
    
    def is_valid(self):
        if not self.already_clean:
            raise Exception('not run clean')
        return self.error is None
    
    def is_not_allow_value(self, value):
        return value in self.not_allow_values

    def to_python(self, value):
        """
        value肯定不是None
        """
        raise NotImplementedError()
    
    def clean(self, data):
        """
        清理数据
        """

        if self.already_clean:
            return
        
        self.already_clean = True

        # data的类型必须是dict
        # 如果self.sname ！= ''，则data[self.sname]为本field的数据
        # 如果self.sname == ''，则data为本field的数据
        mydata = None
        if isinstance(data, dict):
            mydata = data.get(self.sname, None) if self.sname != '' else data

        try:
            # 转换为本field所需要的类型
            try:
                python_value = self.to_python(mydata) if mydata else None
            except Exception as e:
                raise Exception(f'to_python error, {str(e)}')

            # 验证是否允许
            if self.is_not_allow_value(python_value):
                python_value = self.default
            if self.is_not_allow_value(python_value):
                raise Exception(f'{str(python_value)} is not allow')
            
            # 验证器验证
            for validator in self.validators:
                tmp = copy.deepcopy(python_value)
                validator(tmp)
            
            # 通过以上验证则设置clean_data
            self.clean_data = python_value
        except Exception as e:
            field_name = self.sname if self.sname == self.dname else f'{self.sname}->{self.dname}'
            self.error = f'{{"{field_name}":{str(e)}}}'
