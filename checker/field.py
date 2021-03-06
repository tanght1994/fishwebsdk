from fishwebsdk.checker.base import Base as FieldBase
from fishwebsdk.checker import validator
import time, json


"""
所有Field都接收下面的参数：
sname：数据来名
dname：数据去名
not_allow_values：本字段不允许的值
allow_values：允许的值
default：默认值，如果default不为None，则即使原数据中没有此字段，也不error
validators：用户自定义的验证器
"""


class CharField(FieldBase):
    def __init__(self, max_len=None, min_len=None, choice_list=None, **kwargs):
        super().__init__(**kwargs)
        if max_len:
            self.add_validators(validator.max_len_validator(int(max_len)))
        if min_len:
            self.add_validators(validator.min_len_validator(int(min_len)))
        if choice_list:
            self.add_validators(validator.choice_validator(choice_list))

    def to_python(self, data):
        return str(data)


class IntField(FieldBase):
    def __init__(self, max_val=None, min_val=None, choice_list=None, **kwargs):
        super().__init__(**kwargs)
        if max_val:
            self.add_validators(validator.max_val_validator(max_val))
        if min_val:
            self.add_validators(validator.min_val_validator(min_val))
        if choice_list:
            self.add_validators(validator.choice_validator(choice_list))
    
    def to_python(self, data):
        return int(data)


class FloatField(FieldBase):
    def __init__(self, max_val=None, min_val=None, choice_list=None, **kwargs):
        super().__init__(**kwargs)
        if max_val:
            self.add_validators(validator.max_val_validator(max_val))
        if min_val:
            self.add_validators(validator.min_val_validator(min_val))
        if choice_list:
            self.add_validators(validator.choice_validator(choice_list))
    
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


class JsonStringField(FieldBase):
    """
    将python对象转换为Json字符串
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def to_python(self, data):
        if not isinstance(data, (list, dict)):
            raise Exception("is not json")
        return json.dumps(data, ensure_ascii=False)


class ListField(FieldBase):
    def __init__(self, item_field, strict=False, **kwargs):
        """
        验证list类型，对list中的每一个元素使用item_field进行验证
        item_field: 元素验证器，可以是任意Field类型，也可以是Checker类型
        strict: 严格模式，如果是True，则列表中的元素只要有一个不符合，就认为这个字段不符合要求
                如果是False，则不报错，但是只保留通过验证的元素
        """
        super().__init__(**kwargs)
        self.item_field = item_field
        self.strict = strict
    
    def to_python(self, data):
        if not isinstance(data, list):
            data = [data]
        result = []
        for i in data:
            cleaned_data, error = self.item_field.clean(i)
            if error:
                if self.strict:
                    raise Exception(error)
                else:
                    continue
            result.append(cleaned_data)
        return result