class BaseChacker:

    validators = []

    def __init__(self, require=True, init=None):
        self.data = None
        self._errors = None
        self.require = require
        self.init = init

    def is_valid(self):
        if self._errors is None:
            raise Exception('not run run_check')
        return len(self.errors) == 0

    @property
    def clean_data(self):
        if not self.is_valid():
            raise Exception('not valid')
        return self.data
    
    @property
    def errors(self):
        if self._errors is None:
            raise Exception('not run run_check')
        return self._errors

    def run_check(self, value):
        """
        验证data是否符合本checker的规则
        """
        self._errors = []
        self.data = value

        # 如果data不是期望的类型，尝试转换成期望的类型
        try:
            self.data = self.to_python(self.data)
        except Exception:
            self.data = None
        
        # require检查
        try:
            self.check_require()
        except Exception:
            self._errors.append(f'require')
            return
        
        # 执行检查
        self.check()

        # 如果没有通过上面的检查，则不用进行下面的检查了
        if not self.is_valid():
            return
        
        # 执行validator检查
        for validator in self.validators:
            try:
                validator(self.data)
            except Exception as e:
                self._errors.append(str(e))

    def check_require(self):
        """
        检查是否符合require
        """
        if self.is_null():
            if self.require:
                raise Exception('require')
            else:
                self.data = self.init

    def is_null(self):
        """
        是否为空
        """
        return self.data in [None, '', [], {}, ()]

    def check(self):
        """
        派生类实现自己检查算法
        """
        pass
        # raise NotImplementedError('please implemente check function')
    
    def to_python(self, data):
        raise NotImplementedError('please implemente to_python function')
