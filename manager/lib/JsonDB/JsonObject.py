from .Filter import Filter

class Get:

	def __init__(self,db):
		self.db =db

	def _get(self,key):
		try:			
			return JsonObject(self.db, key, self.db[key])
		except Exception as e:			
			print(e)
			return False

	def __call__(self,key):
		return self._get(key) 

class JsonObject(type({})):

	def __init__(self,db, key=None, value=None):		
		self.key = key
		self.value = value				
		self.db = db
		self[key] = self.value
		if type(self.db) == type({}):
			self.db[key] = self.value
			self.get = Get(self.value)
			self.filter = Filter(self[self.key])				

	def push(self,key,value):		
		try:
			self[self.key][key] = value
			return True
		except KeyError:
			return False
		except Exception:
			return False


	def append(self,value):
		self[self.key].append(value)
		return True

	def remove(self,value):
		if value in self[self.key]:
			self[self.key].remove(value)
			return True
		return False

	def search(self,term,include_keys=True):
		find_area = self[self.key]		
		founded = []
		for f in find_area:
			if include_keys:				
				if str(term) in str(list(f.items())):
					founded.append(f)
			else:				
				if str(term) in str(list(f.values())):
					founded.append(f)		
		return founded

	def get_or_set(self,key,value):		
		get = Get(self.db)		
		if len(self._search_key(key)) > 0:						
			return get(key)
		else:						
			self.set(key,value)
			self.commit()					
			return get(key)

	def _search_key(self,term):
		find_area = self.db		
		founded = []
		for f in find_area:
			if str(term) == str(f):
				founded.append(f)							
		return founded


	def set(self,key,value):
		try:
			self[self.key] = value
			return True
		except Exception as e:
			print(e)
			return False

	def delete(self ,key):		
		if not key in self[self.key]:
			return False
		else:
			del self[self.key][key]
			return True

	def __repr__(self):
		return str(dict(self))