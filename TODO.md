# TODO
1) No route should allow updating or posting of a primary or foreign key, or
any field used for statistics, or which is auto generated. Unit tests should
be updated to include tests for these changes

2) Changes need to be made or understood so the whole application doesnt require
sudo to run. Research also needs to be done to see if there is a way to make
the api a service? May need to switch to a config file instead of command line
arguments in this case.

3) Routes need to be added to pull archived values, this isnt needed right away
but will be relevent eventually, especially once someone deletes something they
didnt want to.

4) A route should be added for importing from a file, instead of making it
required to do from the command line.

5) Commands need to be added to update the database or back it up. Addionally
there should be some checks as the API starts to confirm that the database has
the proper structure, to prevent errors in the future.

6) A route would be nice to pull down logging when needed, to debug remotely.
Even if the route just returns the most recent log file.