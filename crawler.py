"""
 Author: Jiawen Liu
 Question: Crawl Pull Requests
 Description: I plan to study all pull requests in GitHub project guava. However, there
              is no database available. Could you build a crawler to download all pull requests in project
              guava, parse them, and store them into a .csv file? After you finish, please share with me
              the .csv file. Collecting following info:
              Title, Labels, Reviewers, Assignees, Comments, Opened time, Closed time, Number of commits,
              Number of changed files, Number of participants
 Libraries:   requests, github, bs4.
              Please install these libraries with following commands before executing the program:
              pip install requests
              pip install bs4
              pip install pygithub
 Solution:    Executing this file will generate a csv file containing required info from github project guava
              to the same file location. A generated pr_result.csv is attached because running this program takes
              around 20 mins. Also update the github token in line 36 before executing the program.
              Reviewers, Comments, Number of Participants are not available from github Pulls API, so I crawl the
              pull request page to get them; others are retrieved from Pulls API.
"""
import re
import time
import requests
from github import Github
from bs4 import BeautifulSoup
import csv

#BASE_URL = "https://github.com/google/guava/pull/"

csv_file = open("pr_result.csv", "w", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Title","Labels","Reviewers","Assignees","Comments","Opened time","Closed time","Number of commits",
                     "Number of changed files","Number of participants"])
start = time.time()
print("Crawling Pull Requests from guava...")
github_instance = Github("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") # TODO: Change the github token here
repo = github_instance.get_repo("google/guava") # Change here to parse another repo
pull_requests = repo.get_pulls(state='all', sort='created') # Use Pulls API to get all pull requests

for pr in pull_requests: # Loop through all pull requests
    print(f"Crawling issue {pr.number}")
    html = requests.get(pr.html_url) # Crawl current pull request page with url retrieved from Pulls API
    bs = BeautifulSoup(html.text, features="html.parser")
    participants = 0
    try:
        participants = re.findall("\d+", bs.find("div", id="partial-users-participants").find(
            "div", attrs={"class": "discussion-sidebar-heading text-bold"}).get_text("participants"))[0]
    except:
        pass
    labels = ""
    for label in pr.labels:
        labels += f", {label.name}"
    reviewers = ""
    try:
        for span in bs.find("form", attrs={"class":"js-issue-sidebar-form"}).find_all("span", attrs={"class":"css-truncate-target"}):
            reviewers += f", {span.get_text()}"
    except:
        pass
    assignees = ""
    try:
        for assignee in pr.assignees:
            assignees += f", {assignee.login}"
    except:
        pass
    comments = ""
    for comment in bs.find_all("div", "unminimized-comment"):
        author = comment.find("strong").find("a", attrs={"class": "author"}).get_text()
        ps = "" # Comment messages
        # If author type next line(enter) in comment message, the text of next line will be under another <p> tag
        # Loop through all <p> to get full comment from the author
        for p in comment.find_all("p"):
            ps += p.get_text() + " "
        comments += f"{author}: {ps} "
    output = [f"Issue#{pr.number} {pr.title}", labels[2:], reviewers[2:], assignees[2:], comments, pr.created_at,
              pr.closed_at, pr.commits,pr.changed_files, participants]
    csv_writer.writerow(output)
csv_file.close()
print("Done! time used:", time.time() - start)
