# Routes
Here are the routes available from the amttest api.  The methods supported,
headers required, expected payload, and return content, are all documented below

Order is based on expected use/flow for the api.

All, PUT, POST, DELETE calls require a token in the headers i.e.
Token=<40 character token>
## User
User has the following fields:
userid: Integer, generated user identifier for each user, always unique.
fbuserid: Text, the user id from facebook.  This is only used for log in, and
                should never be returned.
amt_name: Text, A users amtgard persona name, not required, good to have.  Optional
name: Text, The users real name.
email: Text, The users email address.
kingdom: Text, The kingdom that the user is a member of.  Optional
admin: Boolean, When true, the user can access the admin panel.
archive: Boolean, When true, the user is no longer available for viewing.


```
amttest/api/user
```
### GET
Get all active users

Headers: None
Payload: None
Success: 200
Response:
```
[
    {userid: 1234,
     amt_name: Toaster,
     name: Bob Barker,
     email: Bob@barker.net,
     kingdom: IMD,
     admin: False,
     archive: False
    },
    {userid: <int>,
     amt_name: <txt>,
     name: <txt>,
     email: <txt>,
     kingdom: <txt>,
     admin: <bool>,
     archive: False
    },
    ...
]
```
### POST
Create a new user based on the Facebook userid.  If the Facebook userid is
already in use, the existing user will be returned.
fburserid, name, and email are all REQUIRED for creation, other fields are
optional.

Headers: Token=<40 digit token>
Payload:
```
{
fbuserid:<txt>,
name:<txt>,
email:<txt>,
amt_name:<txt>,
kingdom:<txt>,
admin:<bool>
}
```
Success: 201
Response:
```
{userid: 1234,
 amt_name: Toaster,
 name: Bob Barker,
 email: Bob@barker.net,
 kingdom: IMD,
 admin: False,
 archive: False
}
```
--------------------------------------------------------------------------------
```
amttest/api/user/<int:userid>
```
### GET
Get an individual user based on its user id.  fbuserid is omitted for security
reasons, and it should never be needed.

Headers: None
Payload: None
Success: 200
Response:
```
{userid: 1234,
 amt_name: Toaster,
 name: Bob Barker,
 email: Bob@barker.net,
 kingdom: IMD,
 admin: False,
 archive: False
}
```

### PUT
Headers: Token=<40 digit token>
Payload:
```
{
name:<txt>,
email:<txt>,
amt_name:<txt>,
kingdom:<txt>,
admin:<bool>
}
```
Success: 204
Response: None

### DELETE
"Delete" a user.  Users are not actually deleted, their flag is set to archive.

Headers: Token=<40 digit token>
Payload: None
Success: 204
Response: None

## Exam
Exam has the following fields:
examid: Integer, the exam's identifier, always unique.
time_limit: Integer, The number of minutes given for the user to take the exam.
name: Text, The plain text name of the exam.
pass_percent: Integer, The whole number value required to pass the exam, i.e. 70.
expiration: Integer, The number of months the certifications from the exam are valid.
ula: Text, What the user agrees to before they take the exam.
archive: Boolean, When true, the exam will no longer be available from queries.

```
amttest/api/exam
```
### GET
Get all
Headers: None
Payload: None
Success: 200
Response:
```
[
    {
    examid:1234,
    time_limit:20,
    name: Rules of Play,
    pass_percent: 75,
    expiration: 12,
    ula: do not cheat,
    },
    {
    examid:<int>,
    time_limit:<int>,
    name: <txt>,
    pass_percent: <int>,
    expiration: <int>,
    ula: <txt>,
    },
    ...
]
```

### POST
Create a new exam.  The only REQUIRED value is name.

Headers: Token=<40 digit token>
Payload:
```
{
    time_limit:20,
    name: Rules of Play,
    pass_percent: 75,
    expiration: 12,
    ula: do not cheat,
}
```
Success: 201
Response:
```
{
    examid: 1234,
    time_limit:20,
    name: Rules of Play,
    pass_percent: 75,
    expiration: 12,
    ula: do not cheat,
    archive: false
}
```
--------------------------------------------------------------------------------
```
amttest/api/exam/<int:examid>
```
### GET
Get one exam from based on the examid.

Headers: None
Payload: None
Success: 200
Response:
```
{
    examid: 1234,
    time_limit:20,
    name: Rules of Play,
    pass_percent: 75,
    expiration: 12,
    ula: do not cheat,
    archive: false
}
```

### PUT
Update an existing exam.  If a value is passed in that does not exist in the
exam table, the value will be ignored.  Not all possible fields need to be
included.

Headers: Token=<40 digit token>
Payload:
```
{
    time_limit:20,
    name: Rules of Play,
    pass_percent: 75,
    expiration: 12,
    ula: do not cheat,
}
```
Success: 204
Response: None

### DELETE
Delete an exam.  Deleted exams have the archive flag set to True and will no
longer appear in queries.

Headers: Token=<40 digit token>
Payload: None
Success: 204
Response:None

