class Field:
    def is_valid(self, data):
        pass

    def clean_data(self, data):
        pass


def max_len_checker(value, max_len):
    if len(value) > max_len:
        raise Exception('123')

def min_len_checker(value, min_len):
    if len(value) < min_len:
        raise Exception('123')


class ListField(Field):
    def __init__(self, item_field, require=True, init=[]):
        self.item_field = item_field
        self.require = require
        self.init = init
    
    def clean(self, value):
        tmp = []
        for i in value:
            clean_data = self.item_field.clean(i)
            tmp.append(clean_data)
        return tmp

    def to_python(self, value):
        if value in [None, '']:
            if self.require:
                raise Exception('require')
            else:
                value = self.init
        return str(value)


class CharField(Field):
    def __init__(self, require=True, init=''):
        self.require = require
        self.init = init
        pass
    
    def clean(self, value):
        return self.to_python(value)

    def to_python(self, value):
        if value in [None, '']:
            if self.require:
                raise Exception('require')
            else:
                value = self.init
        return str(value)


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
            if isinstance(field, Field):
                current_fields.append((key, value))
                attrs.pop(key)
        attrs['collect_fields'] = dict(current_fields)
        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class


class Checker(metaclass=MyMetaclass):

    def __init__(self, data=None):
        self._data = {}
        if isinstance(data, dict):
            self._data = data

        # pylint: disable=no-member
        self.fields = self.collect_fields
        # pylint: enable=no-member

    def clean(self):
        clean_data = {}
        for key, value in self.fields.items():
            name = key
            field = value
            if isinstance(value, tuple):
                field = value[0]
                name = value[1]
            raw_data = self._data.get(key, None)
            clean_data = field.clean(raw_data)
            clean_data[name] = clean_data
        return clean_data


class TestChecker(Checker):
    arg1 = CharField(), 'arg8'
    arg2 = ListField(CharField())

post_data = {
    'arg1': 'tanght',
    'arg2': ['tanght', 'haha', 'hehe'],
    'arg3': 'hahah'
}

checker = TestChecker(data=post_data)
data = checker.clean()
print(data)