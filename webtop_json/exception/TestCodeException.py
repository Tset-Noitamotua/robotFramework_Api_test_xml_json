class TestCodeException(Exception):
    def __init__(self, value):
        self.value = 'Test Code - ' + value
    def __str__(self):
        return repr(self.value)
		
if __name__ == "__main__": 
	raise TestCodeException('test');