--------------------------------------------------------------------------------
```
amttest/api/exam/<int:examid>/take
```
### GET
This is what is used to get a generated exam for a user to take.  The number of
questions in the exam is based on the number of active questions from each
section in the exam.  Questions are randomly selected from each section, and
the answers for each question are put in a random order.  Question order is
also scrambled.

Headers: None
Payload: None
Success: 200
Response:
```
[
    {
    questionid: 456,
    question: this is a question,
    answers: [
            {
            answerid: 4,
            answer: answer 4
            },
            {
            answreid: 3,
            answer: answer 3
            }
            ...
        ]
    },
    {
    questionid: <int>,
    question: <text>
    ansswers: [
            {
            answerid: <int>,
            answer: <txt>
            },
            ...
        ]
    },
    ...
]
```

## Section
The fields in section are:
sectionid: Integer, The unique identifier for the section.
name: Text, Name of the section as seen by the admin.
examid: Integer, Related to the exam table.  The exam that this section belongs to.
active_questions: Integer, The number of questions to use from this section for each exam.
archive: Boolean, When true, the section will no longer appear in queries.

```
amttest/api/exam/<int:exam_id>/section
```
### GET
Get all sections for a given exam

Headers: None
Payload: None
Success: 200
Response:
```
[
    {
    sectionid: 1234,
    name: General,
    examid: 2345,
    active_qustions: 3,
    archive: false
    },
    {
    sectionid: <int>,
    name: <text>,
    examid: <int>,
    active_qustions: <int>,
    archive: <boolean>
    },
    ...
]
```

### POST
Create a new section for a given examid.

Headers: Token=<40 digit token>
Payload:
```
{
    name: General,
    active_qustions: 3
}
```
Success: 201
Response:
```
{
    sectionid: 1234,
    name: General,
    examid: 2345,
    active_qustions: 3,
    archive: false
}
```
--------------------------------------------------------------------------------
```
amttest/api/section
```
### GET
Get every active section from the database.

Headers: None
Payload: None
Success: 200
Response:
```
[
    {
    sectionid: 1234,
    name: General,
    examid: 2345,
    active_qustions: 3,
    archive: false
    },
    {
    sectionid: <int>,
    name: <text>,
    examid: <int>,
    active_qustions: <int>,
    archive: <boolean>
    },
    ...
]
```
--------------------------------------------------------------------------------
```
amttest/api/section/<int:section_id>
Get the section data + all question data for any question in that section +
answers for all the questions.  It may return too much data right now.

```
### GET
Headers: None
Payload: None
Success: 200
Response:
```
{
    sectionid: 1234,
    name: General,
    examid: 2345,
    active_qustions: 3,
    archive: false
    questions: [
            {
             questionid: 234,
             question: this is a question,
             sectionid: 1234,
             used: 0,
             correct: 0,
             archive: false,
             answers: [
                {
                answerid: 34,
                answer: this is an answer,
                questionid: 234,
                correct: false,
                chosen: 0
                },
                ...
             ]
            },
            ...
        ]
}
```

### PUT
Update values in a given section. Values which do not match a database field
for section will be ignored.  Not all fields need to be included.

Headers: Token=<40 digit token>
Payload:
```
{
    name: General,
    examid: 2345,
    active_qustions: 3
}
```
Success: 204
Response:

### DELETE
Delete an active section.  Deleted section only have their archive flag set to
True.

Headers: Token=<40 digit token>
Payload: None
Success: 204
Response: None

## Question
The fields in question are:
questionid: Integer, The unique identifier for the question.
question: Text, Actual text of the given question.
sectionid: Integer, Related to the section table.  The section that this
                    question belongs to
used: Integer, A count for how many times this question has been asked. Plans
               to use this for statistics.
correct: Integer, How many times this question has been answered correctly.
archive: Boolean, When true, will no longer appear in queries.

```
amttest/api/section/<int:section_id>/question
```
### POST
Create a new question for a given section.

Headers: Token=<40 digit token>
Payload:
```
{
    question: this is a question
}
```
Success: 201
Response:
```
{
    questionid: 234,
    question: this is a questions,
    sectionid: 1234,
    used: 0,
    correct: 0,
    archive: false
}
```
--------------------------------------------------------------------------------
```
amttest/api/question/<int:questionid>
```
### GET
Get a single question and its answers.

Headers: None
Payload: None
Success: 200
Response:
```
{
    questionid: 234,
    question: this is a question,
    sectionid: 1234,
    used: 0,
    correct: 0,
    archive: false,
    answers: [
        {
            answerid: 34,
            answer: this is an answer,
            questionid: 234,
            correct: false,
            chosen: 0
        },
        ...
    ]
}
```

### PUT
Update fields in a given section.  Extra fields are ignored, not all possible
fields need to be provided.

Headers: Token=<40 digit token>
Payload:
```
{
    question: this is a question,
    sectionid: 1234
}
```
Success: 204
Response: None

### DELETE
Delete an active question.  Deleted questions have their archive flag set to
true and will no longer appear in queries.
Headers: Token=<40 digit token>
Payload: None
Success: 204
Response: None

