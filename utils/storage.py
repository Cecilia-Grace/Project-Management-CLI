import os
import json
from models.project import Project
from models.task import Task
from models.user import User


#paths where files are
data_dir = "data"
users_file = os.path.join(data_dir, "users.json")
tasks_file = os.path.join(data_dir, "tasks.json")
projects_file = os.path.join(data_dir, "projects.json")

def ensure_data_exists():               #makes sure data exists
    os.makedirs(data_dir, exist_ok=True)
    
#project
def save_projects(projects_list):               #saves data
    ensure_data_exists()
    serializable_data = [p.to_dict() for p in projects_list]
    with open(projects_file, "w") as f:
        json.dump(serializable_data, f, indent=4)

def load_projects():            #loads data
    if not os.path.exists(projects_file):
        return []
    with open(projects_file, "r") as f:
        try:
            raw_data = json.load(f)
            return [Project.from_dict(item) for item in raw_data]
        except json.JSONDecodeError:
            return []
        
#tasks
def save_tasks(tasks_list):               #saves data
    ensure_data_exists()
    serializable_data = [t.to_dict() for t in tasks_list]
    with open(tasks_list, "w") as f:
        json.dump(serializable_data, f, indent=4)

def load_tasks():            #loads data
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, "r") as f:
        try:
            raw_data = json.load(f)
            return [Task.from_dict(item) for item in raw_data]
        except json.JSONDecodeError:
            return []



#users
def save_users(users_list):               #saves data
    ensure_data_exists()
    serializable_data = [u.to_dict() for u in users_list]
    with open(users_file, "w") as f:
        json.dump(serializable_data, f, indent=4)

def load_users():            #loads data
    if not os.path.exists(users_file):
        return []
    with open(users_file, "r") as f:
        try:
            raw_data = json.load(f)
            return [User.from_dict(item) for item in raw_data]
        except json.JSONDecodeError:
            return []