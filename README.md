# Jenkins Script

This simple script uses Jenkins' API to get a list of jobs and their status from a given Jenkins instance.
The status for each job is then stored in a sqlite database along with the time for when it was checked.

## Usage

Install required packages from *requirements.txt* using:

`pip install -r requirements.txt`

Then simply run *jenkins_script.py* on python with the username, password, and instance url in the following format:

`python jenkins_script.py [-h] --user USERNAME --pass PASSWORD instance`