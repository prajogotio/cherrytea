from app import db
import csv, datetime, os, time

def setAttributes(obj, params):
	for k in params:
		if (params.get(k)):
			setattr(obj, k, params.get(k))

# Relationship
proj_follower = db.Table('proj_follower',
					  db.Column('follower_id', db.Integer, db.ForeignKey('users.user_id'),nullable=False),
					  db.Column('proj_id', db.Integer, db.ForeignKey('proj.proj_id'),nullable=False),
					  db.PrimaryKeyConstraint('follower_id', 'proj_id'))

proj_broadcast_like = db.Table('proj_broadcast_like',
					  db.Column('broadcast_id', db.Integer, db.ForeignKey('proj_broadcast.broadcast_id'),nullable=False),
					  db.Column('liker_id', db.Integer, db.ForeignKey('users.user_id'),nullable=False),
					  db.PrimaryKeyConstraint('liker_id', 'broadcast_id'))

# Entity
class User(db.Model):
	# Constants
	USER_TYPE_INDIVIDUAL = "ind"
	USER_TYPE_ORGANIZATION = "org"
	IS_VERIFIED = 1
	IS_NOT_VERIFIED = 0

	# Schema
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	user_type = db.Column(db.String(length=4), nullable=False)
	paypal_id = db.Column(db.Integer, db.ForeignKey('paypal.paypal_id'))
	date_joined = db.Column(db.DateTime)
	time_last_active = db.Column(db.DateTime)
	charity_number = db.Column(db.String())
	verified = db.Column(db.Integer, default=IS_NOT_VERIFIED)
	address = db.Column(db.String())
	email = db.Column(db.String())

	# affliation
	org_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	members = db.relationship('User', backref=db.backref('affliated_to', remote_side=[user_id]))

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<User[{id}] - {username}>'.format(id=self.user_id, username=self.username)

class Project(db.Model):
	# Constant
	STATUS_ONGOING = 0
	STATUS_CONCLUDED = 1

	# Schema
	__tablename__ = 'proj'
	proj_id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
	date_created = db.Column(db.DateTime)
	proj_name = db.Column(db.String(), nullable=False)
	proj_desc = db.Column(db.Text, nullable=False)
	location = db.Column(db.String())
	category = db.Column(db.String())
	charity_org = db.Column(db.String())
	donation_total = db.Column(db.Float,default=0)
	donation_goal = db.Column(db.Float)
	status = db.Column(db.Integer,default=STATUS_ONGOING)
	num_followers = db.Column(db.Integer,default=0)
	other_info = db.Column(db.Text)
	paypal_id = db.Column(db.Integer, db.ForeignKey('paypal.paypal_id'))
	proj_pic_id = db.Column(db.Integer, db.ForeignKey('profile_pic.pic_id'))
	num_of_donations = db.Column(db.Integer, default=0)


	owner = db.relationship('User', backref='projects')
	followers = db.relationship('User', secondary=proj_follower, backref='following')
	proj_pic = db.relationship('ProfilePicture', backref='proj')

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Project[{id}] - {title}>'.format(id=self.proj_id, title=self.proj_name)


class Broadcast(db.Model):
	__tablename__ = 'proj_broadcast'
	broadcast_id = db.Column(db.Integer, primary_key=True)
	proj_id = db.Column(db.Integer, db.ForeignKey('proj.proj_id'),nullable=False)
	date_broadcasted = db.Column(db.DateTime)
	title = db.Column(db.String())
	content = db.Column(db.Text, nullable=False)
	num_likes = db.Column(db.Integer, default=0)

	proj = db.relationship('Project', backref='broadcasts')
	likers = db.relationship('User', secondary=proj_broadcast_like, backref='liked_broadcasts')

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Broadcast[{id}] - {title}>'.format(id=self.broadcast_id, title=self.proj.proj_name)

