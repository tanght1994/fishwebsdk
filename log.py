import logging, time


logger = logging.getLogger(__name__)
_never_handler = logging.Handler(level=99999999)
logger.addHandler(_never_handler)
_simple_log_path = ''


def simplelog(msg, path='log.log'):
    try:
        if (_simple_log_path != '') and (path == 'log.log'):
            path = _simple_log_path
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg = f'{current_time} {str(msg)}\n'
        with open(path, 'a', encoding='utf-8') as f:
            f.write(msg)
    except Exception:
        pass


def set_up(log_config, log_fun):
    global _simple_log_path, logger

    if log_config is None:
        log_fun(f'log_config is None')
        return

    _simple_log_path = log_config.get('simple_log_path', _simple_log_path)

    log_level = log_config.get('log_level', None)
    log_path = log_config.get('log_path', None)
    if None in (log_level, log_path):
        log_fun('not log_level or not log_path')
        return

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(str(log_path))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(int(log_level))