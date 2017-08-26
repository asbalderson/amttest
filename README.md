NOT YET IN MARKDOWN

Orignially I planned to write this in python using flask and a MongoDB to store 
the information.  I may change the plan to use MySQL to store the data because
I can do lookups and make things a bit more clean and efficient.  wont be a big
change for the front end, so that design decision will be figured out when when
the code is being written.

LOGIN:
	Plan to use the facebook API to have logins use facebook authentication.
	I'm not sure what information will be available to us, but hopefully some
	level of email, name, etc.  The admin(s) might need to have their own seperate
	login information unless we can have a closed group for the admins/GMR and
	facebook look up the group and make the admin pages available.

ADMIN ROUTE:
	The admin should be able to view and modify all existing tests and questions as 
	well as all the users who have taken the test within some time limit (1 year?).

	The ordering will seem a little backward here, but im a programmer and that's
	how we think sometimes

	1) Create a new section and add questions
		A) /sections/section_name should create a new blank section for questions
		B) select the section from /sections (this is where we get the uid)
		C) create a new qestion from /sections/section id/question (see 272)
		D) Do A-C for as many sections and questions as needed
	2) Create a test
		A) /tests/test_name will create a new blank test
		B) select the test from /tests
		C) select the sections to take questions from /sections and choose how many
		   questions to take from each section, number correct needed to pass, time
		   limit, etc.  see 378
	3) view results
		A) /users should get all the relavent user information and can be posted in
		   a nice pretty table, an export to xls can be added at a later date

USER ROUTE:
	User should log in and see thier own information from /users/user_uid and 
	the user_uid will probably be their email address or something facebook can
	provide.  they should be able to select a test to take from available tests
	at /tests and the test will start

	1) Taking a test
		A) A test is generated from /tests/testid (as looked up from /tests before)
		B) User checks the ULA or whatever we call it, and the timer starts once
		they click accept.
		C) timer should run from the frontend :)
		D) User answers all the questions, I'd like to check all the answers at the
		   end and log the score all at once.  sending back the API to check the 
		   questions is still kinda being worked out, but it shouldnt be too big 
		   of a deal. If MySQL is used, we can just look up the question by UID.
		   questions need to be graded based on the text in the answer, which will
		   allow for random question selection.
		E) Use /certificate/userid/testid to update the number correct for that
		   test. 
		F) look up the user again from /user/userID and report the results, the API
		   can calculate if they passed or not on the fly.

