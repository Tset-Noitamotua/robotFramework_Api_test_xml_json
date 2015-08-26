class APIException(Exception):
    def __init__(self, value):
        self.value = '[error_code]' + value
    def __str__(self):
        return repr(self.value)
		
if __name__ == "__main__": 
	raise APIException('test')