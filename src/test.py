class Parent:
	def __init__(self):
		print("Initialized parent")

	def parentFunc(self):
		print("parent function")

class Functions(Parent):
	def __init__(self):
		print("Initialized")
	
	@property	
	def func1(self):
		print("func 1")
	
	def func2(self, string):
		print(string)
	
	def func3(self, function):
		function

	def func4(self):
		self.parentFunc()

testFunctions = Functions()

testFunctions.func2("this is a test")
testFunctions.func3(testFunctions.func1)

testFunctions.func4()
