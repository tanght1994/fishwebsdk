import json
from fishwebsdk.checker.base import BaseChacker


class MyMetaclass(type):
    """
    将Field类型的成员收集到collect_fields中
    """
    def __new__(mcs, name, bases, attrs):
        current_fields = []
        for key, value in list(attrs.items()):
            field = value
            if isinstance(field, tuple):
                field = field[0]
            if isinstance(field, BaseChacker):
                current_fields.append((key, value))
                attrs.pop(key)
        attrs['collect_fields'] = dict(current_fields)
        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class


class Checker(BaseChacker, metaclass=MyMetaclass):

    def __init__(self, require=True, init=None):
        super().__init__(require=require, init=init)
        # pylint: disable=no-member
        self.fields = self.collect_fields
        # pylint: enable=no-member
    
    def is_null(self):
        return not isinstance(self.data, dict)
    
    def to_python(self, data):
        if isinstance(data, dict):
            return data
        elif isinstance(data, str):
            return json.loads(data)
        raise Exception()
        
    def check(self):
        clean_data = {}
        for key, value in self.fields.items():
            front_name = back_name = key
            field = value
            if isinstance(value, tuple):
                field = value[0]
                back_name = value[1]

            field_data = self.data.get(key, None)
            field.run_check(field_data)

            if not field.is_valid():
                field_name = front_name if front_name == back_name else f'{front_name}_{back_name}'
                err_msg = f'{{"{field_name}": {" AND ".join(field.errors)}}}'
                self.errors.append(err_msg)
                continue

            clean_data[back_name] = field.clean_data

        self.data = clean_data
