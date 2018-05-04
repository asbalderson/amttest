# Routes
Here are the routes available from the amttest api.  The methods supported,
headers required, expected payload, and return content, are all documented below

Order is based on expected use/flow for the api.

All, PUT, POST, DELETE calls require a token in the headers i.e.
Token=server_generated_token



## User
User has the following fields:<br>
userid: Integer, generated user identifier for each user, always unique.<br>
fbuserid: Text, the user id from facebook.  This is only used for log in, and
                should never be returned.<br>
amt_name: Text, A users amtgard persona name, not required, good to have.  Optional<br>
name: Text, The users real name.<br>
email: Text, The users email address.<br>
kingdom: Text, The kingdom that the user is a member of.  Optional<br>
admin: Boolean, When true, the user can access the admin panel.<br>
archive: Boolean, When true, the user is no longer available for viewing.<br>

--------------------------------------------------------------------------------


```
amttest/api/user
```
### GET
Get all active users

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
Payload:<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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
Headers: Token=server_generated_token<br>
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
Success: 204<br>
Response: None<br>

### DELETE
"Delete" a user.  Users are not actually deleted, their flag is set to archive.

Headers: Token=server_generated_token<br>
Payload: None<br>
Success: 204<br>
Response: None<br><br>

--------------------------------------------------------------------------------

## Exam
Exam has the following fields:<br>
examid: Integer, the exam's identifier, always unique.<br>
time_limit: Integer, The number of minutes given for the user to take the exam.<br>
name: Text, The plain text name of the exam.<br>
pass_percent: Integer, The whole number value required to pass the exam, i.e. 70.<br>
expiration: Integer, The number of months the certifications from the exam are valid.<br>
ula: Text, What the user agrees to before they take the exam.<br>
archive: Boolean, When true, the exam will no longer be available from queries.<br>

```
amttest/api/exam
```
### GET
Get all exams

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
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
Success: 201<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
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
Success: 204<br>
Response: None

### DELETE
Delete an exam.  Deleted exams have the archive flag set to True and will no
longer appear in queries.

Headers: Token=server_generated_token<br>
Payload: None<br>
Success: 204<br>
Response:None<br>

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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

--------------------------------------------------------------------------------

## Section
The fields in section are:<br>
sectionid: Integer, The unique identifier for the section.<br>
name: Text, Name of the section as seen by the admin.<br>
examid: Integer, Related to the exam table.  The exam that this section belongs to.<br>
active_questions: Integer, The number of questions to use from this section for each exam.<br>
archive: Boolean, When true, the section will no longer appear in queries.<br>

```
amttest/api/exam/<int:exam_id>/section
```
### GET
Get all sections for a given exam

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
Payload:
```
{
    name: General,
    active_qustions: 3
}
```
Success: 201<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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
```
### GET
Get the section data + all question data for any question in that section +
answers for all the questions.  It may return too much data right now.

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
Payload:
```
{
    name: General,
    examid: 2345,
    active_qustions: 3
}
```
Success: 204<br>
Response:

### DELETE
Delete an active section.  Deleted section only have their archive flag set to
True.

Headers: Token=server_generated_token<br>
Payload: None<br>
Success: 204<br>
Response: None<br>

--------------------------------------------------------------------------------

## Question
The fields in question are:<br>
questionid: Integer, The unique identifier for the question.<br>
question: Text, Actual text of the given question.<br>
sectionid: Integer, Related to the section table.  The section that this
                    question belongs to<br>
used: Integer, A count for how many times this question has been asked. Plans
               to use this for statistics.<br>
correct: Integer, How many times this question has been answered correctly.<br>
archive: Boolean, When true, will no longer appear in queries.<br>

```
amttest/api/section/<int:section_id>/question
```
### POST
Create a new question for a given section.

Headers: Token=server_generated_token<br>
Payload:
```
{
    question: this is a question
}
```
Success: 201<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
Payload:
```
{
    question: this is a question,
    sectionid: 1234
}
```
Success: 204<br>
Response: None<br>

### DELETE
Delete an active question.  Deleted questions have their archive flag set to
true and will no longer appear in queries.

Headers: Token=server_generated_token<br>
Payload: None<br>
Success: 204<br>
Response: None<br>

--------------------------------------------------------------------------------

## Answer
The fields in answer are:<br>
answerid: Integer, Unique identifier for an answer.<br>
correct: Boolean, True for the correct answer<br>
questionid: Integer, Relates to the question table.  The question this answer
belongs to.<br>
archive: Boolean, When true, this question will no longer appear in queries.<br>
chosen: Integer, The number of times this answer has been chosen by a user.<br>

```
amttest/api/question/<int:questionid>/answer
```
### POST
Create a new question for a given answer.

Headers: Token=server_generated_token<br>
Payload:
```
{
    answer: this is an answer,
    correct: false
}
```
Success: 201<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: Token=server_generated_token<br>
Payload:
```
{
    answer: this is an answer,
    questionid: 234,
    correct: false,
}
```
Success: 204<br>
Response: None<br>

### DELETE
Delete a given answer.  Deleted answers have their archive flag set to true, and
will no longer appear in queries.

Headers: Token=server_generated_token<br>
Payload: None<br>
Success: 204<br>
Response: None<br>

--------------------------------------------------------------------------------


## Certificate
The fields for certificate are:<br>
certid: Integer, The unique identifier for a cetificate.<br>
userid: Integer, Related to the User table.  The user this certificate
                 belongs to.<br>
examid: Integer, Related to the Exam table.  The exam this certificate belongs
                 to.<br>
correct: Integer, Number of questions that were answered correctly.<br>
possible: Integer, Number of questions that were given for the exam.<br>
passed: Boolean, True if the correct/possible was greater than or equal to the
                 required passing score from the exam AT THE TIME OF TAKING THE
                 TEST.<br>
testdate: Date, Date this test was taken.<br>
archive: Boolean, When true, this certificate will no longer appear in queries.<br>

```
amttest/api/certificate/<int:userid>/<int:examid>
```
### POST
Grade an exam, and create a new certificate based on the results.
Here we are expecting the question number, and the answer the user chose.
Grading is all done on the back end, so the answers cannot be looked up by
the user mid test.

Stats for questions and answers are also updated during grading.

Headers: Token=server_generated_token<br>
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
Success: 201<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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

Headers: None<br>
Payload: None<br>
Success: 200<br>
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
