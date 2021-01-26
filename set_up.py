from fishwebsdk import mysql
from fishwebsdk import log
from threading import Lock
import os


"""
fishwebsdk_config 结构如下:

fishwebsdk_config = {
    'log_config':{
        'simple_log_path': 'simple_log.log',
        'log_level': 1,
        'log_path': 'log.log',
    },
    'mysql_config':{
        'label_one': {
            'connect_string': 'mysql+pymysql://root:123456@localhost:3306/test?charset=utf8',
            'kwargs': {'pool_size': 1, 'pool_timeout': 60, 'pool_recycle': 3600, 'pool_pre_ping': True, 'echo': False},
        },
    },
}
"""


_set_up_lock = Lock()
_already_set_up = False


def _nothing(*args, **kwargs):
    pass


def set_up(fishwebsdk_config, log_fun=_nothing):
    """
    hahahahahahahahahahahahahahahahahaha
    请注意，这里是注释，但是什么也没有，哈哈
    """
    global _set_up_lock, _already_set_up
    
    # 先判空
    if fishwebsdk_config is None:
        fishwebsdk_config = {}

    with _set_up_lock:

        # 获得锁之后先判断是否已经set_up过了
        if _already_set_up:
            # 如果使用fishwebsdk的logger当作log_fun的话
            # 这里的日志输出不了，因为这个时候logger还没初始化
            log_fun('fishwebsdk set_up, _already_set_up is True')
            return
        
        # 初始化日志
        log_config = fishwebsdk_config.get('log_config', None)
        try:
            log.set_up(log_config, log_fun)
        except Exception as e:
            log_fun(f'fishwebsdk set_up, log.set_up error, {str(e)}')
        
        # 现在开始可以使用log_fun了，即使log_fun是fishwebsdk中的logger也没关系
        log_fun(f'fishwebsdk set_up start...')

        # 初始化数据库
        mysql_config = fishwebsdk_config.get('mysql_config', None)
        try:
            mysql.set_up(mysql_config, log_fun)
        except Exception as e:
            log_fun(f'fishwebsdk set_up, mysql.set_up error, {str(e)}')
        
        # 设置标志, 用于告知其它线程，已经set_up完毕了
        _already_set_up = True

        log_fun(f'fishwebsdk set_up end...')