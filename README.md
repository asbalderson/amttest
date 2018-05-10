[![Build Status](https://travis-ci.com/asbalderson/amttest.svg?branch=master)](https://travis-ci.com/asbalderson/amttest)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5367f199992041cea4fc8f700de21fe7)](https://www.codacy.com/app/asbalderson/amttest?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=asbalderson/amttest&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/asbalderson/amttest/branch/master/graph/badge.svg)](https://codecov.io/gh/asbalderson/amttest)

# amttest

A basic API for creating multiple choice tests.  Users are stored based on
facebook uid.  Tests (exams) are broken into sections, and random questions are
chosen from each section, answers and question order is scrambled.  Tests are
graded and stored as certificates for each user based on the exam requirements
at the time of grading.

A front-end (UI) for this project is under development (at the time of this
writing) by [dpat](https://github.com/dpat).

## Prereqs

Requirements are meant to be installed via pip, the requirements likely exist
from apt, but the project was designed to run with pip.
```
$ pip3 install --user --requirements requirements.txt
```

## Install

This api is meant to be run as a command line script, after installation.  The
prereqs will be installed while the package is being installed and ready to go.
```
$ pip3 install --user .
```

## Using amttest
### Help
There are a variety of options while running the api, to get a full list of
options run:

```
$ amttest -h
```
Finally, the api supports logging.  Everything which is a warning message or
worse is logged in /var/log by default.  More information can be logged (and
displayed) using additional options.  See the help for more details.

### Database
Amttest needs to setup a database to store the users, tests, and certificates.
First the database needs to be created.  Currently amttest runs on an sqlite
database and is stored /var/cache/amttest.
sudo is needed to create the database in /var/cache, because permissoins.
```
$ sudo amttest init
```

### Token
Any request that requires a write operation (delete, post, put) requires a
token generated from amttest and stored in the database.  This is to help
prevent unwanted users from deleting and modifying existing data.  To generate
a new token run
```
$ sudo amttest token
```
To view existing tokens run
```
$ sudo amttest token --list
```
Tokens must be sent as a header with write required requests under the name
token.  i.e. Token=<string of characters> inside the headers of the request.
Headers were chosen to pass the token instead of URL parameters for security
reasons.  I understand that this can be tricky with javascript.  Deal with it.

### Import
In the case of needing to add a large number of questions and answers to the
database in one pass, an import feature was included.  It runs by reading in a
table of questions from a .csv file and dumping the values into te database.
Section information will have to be updated after the questions have been
imported, but this should be much easier for managing a large number of files.
A route to handle this import will be added eventally.  An example csv file is
included in the [data](./data) directory.
```
$ sudo amttest import <file.csv> <name of test>
```
Note that name of test will need to be in quotes if it is more than one word.
see help for more information.

### Run
Running the api is very simple.
```
$ sudo amttest run [--ip <ip address>] [--port <port>]
```
By default can be reached at http://localhost:5000/amttest/api/<route>

# Routes
See [Routes](./amttest/routes/README.md)