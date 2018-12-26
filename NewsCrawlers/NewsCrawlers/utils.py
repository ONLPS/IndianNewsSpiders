




def error_handling(func):
	def func_wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as ex:
			print(ex)
			return 'null'
	return func_wrapper

@error_handling
def get_title(response, path):
	title = response.xpath(path).extract()
	return title[0]

@error_handling
def get_content(response,path):
	content = response.xpath(path).extract()
	content = " ".join(content)
	return content

@error_handling
def get_author(response,path):
	author = response.xpath(path).extract()
	author = ' '.join(author)
	return author

@error_handling
def get_comment(response,path):
	comment = response.xpath(path).extract()
	return comment

@error_handling
def get_tag(response,path):
	tag = response.xpath(path).extract()
	return tag

@error_handling
def get_share(self,response):
	share = response.xpath(path).extract()
	return share
