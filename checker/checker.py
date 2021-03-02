from fishwebsdk.checker.base import Base


class Checker(Base):
    fields = []

    def __init__(self, sname='', dname=None, not_allow_values=None, default=None):
        super().__init__(sname, dname, not_allow_values, default)

    def to_python(self, data):
        # 调用所有字段的clean
        result = {}
        for field in self.fields:
            cleaned_data, error = field.clean(data)
            if error:
                raise Exception(error)
            result[field.dname] = cleaned_data
        return result
