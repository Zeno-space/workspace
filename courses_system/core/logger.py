import os
import logging
from logging.handlers import TimedRotatingFileHandler
from conf import setting


#可以使用类，添加格式化的消息，例如debug_log.err_unique输出唯一值错误
#可以添加更丰富的配置，有待升级
def logger(log_name, **kwargs):
    """
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(setting.LOG_LEVEL['base_level'])

    if log_name == 'debug.log':
        ch_formatter = logging.Formatter('    \n\t%(message)s')
        fh_formatter = logging.Formatter(
            '%(asctime)s - %(module)s - %(funcName)s - %(lineno)d : \n\t%(message)s'
        )
    else:
        ch_formatter = logging.Formatter('%(asctime)s : %(message)s')
        fh_formatter = logging.Formatter(
            '%(levelname)s - %(asctime)s : %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(setting.LOG_LEVEL[log_name]['screan'])
    ch.setFormatter(ch_formatter)

    file_path = os.path.join(setting.LOG_PATH, log_name)
    if kwargs.get('timedrotating') and kwargs.get('interval'):
        fh = TimedRotatingFileHandler(
            file_path,
            when=kwargs['timedrotating'],
            interval=kwargs['interval'],
            encoding='utf-8')
    else:
        fh = logging.FileHandler(file_path, encoding='utf-8')
    fh.setLevel(setting.LOG_LEVEL[log_name]['file'])
    fh.setFormatter(fh_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


# operation_log = logger('operation.log')

#30日 日志回滚
# consumption_log = logger('consumption.log', timedrotating='D', interval=30)

debug_log = logger('debug.log')

if __name__ == '__main__':
    logger('debug.log')