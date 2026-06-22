import argparse
from datetime import date, datetime
from models.project import Project
from models.task import Task
from models.user import User
from utils.storage import load_projects, save_projects
from utils.storage import load_tasks, save_tasks
from utils.storage import load_users, save_users


#project
def handle_create_project(args):            #creating a new project
    #Load the existing projects from json file
    projects = load_projects()
    
    #check if a project name already exists to prevent duplicates
    if any(p.project_title.lower() == args.title.lower() for p in projects):
        print(f"Project named '{args.title}' already exists.")
        return

    new_project = Project(
        project_title=args.title,
        user_id=args.user_id,
        due_date=args.due,
        project_description=args.desc
    )
    
    #appends and saves it 
    projects.append(new_project)
    save_projects(projects)
    print(f"✅ Successfully created new project!")
    print(new_project)  
    

def handle_list_projects(args):         #displays existing projects
    projects = load_projects()
    
    if not projects:
        print("No projects found.")
        return
        
    print(f"Current Projects Overview ({len(projects)} total):")
    print("-" * 50)
    for project in projects:
        print(project)
    print("-" * 50)
    

def handle_delete_project(args):
    """removing a project and its associated tasks."""
    projects = load_projects()
    
    updated_projects = [p for p in projects if p.id != args.project_id]     #pick specific project
    
    if len(projects) == len(updated_projects):
        print(f"❌ Error: Project with ID '{args.project_id}' does not exist.")
        return

    #save updated project list back to projects.json
    save_projects(updated_projects)
    print(f"🗑️ Project [{args.project_id}] has been deleted successfully.")

    #remove all tasks matching this project_id
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t.project_id != args.project_id]
    
    if len(tasks) != len(updated_tasks):
        save_tasks(updated_tasks)
        print(f"🧹 Cleaned up {len(tasks) - len(updated_tasks)} task(s) linked to that project.")
    
    
#tasks
def handle_create_tasks(args):            #creating a new task
    #Load the existing tasks from json file
    tasks = load_tasks()
    projects = load_projects()
    users = load_users()
    
    project_exists = (p.id == args.project_id for p in projects)
    if not project_exists:
        print(f"Project ID '{args.project_id}' does not exist")
        return
    
    if args.assigned_to:
        user_exists = (u.id == args.assigned_to for u in users)
        if not user_exists:
            print(f"User ID '{args.assigned_to}' does not exist")
            return

    new_task = Task(
        project_id=args.project_id,
        task_title=args.title,
        status=args.status,
        assigned_to=args.assigned_to,
    )
    
    #appends and saves it 
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Successfully created new task!")
    print(new_task)  
    

def handle_list_tasks(args):         #displays existing tasks
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found.")
        return
    
    if args.project_id:         #for a specific project id
        tasks = [t for t in tasks if t.project_id == args.project_id]
        print(f"Tasks Overview for Project [{args.project_id}]:")
    else:
        print("All Tracked Tasks Overview:")              #if not specified, prints all tasks
        
        
    print(f"Current Tasks Overview ({len(tasks)} total):")
    print("-" * 50)
    for task in tasks:
        print(task)
    print("-" * 50)
    
def handle_delete_task(args):
    """removing a task"""
    tasks = load_tasks()
    
    updated_tasks = [t for t in tasks if t.id != args.title]     #pick specific task
    
    if len(tasks) == len(updated_tasks):
        print(f"Task '{args.title}' does not exist.")
        return

    #save updated tasks list back to projects.json
    save_projects(updated_tasks)
    print(f"🗑️ tasks [{args.title}] has been deleted successfully.")
    


#users
def handle_create_users(args):            #creating a new user
    #Load the existing users from json file
    users = load_users()
    
    if any(u.username.lower() == args.username.lower() for u in users):
        print(f"The username '{args.username}' is already taken.")
        return

    new_user = User(
        username=args.username,
        email=args.email,
    )
    
    #appends and saves it 
    users.append(new_user)
    save_users(users)
    print(f"✅ Successfully created new user!")
    print(new_user)  
    