class BroadcastReply(db.Model):
	__tablename__ = 'proj_broadcast_reply'
	reply_id = db.Column(db.Integer, primary_key=True)
	broadcast_id = db.Column(db.Integer, db.ForeignKey('proj_broadcast.broadcast_id'),nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
	content = db.Column(db.Text, nullable=False)
	date_replied = db.Column(db.DateTime)

	broadcast = db.relationship('Broadcast', backref='replies')
	user = db.relationship('User', backref='comments')

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<BroadcastReply[{id}] - {title}>'.format(id=self.reply_id, title=self.user.username)

# class BroadcastLike(db.Model):
# 	__tablename__ = 'proj_broadcast_like'
# 	broadcast_id = db.Column(db.Integer, db.ForeignKey('proj_broadcast.broadcast_id'), primary_key=True)
# 	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
# 	date_liked = db.Column(db.DateTime)

# 	broadcast = db.relationship('Broadcast', backref='likes')
# 	user = db.relationship('User', backref='liked')

# 	def __init__(self, **kwargs):
# 		for key in kwargs:
# 			setattr(self, key, kwargs[key])

# 	def __repr__(self):
# 		return '<BroadcastLike[{projectname}] - [{username}]>'.format(projectname=self.broadcast.proj.proj_name, username=self.user.username)



# class ProjectFollowerList(db.Model):
# 	__tablename__ = 'proj_follower'
# 	proj_id = db.Column(db.Integer, db.ForeignKey('proj.proj_id'), primary_key=True)
# 	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
	
# 	user = db.relationship('User', backref='following')
# 	proj = db.relationship('Project', backref='follower')

# 	def __init__(self, **kwargs):
# 		for key in kwargs:
# 			setattr(self, key, kwargs[key])

# 	def __repr__(self):
# 		return '<Follower[{projectname}] - [{username}]>'.format(projectname=self.broadcast.proj.proj_name, username=self.user.username)

class Donation(db.Model):
	__tablename__ = 'donation'

	donation_id = db.Column(db.Integer, primary_key=True)
	donator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	proj_id = db.Column(db.Integer, db.ForeignKey('proj.proj_id'), nullable=False)
	date_donated = db.Column(db.DateTime)
	amount = db.Column(db.Float, nullable=False)
	paypal_id = db.Column(db.Integer, db.ForeignKey('paypal.paypal_id'))

	donator = db.relationship('User', backref='donations')
	proj = db.relationship('Project', backref='donations')

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Donation[{id}] - [{username}, {amount}]>'.format(id=self.donation_id,username=self.donator.username,amount=self.amount)


class PaypalAccount(db.Model):
	__tablename__ = 'paypal'

	paypal_id = db.Column(db.Integer, primary_key=True)
	# other details
	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Paypal[{id}]>'.format(id=self.paypal_id)

class UserProfile(db.Model):
	__tablename__ = 'profile'
	profile_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
	first_name = db.Column(db.String())
	last_name = db.Column(db.String())
	date_of_birth = db.Column(db.DateTime)
	bio = db.Column(db.Text)
	advocate = db.Column(db.Text)
	profile_pic_id = db.Column(db.Integer, db.ForeignKey('profile_pic.pic_id'))
	address = db.Column(db.String())

	user = db.relationship('User', backref='profile')

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Profile[{id}] - {username}>'.format(id=self.profile_id,username=self.user.username)

class Notification(db.Model):
	UNREAD = 0
	READ = 1

	__tablename__ = 'notif'
	notif_id = db.Column(db.Integer, primary_key=True)
	recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	content = db.Column(db.String())
	date_created = db.Column(db.DateTime)
	status = db.Column(db.Integer, default=UNREAD)


	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Notification[{id}] - {content}>'.format(id=self.notif_id,username=self.content)



class ProfilePicture(db.Model):
	__tablename__ = 'profile_pic'
	pic_id = db.Column(db.Integer, primary_key=True)
	pic_url = db.Column(db.String())
	pic_data = db.Column(db.LargeBinary)

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<ProfilePicture[{id}]>'.format(id=self.pic_id)


def get_filepath(x):
	return os.path.abspath(os.path.join(os.path.dirname(__file__),x))

def init_db():
	db.drop_all()
	db.create_all()
	with open(get_filepath('init_data/user.csv'), 'r') as f:
		reader = csv.reader(f)
		fields = next(reader, None)
		for row in reader:
			params = dict(zip(fields, row))
			db.session.add(User(**params))
		db.session.commit()
	with open(get_filepath('init_data/proj.csv'), 'r') as f:
		reader = csv.reader(f)
		fields = next(reader, None)
		for row in reader:
			params = dict(zip(fields, row))
			u = db.session.query(User).filter(User.user_id==int(params['owner_id'])).first()
			p = Project(**params)
			u.projects.append(p)
			db.session.add(p)
		db.session.commit()


# User Registration
def create_user(username,password,user_type='ind',paypal_id=None,date_joined=None,time_last_active=None,charity_number=None,verified=None,address=None,email=None):
	try:
		if not date_joined:
			date_joined = datetime.datetime.utcnow()
		if not time_last_active:
			time_last_active = date_joined
		params = {'username':username,
				  'password':password,
				  'user_type':user_type,
				  'paypal_id':paypal_id,
				  'date_joined':date_joined,
				  'charity_number':charity_number,
				  'verified':verified,
				  'address':address,
				  'email':email}
		u = User(**params)
		db.session.add(u)
		db.session.commit()
		return True
	except:
		return False


# Project registration
def create_project(owner_id, proj_name, proj_desc, location, category, donation_goal, charity_org=None, other_info=None, proj_pic_id=None):
	#try:
		params = {'proj_name':proj_name,
				  'proj_desc':proj_desc,
				  'location':location,
				  'category':category,
				  'charity_org':charity_org,
				  'donation_goal':donation_goal,
				  'other_info':other_info,
				  'proj_pic_id':proj_pic_id,
				  'date_created':datetime.datetime.utcnow()}
		p = Project(**params)
		u = User.query.filter(User.user_id==owner_id).first()
		u.projects.append(p)
		db.session.add(p)
		db.session.commit()
		return {'success':True, 'proj_id':p.proj_id}
	#except:
	#	return {'success':False}

def update_project(proj_id, proj_name=None, proj_desc=None, location=None, category=None, donation_goal=None, charity_org=None, other_info=None, proj_pic_id=None):
	#try:
		params = {'proj_name':proj_name,
				  'proj_desc':proj_desc,
				  'location':location,
				  'category':category,
				  'charity_org':charity_org,
				  'donation_goal':donation_goal,
				  'other_info':other_info,
				  'proj_pic_id':proj_pic_id,
				  'date_created':datetime.datetime.utcnow()}
		p = Project.query.filter(Project.proj_id==proj_id).first()
		setAttributes(p, params)
		db.session.commit()
		return {'success':True, 'proj_id': proj_id}
	#except:
	#	return {'success':False}


def follow_project(user_id, proj_id):
	try:
		u = User.query.filter(User.user_id==user_id).first()
		p = Project.query.filter(Project.proj_id==proj_id).first()
		p.followers.append(u)
		db.session.commit()
		return True
	except:
		return False

def unfollow_project(user_id, proj_id):
	try:
		u = User.query.filter(User.user_id==user_id).first()
		p = Project.query.filter(Project.proj_id==proj_id).first()
		p.followers.remove(u)
		db.session.commit()
		return True
	except:
		return False

def post_broadcast(proj_id, title, content):
	#try:
		params = {'date_broadcasted':datetime.datetime.utcnow(),
				  'title':title,
				  'content':content}
		b = Broadcast(**params)
		p = Project.query.filter(Project.proj_id==proj_id).first()
		p.broadcasts.append(b)
		db.session.add(b)
		db.session.commit()

		for f in b.proj.followers:
			make_notification(f.user_id, '<a href=\'/project/{proj_id}\'>{proj_name}</a> has broadcasted a new update!'.format(proj_id=b.proj.proj_id,proj_name=b.proj.proj_name))

		return True
	#except:
		#return False

def like_broadcast(broadcast_id, user_id):
	#try:
		b = Broadcast.query.filter(Broadcast.broadcast_id==broadcast_id).first()
		u = User.query.filter(User.user_id==user_id).first()
		b.likers.append(u)
		b.num_likes += 1
		db.session.commit()

		make_notification(b.proj.owner_id, '<a href=\'/user/{user_id}\'>{username}</a> liked your broadcast on <a href=\'/project/{proj_id}\'>{proj_name}</a>.'.format(user_id=user_id, username=u.username, proj_id=b.proj.proj_id, proj_name=b.proj.proj_name))

		return True
	#except:
	#	return False


def unlike_broadcast(broadcast_id, user_id):
	#try:
		b = Broadcast.query.filter(Broadcast.broadcast_id==broadcast_id).first()
		u = User.query.filter(User.user_id==user_id).first()
		b.likers.remove(u)
		b.num_likes -= 1
		db.session.commit()
		return True
	#except:
	#	return False


def reply_broadcast(broadcast_id, user_id, content):
	#try:
		params = {'broadcast_id':broadcast_id,
				  'content':content,
				  'date_replied':datetime.datetime.utcnow()}
		r = BroadcastReply(**params)
		b = Broadcast.query.filter(Broadcast.broadcast_id==broadcast_id).first()
		u = User.query.filter(User.user_id==user_id).first();
		#r.broadcast.append(b)
		#r.user.append(u)
		u.comments.append(r)
		b.replies.append(r)
		db.session.add(r)
		db.session.commit()

		make_notification(b.proj.owner_id, '<a href=\'/user/{user_id}\'>{username}</a> replied to your broadcast on <a href=\'/project/{proj_id}\'>{proj_name}</a>.'.format(user_id=user_id, username=u.username, proj_id=b.proj.proj_id, proj_name=b.proj.proj_name))
		return True
	#except:
		#return False

def record_donation(user_id, proj_id, amount, paypal_id=None, date_donated=None):
	#try:
		if not date_donated:
			date_donated = datetime.datetime.utcnow()
		params = {'amount':amount,
				  'proj_id':proj_id,
				  'paypal_id':paypal_id,
				  'date_donated':date_donated}
		d = Donation(**params)
		u = User.query.filter(User.user_id==user_id).first()
		p = Project.query.filter(Project.proj_id==proj_id).first()
		u.donations.append(d)
		p.donations.append(d)
		p.donation_total += amount
		p.num_of_donations += 1
		db.session.add(d)
		db.session.commit()

		make_notification(p.owner_id, '<a href=\'/user/{user_id}\'>{username}</a> donated ${amount} to <a href=\'/project/{proj_id}\'>{proj_name}</a>.'.format(user_id=user_id, username=u.username, proj_id=proj_id, proj_name=p.proj_name,amount=amount))
		return True
	#except:
		#return False

def create_user_profile(user_id, params):
	try:
		p = UserProfile(**params)
		u = User.query.filter(User.user_id==user_id).first()
		u.profile.append(p)
		db.session.add(p)
		db.session.commit()
		return True
	except:
		return False

def set_affliation(user_id, org_id):
	try:
		u = User.query.filter(User.user_id==user_id).first()
		o = User.query.filter(User.user_id==org_id).first()
		if o.user_type != User.USER_TYPE_ORGANIZATION:
			return False
		o.members.append(u)
		db.session.commit()
		return True
	except:
		return False

def record_prof_pic(url):
	try:
		params = {'pic_url':url}
		pp = ProfilePicture(**params)
		db.session.add(pp)
		db.session.commit()
		return {'success':True, 'pic_id':pp.pic_id}
	except:
		return {'success':False}

def get_user_profile(user_id):
	#try:
	up = UserProfile.query.filter(UserProfile.user_id==user_id).first()
	if up:
		res =  {'success':True,
				'found':True,
				'first_name':up.first_name,
				'last_name':up.last_name,
				'full_name':up.first_name +' '+ up.last_name,
				'bio':up.bio,
				'advocate':up.advocate,
				'address':up.address}
		if up.date_of_birth:
			res['date_of_birth']=time.strftime("%d %b %Y",up.date_of_birth.timetuple())
			res['date_of_birth_us']=time.strftime("%Y-%m-%d",up.date_of_birth.timetuple())
		
		if up.profile_pic_id:
			pp = ProfilePicture.query.filter(ProfilePicture.pic_id==up.profile_pic_id).first()
			res['profile_pic_url'] = pp.pic_url
		return res
	return {'success':False,'found':False}
	# except:
	# 	return {'success':False}

def get_username(user_id):
	try:
		u = User.query.filter(User.user_id==user_id).first()
		if u:
			return u.username
		return None
	except:
		return None

def get_membership(user_id):
	try:
		u = User.query.filter(User.user_id==user_id).first()
		if u:
			return u.user_type
		return None
	except:
		return None

def get_num_of_backed_projects(user_id):
	try:
		x = db.engine.execute('SELECT COUNT(DISTINCT proj_id) FROM donation WHERE donator_id='+str(user_id))
		res = x.fetchone()
		return res[0]
	except:
		return 0

def get_num_of_project_backers(proj_id):
	#try:
		x = db.engine.execute('SELECT COUNT(DISTINCT donator_id) FROM donation WHERE proj_id='+str(proj_id))
		res = x.fetchone()
		return res[0]
	#except:
	#	return 0

def get_recently_backed_projects(user_id):
	#try:
		x = db.engine.execute('SELECT d.proj_id, d.date_donated, amount, pp.pic_url, p.proj_name FROM donation d JOIN proj p ON d.proj_id = p.proj_id LEFT JOIN profile_pic pp ON pp.pic_id = p.proj_pic_id WHERE donator_id=%d ORDER BY date_donated DESC LIMIT 3' % user_id)
		res = [{'proj_id':row[0], 
				'date_donated':time.strftime('%d %b %Y', row[1].timetuple()), 
				'amount':row[2],
				'pic_url':row[3],
				'proj_name':row[4]} 
				for row in x]
		return res
	#except:
	#	return None

def get_join_date(user_id):
	try:
		u = User.query.filter(User.user_id==user_id).first();
		if u:
			return time.strftime("%b %Y", u.date_joined.timetuple())
		return None
	except:
		return None

def update_user_profile(user_id, params):
	# try:
	up = UserProfile.query.filter(UserProfile.user_id==user_id).first()
	if up:
		setAttributes(up, params)
		db.session.commit()
		return {'success':True}
	else:
		return {'success':create_user_profile(user_id, params)}
	# except:
	# 	return {'success':False}

def get_project_profile(proj_id):
	p = Project.query.filter(Project.proj_id==proj_id).first()
	if p:
		res = {'success':False,
			   'proj_id':p.proj_id,
			   'owner_id':p.owner_id,
			   'owner_username':p.owner.username,
			   'date_created':time.strftime('%d %b %Y', p.date_created.timetuple()),
			   'proj_name':p.proj_name,
			   'proj_desc':p.proj_desc,
			   'location':p.location,
			   'category':p.category,
			   'charity_org':p.charity_org,
			   'donation_total':p.donation_total,
			   'donation_goal':p.donation_goal,
			   'status':p.status,
			   'num_followers':p.num_followers,
			   'other_info':p.other_info,
			   'num_of_backers':get_num_of_project_backers(proj_id)
			   }
		if p.proj_pic_id:
			pic = ProfilePicture.query.filter(ProfilePicture.pic_id==p.proj_pic_id).first()
			res['proj_pic_url'] = pic.pic_url
		return res
	return {'success':False}

def get_recent_projects(size=3, offset=None):
	q = 'SELECT proj_id, category, proj_name, num_of_donations, pic_url FROM proj p LEFT JOIN profile_pic pp ON p.proj_pic_id = pp.pic_id ORDER BY date_created desc LIMIT %d' % size
	if offset:
		q += ' OFFSET %d' % offset
	res = db.engine.execute(q);
	
	ret = [{'proj_id':r[0],
			'category':r[1],
			'proj_name':r[2],
			'donations':r[3],
			'proj_pic_url':r[4]}
			for r in res]
	return ret

def get_popular_projects(size=3, offset=None):
	q = 'SELECT proj_id, category, proj_name, num_of_donations, pic_url FROM proj p LEFT JOIN profile_pic pp ON p.proj_pic_id = pp.pic_id ORDER BY num_of_donations DESC, date_created DESC LIMIT %d' % size
	if offset:
		q += ' OFFSET %d' % offset
	res = db.engine.execute(q);
	
	ret = [{'proj_id':r[0],
			'category':r[1],
			'proj_name':r[2],
			'donations':r[3],
			'proj_pic_url':r[4]}
			for r in res]
	return ret


def search_project(search_term, options={}):
	q = 'SELECT p.proj_id, p.proj_name, p.proj_desc, p.date_created, p.num_of_donations, p.category, \
				u.username, u.user_id,\
				pp.pic_url\
		FROM proj p\
		JOIN users u\
		ON u.user_id = p.owner_id\
		LEFT JOIN profile_pic pp\
		ON pp.pic_id = p.proj_pic_id\
		WHERE LOWER(p.proj_name) like \'%%{0}%%\'\
		OR LOWER(p.proj_desc) like \'%%{0}%%\'\
		OR LOWER(u.username) like \'%%{0}%%\'\
		OR LOWER(p.category) like \'%%{0}%%\'\
		OR LOWER(p.location) like \'%%{0}%%\'\
		ORDER BY p.num_of_donations DESC, p.date_created DESC\
		LIMIT {1} OFFSET {2}\
		'.format(search_term.lower(), options.get('size', 10), options.get('offset', 0))
	res = db.engine.execute(q).fetchall()
	
	ret = {'result':[dict(row) for row in res]}

	for r in ret['result']:
		r['date_created'] = time.strftime('%d %b %Y', r['date_created'].timetuple())

	q = 'SELECT COUNT(*) as num_of_matches\
		FROM proj p\
		JOIN users u\
		ON u.user_id = p.owner_id\
		WHERE LOWER(p.proj_name) like \'%%{0}%%\'\
		OR LOWER(p.proj_desc) like \'%%{0}%%\'\
		OR LOWER(u.username) like \'%%{0}%%\'\
		OR LOWER(p.category) like \'%%{0}%%\'\
		OR LOWER(p.location) like \'%%{0}%%\'\
		'.format(search_term.lower())
	res = db.engine.execute(q).fetchone()
	ret['num_of_matches'] = res[0]
	ret['size'] = options.get('size', 10)
	ret['offset'] = options.get('offset', 0)
	ret['search_term'] = search_term
	return ret
	
def is_project_follower(proj_id, user_id):
	res = db.engine.execute('SELECT true FROM proj_follower WHERE proj_id={0} AND follower_id={1}'.format(proj_id, user_id))
	x = res.fetchall()
	return True if x else False

def get_recent_donations(proj_id):
	q = 'SELECT donator_id, amount, date_donated, username\
	     FROM donation d\
	     JOIN users u\
	     ON u.user_id = d.donator_id\
	     WHERE d.proj_id = {0}\
	     ORDER BY date_donated DESC\
	     LIMIT 7'.format(proj_id)
	res = db.engine.execute(q)

	ret = [dict(r) for r in res]
	for r in ret:
		r['date_donated'] = time.strftime('%d %b %Y', r['date_donated'].timetuple())
	return ret

def get_recent_follower_info(proj_id):
	q = 'SELECT follower_id, username, \
		 		COALESCE(pic_url, \'/static/img/no_prof_pic.jpg\') as pic_url\
		 FROM proj_follower pf\
		 JOIN users u\
		 ON u.user_id = pf.follower_id\
		 LEFT JOIN profile p\
		 ON p.user_id = u.user_id\
		 LEFT JOIN profile_pic pp\
		 ON p.profile_pic_id = pp.pic_id\
		 WHERE pf.proj_id = {0}\
		 LIMIT 7'.format(proj_id)
	res = db.engine.execute(q)
	ret = {'followers':[dict(r) for r in res]}

	q = 'SELECT COUNT(follower_id) FROM proj_follower WHERE proj_id={0}'.format(proj_id)
	res = db.engine.execute(q)
	row = res.fetchone()
	ret['num_followers'] = row[0]
	return ret

def get_recent_broadcasts(proj_id, size=5):
	q = 'SELECT broadcast_id, title, content, num_likes, date_broadcasted FROM proj_broadcast WHERE proj_id={0} ORDER BY date_broadcasted DESC LIMIT {1}'.format(proj_id, size)
	res = db.engine.execute(q)
	ret = [dict(r) for r in res]
	for r in ret:
		r['date_broadcasted'] = time.strftime('%d %b %Y', r['date_broadcasted'].timetuple())
	return ret

def get_broadcast_reply(broadcast_id, size=5, offset=0):
	q = 'SELECT u.user_id, content, date_replied, username FROM proj_broadcast_reply pbr JOIN users u ON pbr.user_id = u.user_id WHERE broadcast_id = {0} ORDER BY date_replied DESC LIMIT {1} OFFSET {2}'.format(broadcast_id, size, offset)
	res = db.engine.execute(q)
	replies = [dict(r) for r in res]
	for r in replies:
		 r['date_replied'] = time.strftime('%d %b %Y', r['date_replied'].timetuple())
	return {'replies':replies,
			'offset':offset,
			'size':size}

def is_broadcast_liked(broadcast_id, user_id):
	b = Broadcast.query.filter(Broadcast.broadcast_id==broadcast_id).first()
	u = User.query.filter(User.user_id==user_id).first()
	return u in b.likers

def get_owned_projects(user_id, options={}):
	q = 'SELECT p.proj_id, p.proj_name, p.proj_desc, p.date_created, p.num_of_donations, p.category, \
				pp.pic_url\
		FROM proj p\
		LEFT JOIN profile_pic pp\
		ON pp.pic_id = p.proj_pic_id\
		WHERE p.owner_id = {0}\
		ORDER BY p.num_of_donations DESC, p.date_created DESC\
		LIMIT {1} OFFSET {2}\
		'.format(user_id, options.get('size', 100), options.get('offset', 0))
	res = db.engine.execute(q).fetchall()
	
	ret = [dict(row) for row in res]

	for r in ret:
		r['date_created'] = time.strftime('%d %b %Y', r['date_created'].timetuple())
	return ret

def get_donation_statistics(proj_id):
	# get donations for past 7 months
	now = datetime.date.today()
	limit = now - datetime.timedelta(days=30*7)
	q = 'SELECT SUM(amount) AS total, to_char(date_donated, \'YYYYMM\') AS month_year\
		 FROM donation \
		 WHERE proj_id={0}\
		 AND date_donated > date(\'{1}\')\
		 GROUP BY month_year\
		 ORDER BY month_year DESC\
		 LIMIT 7'.format(proj_id, time.strftime('%Y%m%d', limit.timetuple()))
	res = db.engine.execute(q)
	ret = {}
	for r in res:
		ret[r['month_year']] = r['total']
	cur_month = now.timetuple().tm_mon;
	cur_year = now.timetuple().tm_year;
	needed = []
	for i in range(7):
		if cur_month == 0:
			cur_year -= 1
			cur_month = 12
		needed.append(time.strftime('%Y%m', datetime.datetime(cur_year, cur_month, 1).timetuple()))
		cur_month -= 1

	return [{'x':time.strftime('%b %y', time.strptime(t, '%Y%m')),
		     'y':ret.get(t, 0)} for t in needed]

def make_notification(recipient_id, content):
	params = {'recipient_id':recipient_id,
			  'content':content,
			  'date_created':datetime.datetime.utcnow()}
	n = Notification(**params)
	db.session.add(n)
	db.session.commit()
	return True

def retrieve_notification(user_id, offset_id=0):
	now = datetime.date.today()
	limit = now - datetime.timedelta(days=7)
	q = "SELECT notif_id, content, date_created, status FROM notif WHERE recipient_id={0} AND date_created > date(\'{1}\') AND notif_id > {2} ORDER BY date_created DESC LIMIT 20".format(user_id, time.strftime('%Y%m%d', limit.timetuple()), offset_id)
	res = db.engine.execute(q)
	ret = [dict(r) for r in res]
	for r in ret:
		r['date_created'] = time.strftime('%d %b %Y', r['date_created'].timetuple())
	return ret

def mark_notification_as_read(notif_id):
	n = Notification.query.filter(Notification.notif_id==notif_id).first()
	n.status = Notification.READ
	db.session.commit()
	return True