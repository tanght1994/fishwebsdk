from fishwebsdk.checker.base import Base as FieldBase
from fishwebsdk.checker import validator
import time


"""
所有Field都接收下面的参数：
sname：数据来名
dname：数据去名
not_allow_values：本字段不允许的值
default：默认值，如果default不为None，则即使原数据中没有此字段，也不error
"""


class CharField(FieldBase):
    def __init__(self, max_len=None, min_len=None, choice_list=None, **kwargs):
        super().__init__(**kwargs)
        if max_len:
            self.validators.append(validator.max_len_validator(int(max_len)))
        if min_len:
            self.validators.append(validator.min_len_validator(int(min_len)))
        if choice_list:
            self.validators.append(validator.choice_validator(choice_list))

    def to_python(self, data):
        return str(data)


class IntField(FieldBase):
    def __init__(self, max_val=None, min_val=None, choice_list=None, **kwargs):
        super().__init__(**kwargs)
        if max_val:
            self.validators.append(validator.max_val_validator(max_val))
        if min_val:
            self.validators.append(validator.min_val_validator(min_val))
        if choice_list:
            self.validators.append(validator.choice_validator(choice_list))
    
    def to_python(self, data):
        return int(data)


class FloatField(FieldBase):
    def __init__(self, max_val=None, min_val=None, choice_list=None, **kwargs):
        super().__init__(**kwargs)
        if max_val:
            self.validators.append(validator.max_val_validator(max_val))
        if min_val:
            self.validators.append(validator.min_val_validator(min_val))
        if choice_list:
            self.validators.append(validator.choice_validator(choice_list))
    
    def to_python(self, data):
        return float(data)


class TimeField(FieldBase):
    """
    验证时间字符串
    stype:设置来类型，不设置的话就是'%Y-%m-%d %H:%M:%S'
    dtype:设置去类型，不设置的话就是'%Y-%m-%d %H:%M:%S'
    """
    def __init__(self, stype=None, dtype=None, **kwargs):
        super().__init__(**kwargs)
        self.stype = stype if isinstance(stype, str) else '%Y-%m-%d %H:%M:%S'
        self.dtype = dtype if isinstance(dtype, str) else '%Y-%m-%d %H:%M:%S'
    
    def to_python(self, data):
        data = str(data)
        t = time.mktime(time.strptime(data, self.stype))
        return time.strftime(self.dtype, time.localtime(t))

