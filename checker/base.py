import copy


class Base:

    def __init__(self, sname=None, dname=None, not_allow_values=None, allow_values=None, default=None, validators=None):
        """
        参数解释：
        sname: 来名
        dname: 去名
        not_allow_values: 不被允许的值。若设置了这个参数，就会覆盖默认的not_allow_values，默认值为[None, '', {}, []]
        allow_values: 从not_allow_values中剔除allow_values
        default: 默认值。若设置了这个值则原数据中可以没有这个字段，用默认值代替
        
        成员变量解释：
        self._validators: 验证器
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
        self._not_allow_values = [None, '', {}, []]

        if not_allow_values:
            # 判断参数类型是否被允许
            if not isinstance(not_allow_values, (tuple, list)):
                raise Exception('not_allow_values type error, it must be tuple/list type')
            
            # 使用用户传入的not_allow_values覆盖默认的not_allow_values
            self._not_allow_values = []
            for i in not_allow_values:
                if i not in not_allow_values:
                    self._not_allow_values.append(i)
        
        # 从not_allow_values中剔除allow_values
        if allow_values and isinstance(allow_values, (tuple, list)):
            for i in allow_values:
                try:
                    self._not_allow_values.remove(i)
                except Exception:
                    pass
        
        # 添加用户的验证器
        if not hasattr(self, '_validators'):
            self._validators = []
        self.add_validators(validators)

        # 保存default
        self._default = default
    
    def add_validators(self, validators: list):
        if validators is None:
            return
        if isinstance(validators, list):
            self._validators.extend(validators)
        else:
            self._validators.append(validators)
    
    def is_not_allow_value(self, value):
        return value in self._not_allow_values

    def to_python(self, value):
        """
        外部保证value肯定不是None
        子类负责实现这个方法
        """
        raise NotImplementedError()
    
    def clean(self, data):
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
            except Exception:
                python_value = None

            # 验证是否是允许的值，如果是不允许的值，则用default代替
            if self.is_not_allow_value(python_value):
                python_value = self._default
            
            # 有可能用户没有设置default，那么就是不允许了
            if self.is_not_allow_value(python_value):
                raise Exception(f'{str(python_value)} is not allow')
            
            # 验证器验证
            for validator in self._validators:
                tmp = copy.deepcopy(python_value)
                validator(tmp)
            
            # 返回  清理后的数据, error
            return python_value, None
        except Exception as e:
            field_name = self.sname if self.sname == self.dname else f'{self.sname}-{self.dname}'
            err_msg = f'{{"{field_name}":{str(e)}}}' if field_name != '' else str(e)
            return None, err_msg
