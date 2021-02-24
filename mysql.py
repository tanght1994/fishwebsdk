import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from threading import Lock


"""
1. sql2python() 将sqlalchemy的结果转换为python内置类型，
2. tables_dict 储存了所有数据库的所有表格信息
3. Session 封装了数据库连接，通过with调用它
4. 调用set_up(config)来初始化数据库信息

注意: 推荐在main.py中调用 set_up(config)，保证只set_up一次
未set_up之前，不可以使用本文件中的其它 函数or变量 因为都是空的

向外部提供 tables_dict Session sql2python
"""


_set_up_lock = Lock()
_engines = {}
_already_set_up = False
tables_dict = {}


def _nothing(*args, **kwargs):
    pass


def sql2python(result, log_fun=_nothing):
    """
    功能：将sqlalchemy查询返回的结果转换为python的内置类型，[dict,]
    参数：sqlalchemy查询返回的结果
    返回值：(data, error_msg)   data肯定为list，有可能是空list
    注意：必须在session未commit和close的时候调用此函数，若调用此函数的时候session已经commit或者close，则报错
    """
    try:
        if result is None:
            return []
        # 处理session.execute()的结果
        if isinstance(result, sqlalchemy.engine.result.ResultProxy):
            return [{k: str(row[k]) for k in row.keys()} for row in result]

        # 处理ORM的结果
        if isinstance(result, list):
            if len(result) == 0:
                return []
            if hasattr(result[0], '__table__'):
                return [{c.name: str(getattr(r, c.name)) for c in r.__table__.columns} for r in result]
            elif hasattr(result[0], '_real_fields'):
                fields = [field for field in result[0]._real_fields]
                fields_length = len(fields)
                return [{fields[i]: str(item[i]) for i in range(fields_length)} for item in result]
            else:
                log_fun('trans sqlalchemy result error 1')
                return []
        else:
            if hasattr(result, '__table__'):
                return [{c.name: str(getattr(result, c.name)) for c in result.__table__.columns}]
            elif hasattr(result, '_real_fields'):
                fields = [field for field in result._real_fields]
                return [{fields[i]: str(result[i]) for i in range(len(fields))}]
            else:
                log_fun('trans sqlalchemy result error 2')
                return []
    except Exception as e:
        log_fun(f'trans sqlalchemy result error, {str(e)}')
    return []


class Session():
    """
    with Session('1') as session:
        数据库操作...
    离开with作用域时，自动close
    """
    def __init__(self, db_label: str):
        global _engines
        self.session = sessionmaker(_engines[db_label])()

    def __enter__(self):
        return self.session

    def __exit__(self, a, b, c):
        # pylint: disable=no-member
        self.session.close()
        # pylint: enable=no-member


def insert_on_duplicate_key_update(session, table, data: dict):
    """
    插入数据，遇到主键冲突时，更新除主键外的所有数据为data中对应的数据
    注意，当使用 ON DUPLICATE KEY UPDATE 语句时，可能会造成‘自增字段不连续’
    可以通过修改mysql的配置来解决‘自增字段不连续’的问题，但是会影响mysql性能
    详细信息请查询mysql官方文档
    """
    from sqlalchemy.dialects.mysql import insert
    insert_stmt = insert(table).values(**data)
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**data)
    # pylint: disable=no-member
    session.execute(on_duplicate_key_stmt)
    # pylint: enable=no-member


def set_up(mysql_config: dict, log_fun=_nothing):
    """
    功能: 创建数据库引擎，制作数据库结构映射
    注意: 在使用本文件的其它函数、变量之前要先调用此函数
    """
    global _engines, tables_dict

    if mysql_config is None:
        return
    
    log_fun('init mysql engine start...')

    # 创建sqlalchemy引擎(数据库), 储存到_engines字典中
    # 对每个引擎(数据库), 映射表格，储存到tables_dict字典中
    for label, config in mysql_config.items():
        try:
            log_fun(f"create engine[{label}] start...")

            # 检查connect_string
            connect_string = config.get('connect_string', None)
            if connect_string is None:
                log_fun(f"error, not find connect_string node")
                continue

            log_fun(f"connect_string is [{str(connect_string)}]")
            
            # 检查kwargs
            kwargs = config.get('kwargs', {})
            if not isinstance(kwargs, dict):
                log_fun(f"error, kwargs is not dict")
                continue
            
            log_fun(f"kwargs is [{str(kwargs)}]")
            
            # 创建数据库引擎并映射表格
            _engines[label] = create_engine(str(connect_string), **kwargs)
            tmp = automap_base()
            tmp.prepare(_engines[label], reflect=True)
            tables_dict[label] = tmp.classes

            log_fun(f"successful!")
        except Exception as e:
            try:
                log_fun(f"error, {str(e)}")
            except Exception:
                pass
        finally:
            log_fun(f"create engine[{label}] end...")
    
    log_fun('init mysql engine end...')