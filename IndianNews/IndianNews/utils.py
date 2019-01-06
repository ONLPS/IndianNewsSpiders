"""
Various utility functions 
"""


def error_handler(func):
    """
    error handling decorator
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(ex)
            return 'null'
    return func_wrapper


@error_handler
def get_title(response, path):
    """
    title extractor
    """
    title = response.xpath(path).extract()
    return title[0]


@error_handler
def get_content(response, path):
    """
    content extractor
    """
    content = response.xpath(path).extract()
    content = " ".join(content)
    return content


@error_handler
def get_author(response, path):
    """
    author extractor
    """
    author = response.xpath(path).extract()
    author = ' '.join(author)
    return author


@error_handler
def get_tag(response, path):
    """
    tag extractor
    """
    tag = response.xpath(path).extract()
    if len(tag) == 0:
        tag = []
    return tag
