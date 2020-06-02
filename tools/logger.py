# _*_ coding: utf-8 _*_
import logging
import os.path
from config.config import log_path, log_level
import time




class Logger(object):
    def __init__(self):
        '''''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger()  # 名称

        # 创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # log_path = os.path.dirname(os.path.abspath('.')) + '/logs/'
        # log_name = log_path + rq + '.logs'
        self.fh = logging.FileHandler(log_path, encoding='utf-8')
        # 再创建一个handler，用于输出到控制台
        self.ch = logging.StreamHandler()
        # 定义handler的输出格式
        self.set_loglevel()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)
        self.ch.setLevel(logging.CRITICAL)

        # 给logger添加handler
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def set_loglevel(self):
        level = str.upper(log_level)
        if level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)

        elif level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.WARNING)

            # 单独配置文件写入，即打印控制台的日志等级
            # self.fh.setLevel(logging.WARNING)
            # self.ch.setLevel(logging.WARNING)

    def get_log(self):
        return self.logger




logger =  Logger().get_log()

