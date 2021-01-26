from fishwebsdk.checker.base import Base


class Checker(Base):
    fields = []

    def __init__(self, sname='', dname=None, not_allow_values=None, default=None):
        super().__init__(sname, dname, not_allow_values, default)

    def to_python(self, data):
        # 调用所有字段的clean
        for field in self.fields:
            field.clean(data)
            if not field.is_valid():
                raise Exception(field.error)
        return {field.name: field.value for field in self.fields}
    
    def reset(self):
        # reset自己的成员变量
        super().reset()

        # 调用所有字段的reset
        for field in self.fields:
            field.reset()
