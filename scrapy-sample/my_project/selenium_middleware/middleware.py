import json
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.exceptions import NotConfigured

from importlib import import_module

from selenium.webdriver.support.ui import WebDriverWait

from .request import SeleniumRequest

import scrapy


raw_cookie = ""

def parse_dict_cookies(value):
    result = {}
    for item in value.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        result[name] = value
    return result

cookie = parse_dict_cookies(raw_cookie)
print(json.dumps(cookie, indent=4, sort_keys=True))


class SeleniumMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # Initialize settings for selenium driver with the crawler settings

        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if not driver_name or not driver_executable_path:
            raise NotConfigured('SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set')

        middleware_settings = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments
        )
        crawler.signals.connect(middleware_settings.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware_settings.spider_closed, signal=signals.spider_closed)
        return middleware_settings

    def __init__(self, driver_name, driver_executable_path, driver_arguments):

        # Initialize selenium webdriver with crawler settings
        """
        docstring here
            :param driver_name: str
                The selenium 'webdriver' to use
            :param driver_executable_path: str
                The path of the executable binary of the driver
            :param driver_arguments: list
                A list of arguments to initialize the driver
        """

        web_driver_base_path = f'selenium.webdriver.{driver_name}'

        # get driver class
        driver_class_module = import_module(f'{web_driver_base_path}.webdriver')
        driver_class = getattr(driver_class_module, 'WebDriver')

        # get driver option class
        driver_options_module = import_module(f'{web_driver_base_path}.options')
        driver_options_class = getattr(driver_options_module, 'Options')

        # add argument to driver options
        driver_options = driver_options_class()
        if driver_arguments:
            for argument in driver_arguments:
                driver_options.add_argument(argument)

        # add argument to driver
        driver_kargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        self.driver = driver_class(**driver_kargs)
        self.driver.get("https://facebook.com")  # NOTE: it must be access facebook.com before add cookie of facebook, else ERROR happend

        for key, value in cookie.items():
            self.driver.add_cookie({'name' : key, 'value' : value, 'domain' : 'facebook.com'})

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # Process a request using the selenium driver if applicable

        if not isinstance(request, SeleniumRequest):
            return None

        self.driver.get(request.url)
        self.driver.maximize_window()
        # self.driver.set_network_conditions(
        #     offline=False,
        #     latency=10,
        #     download_throughput=100 * 1024,
        #     upload_throughput=100 * 1024)

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(method=request.wait_until, message='Timeout happend')

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        body = str.encode(self.driver.page_source)

        # Expose the drive via the 'meta' attribute
        request.meta.update({'driver': self.driver})
        # request.meta['driver', self.driver]

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        # shutdown the driver when the spider is closed
        self.driver.close()

