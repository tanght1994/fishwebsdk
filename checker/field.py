from fishwebsdk.checker.base import BaseChacker


class ListField(BaseChacker):
    def __init__(self, item_field, require=True, init=[]):
        self.item_field = item_field
        super().__init__(require=require, init=init)
    
    def check(self):
        clean_data = []

        # 遍历自己的data，对每个元素调用item_field进行检查
        for one_data in self.data:
            self.item_field.run_check(one_data)
            if not self.item_field.is_valid():
                self._errors.append(' AND '.join(self.item_field.errors))
            clean_data.append(self.item_field.clean_data)

        self.data = clean_data

    def to_python(self, data):
        if isinstance(data, list):
            return data
        return [data]


class CharField(BaseChacker):
    def __init__(self, require=True, init='', max_len=None, min_len=None):
        super().__init__(require=require, init=init)

    def to_python(self, data):
        return None if data is None else str(data)