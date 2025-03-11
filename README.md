API testing project.

To run the tests:

git clone https://github.com/amielnoy/RafaelApiPytestGithubActionsTest 

## installation.
1.create virtual env:
python3 -m venv venv

install all packages:
pip install -r requirements.txt


LOCALLY:
1.run flask:
from root folder in terminal:  
flask run

2.Run tests:
Python3 -m pytest tests

LOCALLY USING docker:
1.run chmod +x runDocker.sh
2.run runDocker.sh 
3.Run tests
python3 -m pytest tests

To run on github actions 
https://github.com/amielnoy/RafaelApiPytestGithubActionsTest/actions/runs/

and click rerun all jobs button
