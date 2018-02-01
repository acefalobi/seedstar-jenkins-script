"""

This simple script uses Jenkins' API to get a list of jobs
and their status from a given Jenkins instance.
The status for each job is then stored in a sqlite database
along with the time for when it was checked.

"""

import argparse
import sqlite3

from datetime import datetime

from jenkinsapi.jenkins import Jenkins

DB_NAME = 'jenkins_jobs.db'

def get_jenkins_instance(url, username, password):
    """
    Retrieve Jenkins Instance from url and authentication details
    """

    server = Jenkins(url, username=username, password=password)
    return server


def save_job(instance_url, job_name, job_status):
    """
    Save Jenkins job and status to SQLite DB
    """

    # initialize SQLite
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        # Try to create "jobs" table if it hasn't been created
        cursor.execute("CREATE TABLE jobs (instance_url, name, status, date_checked)")
    except sqlite3.OperationalError:
        # Do nothing since table has already been created
        pass

    query = ("INSERT INTO jobs VALUES ('{instance}', '{job}', '{status}', '{checkin}')"
             .format(
                 instance=instance_url, job=job_name, status=job_status, checkin=datetime.now()
                 ))

    # Execute INSERT query and conclude operation
    cursor.execute(query)
    connection.commit()
    connection.close()


def main(args):
    """
    Retrieve Jenkins Instance from url and save all jobs to SQLite DB
    """

    # Get Jenkins Instance
    print("Connecting to jenkins instance...")
    jenkins_instance = get_jenkins_instance(args.instance_url, args.username, args.password)
    print("Connected")

    # Get all jobs from Jenkins Instance
    print("Retrieving Jobs...")
    jobs = jenkins_instance.get_jobs()

    # Iterate through and save all jobs

    print("Saving jobs to DB...")
    for job_name, job_instance in jobs:
        save_job(args.instance_url, job_instance, job_instance.get_last_build().get_status())
        print("Saved job: " + job_name)

    print("Success! Saved all jobs.")


if __name__ == '__main__':
    # Create argument parser to get arguments

    PARSER = argparse.ArgumentParser(description="JenkinsAPI CLI Interface")
    PARSER.add_argument("instance_url", metavar="instance", type=str)
    PARSER.add_argument("--user", "-u", dest="username", type=str, required=True)
    PARSER.add_argument("--pass", "-p", dest="password", type=str, required=True)

    ARGS = PARSER.parse_args()

    # And off we go \(oo)/
    main(ARGS)
