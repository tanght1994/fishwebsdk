"""
此文件是config例子，无其他作用
"""

config = {
    'log_config':{
        'simple_log_path': 'D:\\work\\web\\fishwebsdk\\simple_log.log',
        'log_level': 0,
        'log_path': 'D:\\work\\web\\fishwebsdk\\thtlog.log',
    },
    'mysql_config':{
        'label_one': {
            'connect_string': 'mysql+pymysql://root:123456@localhost:3306/test1?charset=utf8',
            'kwargs': {'pool_size': 10, 'pool_timeout': 60, 'pool_recycle': 3600, 'pool_pre_ping': True, 'echo': False},
        },
    },
}