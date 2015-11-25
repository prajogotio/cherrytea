import sys, csv, random, os

class DataGenerator():
	SCRIPT_PATH = os.path.dirname(__file__)
	
	def __init__(self):
		self.init_words()

	def get_filepath(self, x):
		return os.path.abspath(os.path.join(DataGenerator.SCRIPT_PATH, x))

	def init_words(self):
		# load random words
		with open(self.get_filepath('verbs.csv'), 'r') as f:
			self.verb = [r[:-1] for r in f]
		with open(self.get_filepath('adjectives.csv'), 'r') as f:
			self.adj = [r[:-1] for r in f]
		with open(self.get_filepath('adverbs.csv'), 'r') as f:
			self.adv = [r[:-1] for r in f]
		with open(self.get_filepath('nouns.csv'), 'r') as f:
			self.noun = [r[:-1] for r in f]

		# load countries
		with open(self.get_filepath('countries.csv'), 'r') as f:
			reader = csv.reader(f)
			next(reader)
			self.country = [r[1] for r in reader]

		# load names
		with open(self.get_filepath('fname.csv'), 'r') as f:
			self.fname = [r for r in f.read().splitlines()]
		with open(self.get_filepath('lname.csv'), 'r') as f:
			self.lname = [r for r in f.read().splitlines()]


	def generate_sentence(self):
		# noun adv verb adj noun adv
		l = [self.noun, self.adv, self.verb, self.adj, self.noun, self.adv]
		ret = ''
		flag = False
		for x in l:
			ret += ' ' if flag else ''
			if flag:
				ret += x[random.randint(0, len(x)-1)].lower()
			else:
				ret += x[random.randint(0, len(x)-1)].lower().title()
			flag = True
		ret += '.'
		return ret

	def generate_project_title(self):
		l = [self.noun, self.verb, self.noun]
		ret = ''
		flag = False
		for x in l:
			ret += ' ' if flag else ''
			ret += x[random.randint(0, len(x)-1)].lower().title()
			flag = True
		return ret

	def generate_country(self):
		return self.country[random.randint(0,len(self.country)-1)]

	def generate_first_name(self):
		return self.fname[random.randint(1,len(self.fname)-1)]

	def generate_last_name(self):
		return self.lname[random.randint(1,len(self.lname)-1)]

	def generate_noun(self):
		return self.noun[random.randint(0, len(self.noun)-1)]

def generate_projects():
	d = DataGenerator()
	max_owner_id = 23
	number_of_projects = 40
	with open(d.get_filepath('proj.csv'), 'w') as f:
		writer = csv.writer(f)
		f.write('owner_id,date_created,proj_name,proj_desc,location,category,charity_org,donation_goal\n');
		for i in xrange(number_of_projects):
			proj = [random.randint(0,max_owner_id), '20150'+str(random.randint(1,9))+str(random.randint(11,27)),
					d.generate_project_title(), d.generate_sentence(), d.generate_country(), d.generate_noun(),
					d.generate_first_name()+' '+d.generate_last_name(), 0, random.randint(100000,500000)]
			writer.writerow(proj)

