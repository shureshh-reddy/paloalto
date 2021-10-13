import git
import os
import time


repo_root_dir = '/root/paloalto'
token = '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'
branch = 'master'
repo_name = 'paloalto'

def git_push():
    path = os.getcwd()
    print(path)
    if os.path.isdir(path):
        print('this is repo')
        repo = git.Repo(path)
    fetch_commad = 'git fetch origin {}:{}'.format('master', 'master')
    add_command = 'git add .'
    commit_msg = "git commit -m 'auto commit from system'"
    os.system(add_command)
    time.sleep(1)
    os.system(commit_msg)

git_push()
