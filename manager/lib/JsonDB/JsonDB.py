import os
import json
from .Filter import Filter
from .JsonObject import JsonObject, Get

class JsonDB:

	def __init__(self,name,path="None"):		
		self.name = name
		if path == "None":
			self.path = os.getcwd()+f"\\{self.name}.json"
		else:
			self.path = path+f"\\{self.name}.json"
		self.db = self.load(self.path)		
		self.get = Get(self.db)		

	def load(self,path):		
		if os.path.exists(path):			
			self.db = self._load(path,"r")
		else:
			self.db = self._load(path,"x")
		return self.db

	def _load(self,path,acc):
		if acc == "x":
			try:
				open(path,acc).write("{}")
				return json.load(open(path,"r"))
			except:
				return json.load(open(path,"r"))
		else:
			return json.load(open(path,acc))

	def commit(self):
		try:
			json.dump(self.db , open(self.path, "w"))
			return True
		except Exception:
			return False	

	
	def add(self,key,value):
		try:
			self.db[key] = value
			return True
		except Exception:			
			return False

	def get_or_set(self,key,value):		
		if len(self._search_key(key)) > 0:			
			return self.get(key)
		else:
			self.set(key,value)
			return self.get(key)

	def _search_key(self,term):
		find_area = self.db
		founded = []
		for f in find_area:						
			if str(term) == str(f):
				founded.append(f)					
		return founded

	def set(self,key,value):
		try:
			self.db[key] = value
			self.commit()
			return True
		except Exception:
			return False

	def delete(self , key):
		if not key in self.db:
			return False
		else:
			del self.db[key]
			return True

	def clear(self):
		try:
			self.db.clear()		
			return True
		except Exception:
			return False
