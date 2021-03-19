class Filter:
	
	def __init__(self, obj):
		self.obj = obj


	def less_than(self,key,term):		
		if type(term) == int:
			find_area = self.obj
			founded = []
			for f in find_area:				
				if f[key] < term:
					founded.append(f)
			return founded
		else:
			raise TypeError

	def greater_than(self,key,term):
		find_area = self.obj
		founded = []
		for f in find_area:				
			if f[key] > term:
				founded.append(f)
		return founded

	def equal_to(self,key,term):
		find_area = self.obj
		founded = []
		for f in find_area:				
			if f[key] == term:
				founded.append(f)
		return founded

	def not_equal_to(self,key,term):
		find_area = self.obj
		founded = []
		for f in find_area:				
			if f[key] != term:
				founded.append(f)
		return founded