def handle_list_users(args):         #displays existing projects
    users = load_users()
    
    if not users:
        print("No users found.")
        return
        
    print(f"Current Users Overview ({len(users)} total):")
    print("-" * 50)
    for user in users:
        print(user)
    print("-" * 50)
    

def handle_delete_user(args):
    """removing a user and un-assigning their tasks."""
    users = load_users()
    
    #target user
    updated_users = [u for u in users if u.id != args.user_id]
    
    # If the lengths match, no user was found with that ID
    if len(users) == len(updated_users):
        print(f"User with ID '{args.user_id}' does not exist.")
        return

    #Save the updated user list back to users.json
    save_users(updated_users)
    print(f"🗑️ User [{args.user_id}] has been removed.")

    # 3. Clean up task assignments: Set matching assigned_to fields back to None
    tasks = load_tasks()
    updated_count = 0
    
    for task in tasks:
        if task.assigned_to == args.user_id:
            task.assigned_to = None  
            updated_count += 1
            
    if updated_count > 0:
        save_tasks(tasks)
        print(f"🧹 Unassigned {updated_count} task(s) previously owned by this user.")
    


    
    
    

def main():
    #instantiate the root parser
    parser = argparse.ArgumentParser(description="Project Manager CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands")

    #project
    #command: pm create-project
    create_parser = subparsers.add_parser("create-project", help="Create a new project")
    create_parser.add_argument("title", type=str, help="The title of the project")
    create_parser.add_argument("user_id", type=str, help="The ID of the owner user")
    create_parser.add_argument("--due", type=str, default="No deadline", help="Due date (YYYY-MM-DD)")
    create_parser.add_argument("--desc", type=str, default="", help="Short description text")
    create_parser.set_defaults(func=handle_create_project)

    #command: pm list-projects
    list_parser = subparsers.add_parser("list-projects", help="List all saved projects")
    list_parser.set_defaults(func=handle_list_projects)
    
    # Command: pm delete-project
    delete_parser = subparsers.add_parser("delete-project", help="Delete a project and its tasks")
    delete_parser.add_argument("project_id", type=str, help="The 6-character unique ID of the project")
    delete_parser.set_defaults(func=handle_delete_project)
    
    
    """tasks"""
    #command: pm create-task
    task_parser = subparsers.add_parser("create-task", help="Add a task to a project")
    task_parser.add_argument("project_id", type=str, help="The ID of the project this task belongs to")
    task_parser.add_argument("title", type=str, help="The name/title of the task")
    task_parser.add_argument("--status", type=str, default="", help="Task status (To Do, In Progress, Done)")
    task_parser.add_argument("--assigned_to", type=str, help="Owner of the project")
    task_parser.set_defaults(func=handle_create_tasks)

    # Command: pm list-tasks
    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks")
    list_tasks_parser.add_argument("--project-id", type=str, default=None, help="Filter tasks by a specific project ID")
    list_tasks_parser.set_defaults(func=handle_list_tasks)
    
    # Command: pm delete-task
    delete_parser = subparsers.add_parser("delete-task", help="Delete a task")
    delete_parser.add_argument("title", type=str, help="The exact task title")
    delete_parser.set_defaults(func=handle_delete_task)
    
    
    """users"""
    #command: pm create-user
    create_parser = subparsers.add_parser("create-user", help="Create a new user")
    create_parser.add_argument("username", type=str, help="The name of the user")
    create_parser.add_argument("email", type=str, help="The email of the user")
    create_parser.set_defaults(func=handle_create_users)

    #command: pm list-user
    list_parser = subparsers.add_parser("list-users", help="List all saved users")
    list_parser.set_defaults(func=handle_list_users)
    
    # Command: pm delete-user
    delete_parser = subparsers.add_parser("delete-user", help="Delete a user")
    delete_parser.add_argument("username", type=str, help="The exact username")
    delete_parser.set_defaults(func=handle_delete_user)
    

    #parsing logic
    args = parser.parse_args()
    args.func(args)         #calls the assigned handler function 

if __name__ == "__main__":
    main()