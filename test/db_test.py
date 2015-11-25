from cherrytea.dbapi import *

def check_and_print(val):
	if val:
		print "Success"
	else:
		print "Fail"

def break_test_db():
	init_db()
	all_tests = [
		create_user('changhong','changhong',User.USER_TYPE_INDIVIDUAL,address='Wilson House, UK'),
		create_user('reddishcross','reddishcross',User.USER_TYPE_ORGANIZATION,charity_number='1344-58137-UG-1341',verified=User.IS_VERIFIED),
		create_project(1, 'Save Sumer Sinha', 'Let\' save sumer sinha from bad grades!', 'London', 'welfare', 150125, 'Reddish Cross'),
		follow_project(1, 1),
		follow_project(2, 3),
		follow_project(1, 4),
		follow_project(2, 5),
		post_broadcast(1, 'We almost saved the world!'),
		post_broadcast(2, 'But somehow we failed'),
		post_broadcast(3, 'But that\' fine we can try again next time'),
		post_broadcast(4, 'So we need more of ur money!'),
		like_broadcast(1, 1),
		like_broadcast(2, 1),
		like_broadcast(3, 2),
		like_broadcast(1, 4),
		like_broadcast(3, 5),
		reply_broadcast(4, 1, 'Boo hooooo!'),
		reply_broadcast(4, 2, 'Are you freaking serious!!'),
		reply_broadcast(4, 3, 'nvm here is my money'),
		record_donation(1, 1, 150000),
		record_donation(1, 2, 200000),
		record_donation(2, 4, 100000),
		create_user_profile(1, 'Prajogo', 'Tio', '19930316', 'The most generous donator of all time'),
		create_user_profile(2, 'Chin', 'Chen', bio='My name is jumbled up!!!!'),
		create_user_profile(3, 'Kwokokwokowko', 'Kong', bio='Mine tooo!!!'),
		create_user_profile(4, 'Sumer', 'Sinha', bio='I am the second most generous donator so far!'),
	]

	for v in all_tests:
		check_and_print(v)

