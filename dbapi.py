from app import db
import csv, datetime, os

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
	proj_pic = db.Column(db.Integer, db.ForeignKey('profile_pic.pic_id'))

	owner = db.relationship('User', backref='projects')
	followers = db.relationship('User', secondary=proj_follower, backref='following')

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
	content = db.Column(db.Text, nullable=False)
	num_likes = db.Column(db.Integer)

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
	profile_pic_id = db.Column(db.Integer, db.ForeignKey('profile_pic.pic_id'))
	address = db.Column(db.String())

	user = db.relationship('User', backref='profile')

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

	def __repr__(self):
		return '<Profile[{id}] - {username}>'.format(id=self.profile_id,username=self.user.username)



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
			params['owner_id'] = None
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
def create_project(owner_id, proj_name, proj_desc, location, category, donation_goal, charity_org=None, other_info=None, proj_pic=None):
	try:
		params = {'proj_name':proj_name,
				  'proj_desc':proj_desc,
				  'location':location,
				  'category':category,
				  'charity_org':charity_org,
				  'donation_goal':donation_goal,
				  'other_info':other_info,
				  'proj_pic':proj_pic,
				  'date_created':datetime.datetime.utcnow()}
		p = Project(**params)
		u = User.query.filter(User.user_id==owner_id).first()
		u.projects.append(p)
		db.session.add(p)
		db.session.commit()
		return {'success':True, 'proj_id':p.proj_id}
	except:
		return {'success':False}


def follow_project(user_id, proj_id):
	try:
		u = User.query.filter(User.user_id==user_id).first()
		p = Project.query.filter(Project.proj_id==proj_id).first()
		p.followers.append(u)
		db.session.commit()
		return True
	except:
		return False

def post_broadcast(proj_id, content):
	try:
		params = {'date_broadcasted':datetime.datetime.utcnow(),
				  'content':content}
		b = Broadcast(**params)
		p = Project.query.filter(Project.proj_id==proj_id).first()
		p.broadcasts.append(b)
		db.session.add(b)
		db.session.commit()
		return True
	except:
		return False

def like_broadcast(broadcast_id, user_id):
	try:
		b = Broadcast.query.filter(Broadcast.broadcast_id==broadcast_id).first()
		u = User.query.filter(User.user_id==user_id).first()
		b.likers.append(u)
		db.session.commit()
		return True
	except:
		return False

def reply_broadcast(broadcast_id, user_id, content):
	try:
		params = {'content':content,
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
		return True
	except:
		return False

def record_donation(user_id, proj_id, amount, paypal_id=None):
	try:
		params = {'amount':amount,
				  'paypal_id':paypal_id,
				  'date_donated':datetime.datetime.utcnow()}
		d = Donation(**params)
		u = User.query.filter(User.user_id==user_id).first()
		p = Project.query.filter(Project.proj_id==proj_id).first()
		#d.donator.append(u)
		#d.proj.append(p)
		u.donations.append(d)
		p.donations.append(d)
		p.donation_total += amount
		db.session.add(d)
		db.session.commit()
		return True
	except:
		return False

def create_user_profile(user_id, first_name=None, last_name=None, date_of_birth=None, bio=None, profile_pic=None):
	try:
		params = {'first_name':first_name,
				  'last_name':last_name,
				  'date_of_birth':date_of_birth,
				  'bio':bio,
				  'profile_pic':profile_pic}
		p = UserProfile(**params)
		u = User.query.filter(User.user_id==user_id).first()
		#p.user.append(u)
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