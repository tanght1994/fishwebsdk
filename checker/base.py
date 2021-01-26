import copy


class Base:

    def __init__(self, sname=None, dname=None, not_allow_values=None, allow_values=None, default=None):
        """
        参数解释：
        sname: 来名
        dname: 去名
        not_allow_values: 不被允许的值。若设置了这个参数，就会覆盖默认的not_allow_values，默认值为[None, '', {}, []]
        allow_values: 从not_allow_values中剔除allow_values
        default: 默认值。若设置了这个值则原数据中可以没有这个字段，用默认值代替
        
        成员变量解释：
        self.validators: 验证器
        self.clean_data: 干净的数据保存在这里，调用value的时候直接返回clean_data
        self.error: 错误原因储存在这里，外部直接读取error来读取错误原因
        self.already_clean: 是否已经运行过clean函数的标识
        """

        # 校验sname
        if sname is None:
            raise Exception('sname must be set')
        self.sname = sname

        # 校验dname
        self.dname = dname or sname
        if self.dname is None:
            raise Exception('dname is None')
        
        # 设置self.not_allow_values
        self.not_allow_values = [None, '', {}, []]

        if not_allow_values:
            # 判断参数类型是否被允许
            if not isinstance(not_allow_values, (tuple, list)):
                raise Exception('not_allow_values type error, it must be tuple/list type')
            
            # 使用用户传入的not_allow_values覆盖默认的not_allow_values
            self.not_allow_values = []
            for i in not_allow_values:
                if i not in not_allow_values:
                    self.not_allow_values.append(i)
        
        # 从not_allow_values中剔除allow_values
        if allow_values and isinstance(allow_values, (tuple, list)):
            for i in allow_values:
                try:
                    self.not_allow_values.remove(i)
                except Exception:
                    pass
        
        # 保存default
        self.default = default

        self.validators = []
        self.clean_data = None
        self.error = None
        self.already_clean = False
    
    @property
    def value(self):
        """
        必须调用过clean()之后才能调用次函数，否则raise
        必须没有错误才能调用此属性，否则raise
        返回处理过的数据，干净的数据
        """
        if not self.already_clean:
            raise Exception('not run clean')
        if self.error is not None:
            raise Exception('have error')
        return self.clean_data
    
    @property
    def name(self):
        return self.dname
    
    def is_valid(self):
        """
        必须调用过clean()之后才能调用次函数，否则raise
        数据是否有效，是返回True，否返回False
        """
        if not self.already_clean:
            raise Exception('not run clean')
        return self.error is None
    
    def is_not_allow_value(self, value):
        return value in self.not_allow_values

    def to_python(self, value):
        """
        value肯定不是None
        子类负责实现这个方法
        """
        raise NotImplementedError()
    
    def clean(self, data):
        """
        清理，验证数据
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

            # 验证是否是允许的值，如果是不允许的值，则用default代替
            if self.is_not_allow_value(python_value):
                python_value = self.default
            
            # 有可能用户没有设置default，那么就是不允许了
            if self.is_not_allow_value(python_value):
                raise Exception(f'{str(python_value)} is not allow')
            
            # 验证器验证
            for validator in self.validators:
                tmp = copy.deepcopy(python_value)
                validator(tmp)
            
            # 通过以上验证就设置clean_data
            self.clean_data = python_value
        except Exception as e:
            field_name = self.sname if self.sname == self.dname else f'{self.sname}_{self.dname}'
            self.error = f'{{"{field_name}":{str(e)}}}'
    
    def reset(self):
        self.clean_data = None
        self.error = None
        self.already_clean = False
