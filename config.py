import json
import os

path = os.path.realpath(__file__)
path = path[:path.rindex("/")]
config_file = f"{path}/config.json"


class Config:
	def __init__(self):
		with open(config_file) as cf:
			self.config = json.loads(cf.read())


	def write(self, key, value):
		self.config[key] = value

	def read(self, key):
		if key not in self.config or str(self.config[key]).strip() == '':
			return None
		return self.config[key]

	def save(self):
		config_txt = json.dumps(self.config, indent=4)
		with open(config_file, 'w') as cf:
			cf.write(config_txt)