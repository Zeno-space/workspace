import os
import logging
from conf import setting

#可以使用类，添加格式化的消息，例如debug_log.err_unique输出唯一值错误
def logger(log_name):
    """
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(setting.LOG_LEVEL['base_level'])

    if log_name == 'debug.log':
        ch_formatter = logging.Formatter('    \n\t%(message)s')
        fh_formatter = logging.Formatter('%(asctime)s - %(module)s - %(funcName)s - %(lineno)d : \n\t%(message)s')
    else:
        ch_formatter = logging.Formatter('%(asctime)s : %(message)s')
        fh_formatter = logging.Formatter('%(levelname)s - %(asctime)s : %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(setting.LOG_LEVEL[log_name]['screan'])
    ch.setFormatter(ch_formatter)

    fh = logging.FileHandler(os.path.join(setting.LOG_PATH, log_name), encoding='utf-8')
    fh.setLevel(setting.LOG_LEVEL[log_name]['file'])
    fh.setFormatter(fh_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

opreration_log = logger('operation.log')
consumption_log = logger('consumption.log')

debug_log = logger('debug.log')

if __name__ == '__main__':
    logger('debug.log')