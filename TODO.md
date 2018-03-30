# Flow:
## User
1) user logs in using facebook api (good luck)
2) User elects to take a test
3) back end generates a random test and returns it to the front end
4) front end presents the test, user takes test
5) front end sends results to back end, back end grades the test and
   reports back the results
6) back end stores results
7) front end presents results

2b) user elects to view past tests
3) front end asks for results from back end
4) back end returns results
5) front end displays results, as a table

## admin
1) logs in with an admin account (can we look up groups from facebook? and have them be an admin if they are in a group?)
### views:
  - view all sections
  - view all questions in a section
     - edit a question in a section (add, remove, modify)
  - eventual way to upload full sets of questoins from xls (alex will do manual for first one)
  - all test results
  - passed test results

# David

1) set up this structure as a django app using the @approute in the current python, make changes as needed
2) figure out how you want the data from alex, really simple
3) figure out how to deal with post, put, delete, get requests
4) facebook api: https://developers.facebook.com/docs/facebook-login
4a) figure out how to call api's from django :)
4b) to be safe, tell alex what data you get once you call the login api
5) if possible, figure out when you are calling the back end and what you want from it
6) setup admin page

# Alex
1) write a deployment method for back end, and set up instructions for setting it up
2) work on basic mongo integration and set up, create needed code there
3) once back end from david, create basic functios to return dummy data
4) write real functions
5) set up run environment
6) deploy

# timeline
lets plan on touching base 2 x week + complete days
monday, thursday

project needs to be done by may 13, possibly may 5!!!
april 10) david through 2, alex has development environement depl0y (1)
april 16) alex has dummy functions ( through 3), david fb api, request method learning
april 30) alex has fully working functions, full user front end
may 5) admin page shell, admin functions
may 11) admin page working, feature complete
may 12) deploy
may 13: working demo