## Answer
The fields in answer are:
answerid: Integer, Unique identifier for an answer.
correct: Boolean, True for the correct answer
questionid: Integer, Relates to the question table.  The question this answer
belongs to.
archive: Boolean, When true, this question will no longer appear in queries.
chosen: Integer, The number of times this answer has been chosen by a user.

```
amttest/api/question/<int:questionid>/answer
```
### POST
Create a new question for a given answer.

Headers: Token=<40 digit token>
Payload:
```
{
    answer: this is an answer,
    correct: false
}
```
Success: 201
Response:
```
{
    answerid: 34,
    answer: this is an answer,
    questionid: 234,
    correct: false,
    chosen: 0
}
```
--------------------------------------------------------------------------------
```
amttest/api/answer/<int:answreid>
```
### GET
Gets one given answer.

Headers: None
Payload: None
Success: 200
Response:
```
{
    answerid: 34,
    answer: this is an answer,
    questionid: 234,
    correct: false,
    chosen: 0
}
```

### PUT
Update a given answer.  Extra fields are ignored, and not all possible fields
need to be included.

Headers: Token=<40 digit token>
Payload:
```
{
    answer: this is an answer,
    questionid: 234,
    correct: false,
}
```
Success: 204
Response: None

### DELETE
Delete a given answer.  Deleted answers have their archive flag set to true, and
will no longer appear in queries.

Headers: Token=<40 digit token>
Payload: None
Success: 204
Response: None

## Certificate
The fields for certificate are:
certid: Integer, The unique identifier for a cetificate.
userid: Integer, Related to the User table.  The user this certificate
                 belongs to.
examid: Integer, Related to the Exam table.  The exam this certificate belongs
                 to.
correct: Integer, Number of questions that were answered correctly.
possible: Integer, Number of questions that were given for the exam.
passed: Boolean, True if the correct/possible was greater than or equal to the
                 required passing score from the exam AT THE TIME OF TAKING THE
                 TEST.
testdate: Date, Date this test was taken.
archive: Boolean, When true, this certificate will no longer appear in queries.

```
amttest/api/certificate/<int:userid>/<int:examid>
```
### POST
Grade an exam, and create a new certificate based on the results.
Here we are expecting the question number, and the answer the user chose.
Grading is all done on the back end, so the answers cannot be looked up by
the user mid test.

Stats for questions and answers are also updated during grading.

Headers: Token=<40 digit token>
Payload:
```
[
    {questionid: 1234,
     answerid: 234
    },
    {questionid: 1235,
     answerid: 267
    },
    ...
]
```
Success: 201
Response:
```
{
    certid: 1234,
    userid: 2345,
    examid: 4567,
    correct: 24,
    possible: 25,
    passed: true,
    testdate: YYYY-MM-DD HH:MM:SS.SSS
}
```

### GET
Get a certificate for a given user and exam.

Headers: None
Payload: None
Success: 200
Response:
```
{
    certid: 1234,
    userid: 2345,
    examid: 4567,
    correct: 24,
    possible: 25,
    passed: true,
    testdate: YYYY-MM-DD HH:MM:SS.SSS
}
```
--------------------------------------------------------------------------------
```
amttest/api/certificate/user/<int:userid>
```
### GET
Get all cetificates for a given user.

Headers: None
Payload: None
Success: 200
Response:
```
[
    {
        certid: 1234,
        userid: 2345,
        examid: 4567,
        correct: 24,
        possible: 25,
        passed: true,
        testdate: YYYY-MM-DD HH:MM:SS.SSS
    },
    {
        certid: <int>,
        userid: <int>,
        examid: <int>,
        correct: <int>,
        possible: <int>,
        passed: <bool>,
        testdate: <date>
    },
    ...
]
```
--------------------------------------------------------------------------------
```
amttest/api/certificate/exam/<int:examid>
```
### GET
Get all certificates for a given exam.

Headers: None
Payload: None
Success: 200
Response:
```
[
    {
        certid: 1234,
        userid: 2345,
        examid: 4567,
        correct: 24,
        possible: 25,
        passed: true,
        testdate: YYYY-MM-DD HH:MM:SS.SSS
    },
    {
        certid: <int>,
        userid: <int>,
        examid: <int>,
        correct: <int>,
        possible: <int>,
        passed: <bool>,
        testdate: <date>
    },
    ...
]
```
--------------------------------------------------------------------------------
```
amttest/api/certificate
```
### GET
Get every certificate issued ever.

Headers: None
Payload: None
Success: 200
Response:
```
[
    {
        certid: 1234,
        userid: 2345,
        examid: 4567,
        correct: 24,
        possible: 25,
        passed: true,
        testdate: YYYY-MM-DD HH:MM:SS.SSS
    },
    {
        certid: <int>,
        userid: <int>,
        examid: <int>,
        correct: <int>,
        possible: <int>,
        passed: <bool>,
        testdate: <date>
    },
    ...
]
```
