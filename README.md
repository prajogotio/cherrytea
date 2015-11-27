#CherryTea

            CCCC                              TTTTTTTT
           CC   C  h                    y   y    TT          aaa
          CC       h     eee  rrrr rrrr y   y    TT   eee       a
          CC       hhh  e   e r    r     y y     TT  e   e   aaaa
          CC       h  h eeeee r    r      y      TT  eeeee  a   a
           CC   C  h  h e     r    r      y      TT  e      a   a
            CCCC   h  h  eee  r    r     y       TT   eee    aaaa

================================================================================
                                   Objective 
================================================================================
This is a 3rd Year Group Project @ Imperial College London [ONGOING]
Group mates: Chen Chin Jieh, Nigel Kong, Sumer Sinha
Submission deadline: January 2016


Main objectives:
1. Be the 'kickstarter.com' for charity projects
2. Allow charitable organizations to publish 'projects' which focus on 
   specific cause. Each project has its autonomous donation goals and 
   objectives.
3. Improve charity-donator interaction
   - Donators can 'follow' projects for new updates
   - Projects can broadcast news, and donators can like/reply to them
   - Donation goal is clearly communicated by the project manager to donators
4. Recommend charitable projects to donators, based on their donation history/
   causes that they identify with
5. Provide a payment platform by integrating well-established payment API


================================================================================
                                Environment setup
================================================================================
This section explains how to start working on the source codes.

1. Getting a local copy of cherrytea
   1.1 run git clone of this repository to your favorite local directory
   1.2 run git remote add origin <url to repo> as necessary

2. Install PostgreSQL on your machine
   There are plenty of resources out there, follow them and you should be
   fine. Make sure you manage to run a postgresql server on your machine.
   You will need it for server-side code testing and debugging. Also make
   sure that you have postgres command line tools in your environment path.

   Additional notes:  If you are on windows, you may need to setup cygwin. 
   More info [here](http://www.davidbaumgold.com/tutorials/set-up-python-windows/).

3. Getting Virtual Environment set up
   The app is built on top of python stack, hence we are using something 
   called virtualenv to help us manage our python libraries. Note: We are
   using python 2.7.x, not python 3.
   
   3.1 Look up how to install virtualenv on your com.
  
   3.2 Go to root directory of your local copy of the cloned cherrytea, 
   then run: `virtualenv venv`. That will create a python environtment
   inside your cherrytea folder. 

   3.3 Everytime you want to start working, run: 
   `source venv/bin/activate`. This command will activate the virtual 
   environment where we can start running our python stack.

   3.4 Install all the needed libraries by running:
   `pip install -r requirements.txt`

4. Initialize cherrytea database
   The next thing you want to do is to initialize the cherrytea database.
   To do this, firstly you need to create the postgres database using
   createdb command. 

   4.1 Start your postgres server (on Mac you can simply double click on
   Postgres.app in your Application folder).

   4.2 run `createdb cherryteadb`

   Once the database has been created, you can populate the database by 
   calling the init_db function in cherrytea/dbapi.py. (You can use python 
   shell to do it.)

5. Start working!
   5.1 Go through Flask to understand how the routing will be done later.

   5.2 Go through Flask-SQLAlchemy to understand more clearly how to use
   this convoluted stuff, so you can extend the database functionality.

   5.3 Go through JS/CSS for our frontend UI design later.

   5.4 Go through JS-XMLHttpRequest which will be one of our mean to
   interact with cherrytea server

   5.5 When in doubt, WHATSAPP

6. God speed, hope we can finish on time!


================================================================================
                                 Schema Design
================================================================================
This section serves as documentation on the DB schema design.

1. Charity project
proj
    (proj_id, owner_id, date_created, proj_name, proj_desc, location, category,
     charity_org, donation_total, donation_goal, status, num_followers, 
     other_info, paypal_id)

Notes:
 *  status     : ongoing/concluded
 *  other_info : allow proj pages to contain html tags (<movie>,<img>,etc)
 *  paypal_id  : payment account for the project (may need to be expanded 
                 depending ont the info required)
 *  category   : the cause of the charity


1.1 Charity project activity broadcast
proj_broadcast
    (broadcast_id, proj_id, date_broadcasted, content, num_likes)

proj_broadcast_reply
    (reply_id, broadcast_id, user_id, content, date_replied)

proj_broadcast_like
    (broadcast_id, user_id)


1.3 Charity project follower list
proj_follower(proj_id, follower_id)


2. User
users
    (user_id, username, password, user_type, paypal_id, date_joined,
    time_last_active, charity_number, verified, address, org_id, email)

Notes:
 *  type           : individual/organization
 *  charity_number : charity_number registered, for verification of organization
 *  verified       : true/false, depending whether the organization passes
                     verification
 *  address        : country/city
 *  org_id         : id of organisation user is affliated to


3. Donation history
donation
    (donation_id, user_id, proj_id, date_donated, amount, paypal_id)

Notes:
 *  amount : in terms of USD

4. Paypal Info
paypal
	(paypal_id, ...other details)

5. User Profile
profile
    (profile_id, user_id, first_name, last_name, date_of_birth, bio,
     profile_pic, address)

profile_pic
    (pic_id, pic_url, pic_data)