from scrapy import Request


class SeleniumRequest(Request):
    def __init__(self, wait_time=None, wait_until=None, screenshot=False, *args, **kargs):
        """
        docstring here
            :param wait_time: int
                The number of second to wait
            :param wait_util: method
                On of the 'selenium.webdriver.support.expected_conditions'.
                The response will be returned until the given condition fulfilled
            :param screen_shot: bool
                If True, a screen short of the page will be taken and the data of
                the screenshot will be return in the response 'meta' attribute
        """
        
        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        
        super().__init__(*args, **kargs)
