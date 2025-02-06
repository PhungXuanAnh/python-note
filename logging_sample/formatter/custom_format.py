import logging

def the_first_way():
    extra = {'custom_format':'11111111111'}
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(custom_format)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    extra = {'custom_format':'222222222'}
    logger = logging.LoggerAdapter(logger, extra)
    logger.info('The sky is so blue')

    extra = {'custom_format':'33333333333'}
    logger = logging.LoggerAdapter(logger, extra)
    logger.info('The sky is so blue')

class MyCustomFormatAttributes(logging.Filter):
    def filter(self, record):
        record.custom_format = 'custom_format'
        return True

def the_second_way():
    logger1 = logging.getLogger(__name__)
    logger1.setLevel(logging.INFO)
    
    logger1.addFilter(MyCustomFormatAttributes())
    
    handler1 = logging.StreamHandler()
    formatter1 = logging.Formatter('%(asctime)s %(custom_format)s : %(message)s')
    handler1.setFormatter(formatter1)
    logger1.addHandler(handler1)

    logger1.info('========================')


if __name__ == "__main__":
    the_first_way()
    the_second_way()


