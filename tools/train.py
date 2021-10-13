import os
import uuid

import subprocess
import datetime
import git.exc
from git import Repo

import time
st = time.time()
backup_remote_path = r"git@github.com:nfsergiu/mytestrepo2.git"
backup_remote_name = "backup"

cur_file_path = os.path.realpath(__file__)
repo_path = os.path.dirname(os.path.dirname(cur_file_path))

repo = Repo(repo_path)

try:
    remote_backup = repo.create_remote(backup_remote_name, backup_remote_path)
except git.exc.GitCommandError:
    pass

active_branch = repo.active_branch

backup_branch_name = uuid.uuid4().hex

cur_time = f"{datetime.datetime.now()}".replace(" ", "__").split(".")[0]

commands = [f"git checkout -b {backup_branch_name}",
f"git add .",
f"git commit -m \"{active_branch}__at__{cur_time}\"",
f"git push {backup_remote_name} {backup_branch_name}",
f"git checkout --detach",
f"git reset --soft {active_branch}",
f"git checkout {active_branch}",
            ]
for command in commands:
    print(command)
    subprocess.run(command.split(" "))

print(time.time() - st)