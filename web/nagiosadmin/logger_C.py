#coding=utf-8

import logging

class Logger():
    def __init__(self, logname, loglevel, logger, output):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)

        # 定义输出等级
        if loglevel == 1:
            self.logger.setLevel(logging.DEBUG)
        elif loglevel == 2:
            self.logger.setLevel(logging.INFO)
        elif loglevel == 3:
            self.logger.setLevel(logging.WARNING)
        elif loglevel == 4:
            self.logger.setLevel(logging.ERROR)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        if output == 1:
            self.logger.addHandler(fh)
        elif output == 2:
            self.logger.addHandler(ch)
        elif output == 3:
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)


    def getlog(self):
        return self.logger
